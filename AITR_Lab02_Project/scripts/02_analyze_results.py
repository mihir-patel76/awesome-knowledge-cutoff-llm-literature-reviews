# scripts/02_analyze_results.py
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

def run_comparative_analysis():
    print("--- Starting Comparative Statistical Analysis ---")
    results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
    
    # 1. Load Data
    b1_path = os.path.join(results_dir, "baseline_1_results.csv")
    b2_path = os.path.join(results_dir, "baseline_2_results.csv")
    
    if not os.path.exists(b1_path) or not os.path.exists(b2_path):
        print("[FAIL] Missing one or both result CSVs.")
        sys.exit(1)
        
    df1 = pd.read_csv(b1_path)
    df1['model'] = 'Modern (3.5)'
    
    df2 = pd.read_csv(b2_path)
    df2['model'] = 'Legacy (1.0)'
    
    combined_df = pd.concat([df1, df2], ignore_index=True)
    clean_df = combined_df.dropna(subset=['omission_score', 'stale_framing']).copy()
    print(f"[OK] Loaded {len(combined_df)} rows. Kept {len(clean_df)} valid rows after dropping NaNs.")
    
    # 2. Descriptive Stats
    print("\n--- Descriptive Statistics ---")
    stats_df = clean_df.groupby(['model', 'temporal_window']).agg(
        mean_omission=('omission_score', 'mean'),
        stale_framing_count=('stale_framing', 'sum'),
        total_valid=('stale_framing', 'count')
    ).reset_index()
    stats_df['stale_pct'] = (stats_df['stale_framing_count'] / stats_df['total_valid']) * 100
    print(stats_df.to_string(index=False))

    # 3. Hypothesis Testing per Model
    print("\n--- Hypothesis Testing ---")
    for model_name in ['Modern (3.5)', 'Legacy (1.0)']:
        print(f"\n[{model_name}]")
        model_df = clean_df[clean_df['model'] == model_name]
        
        # Omission (Kruskal-Wallis)
        windows = model_df['temporal_window'].unique()
        omission_groups = [model_df[model_df['temporal_window'] == w]['omission_score'] for w in windows]
        if len(omission_groups) > 1:
            try:
                stat_k, p_k = stats.kruskal(*omission_groups)
                print(f"  Kruskal-Wallis (Omission): H = {stat_k:.4f}, p = {p_k:.4f}")
            except ValueError as e:
                print(f"  Kruskal-Wallis (Omission): Skipped ({e})")
                
        # Stale Framing (Chi-Square)
        contingency = pd.crosstab(model_df['temporal_window'], model_df['stale_framing'])
        if contingency.shape[1] > 1 and contingency.shape[0] > 1:
            chi2, p_chi2, _, _ = stats.chi2_contingency(contingency)
            print(f"  Chi-Square (Stale Framing): Chi2 = {chi2:.4f}, p = {p_chi2:.4f}")
        else:
            print("  Chi-Square (Stale Framing): Skipped (needs variance)")

    # 4. Comparative Visualizations
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Pivot for plotting
    pivot_omission = stats_df.pivot(index='temporal_window', columns='model', values='mean_omission')
    pivot_stale = stats_df.pivot(index='temporal_window', columns='model', values='stale_pct')
    
    # Enforce order
    order = ['Pre-Cutoff', 'Near-Cutoff', 'Post-Cutoff']
    pivot_omission = pivot_omission.reindex(order)
    pivot_stale = pivot_stale.reindex(order)

    pivot_omission.plot(kind='bar', ax=ax1, color=['#FFA07A', '#87CEEB'])
    ax1.set_title("Mean Omission Score Comparison")
    ax1.set_ylabel("Omission Score (0.0 - 1.0)")
    ax1.tick_params(axis='x', rotation=0)

    pivot_stale.plot(kind='bar', ax=ax2, color=['#FFA07A', '#87CEEB'])
    ax2.set_title("% of Syntheses with Stale Framing")
    ax2.set_ylabel("Percentage (%)")
    ax2.tick_params(axis='x', rotation=0)

    plt.tight_layout()
    plot_path = os.path.join(results_dir, "comparative_decay_plot.png")
    plt.savefig(plot_path)
    print(f"\n[OK] Comparative plot saved to {plot_path}")

if __name__ == "__main__":
    run_comparative_analysis()