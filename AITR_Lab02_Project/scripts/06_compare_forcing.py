import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import os
import sys

def run_forcing_comparison():
    print("--- Starting Comparative Analysis: Naive RAG vs. Primed RAG ---")
    results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
    
    b1_path = os.path.join(results_dir, "baseline_1_results.csv")
    b3_path = os.path.join(results_dir, "temporal_forcing_results.csv")
    
    if not os.path.exists(b1_path) or not os.path.exists(b3_path):
        print(f"[FAIL] Missing result CSVs. Ensure both Baseline 1 and Baseline 3 have been run.")
        sys.exit(1)
        
    df1 = pd.read_csv(b1_path).dropna(subset=['omission_score', 'stale_framing'])
    df1['Condition'] = 'Naive RAG (Baseline 1)'
    
    df3 = pd.read_csv(b3_path).dropna(subset=['omission_score', 'stale_framing'])
    df3['Condition'] = 'Primed RAG (Baseline 3)'
    
    combined_df = pd.concat([df1, df3], ignore_index=True)
    
    print("\n" + "="*60)
    print(" 📊 PART 1: DESCRIPTIVE STATISTICS")
    print("="*60)
    stats_df = combined_df.groupby(['Condition', 'temporal_window']).agg(
        mean_omission=('omission_score', 'mean'),
        stale_framing_count=('stale_framing', 'sum'),
        total_valid=('stale_framing', 'count')
    ).reset_index()
    stats_df['stale_pct'] = (stats_df['stale_framing_count'] / stats_df['total_valid']) * 100
    print(stats_df.to_string(index=False))

    print("\n" + "="*60)
    print(" 🧪 PART 2: TEMPORAL DECAY IN PRIMED RAG (BASELINE 3)")
    print("="*60)
    
    windows = df3['temporal_window'].unique()
    omission_groups = [df3[df3['temporal_window'] == w]['omission_score'] for w in windows]
    
    if len(omission_groups) > 1:
        try:
            stat_k, p_k = stats.kruskal(*omission_groups)
            sig = "SIGNIFICANT" if p_k < 0.05 else "NOT SIGNIFICANT"
            print(f"  Omission Decay (Kruskal-Wallis): p-value = {p_k:.4f} -> {sig}")
        except ValueError as e:
            print(f"  Omission Decay: Skipped ({e})")
            
    contingency = pd.crosstab(df3['temporal_window'], df3['stale_framing'])
    if contingency.shape[1] > 1 and contingency.shape[0] > 1:
        chi2, p_chi2, _, _ = stats.chi2_contingency(contingency)
        sig = "SIGNIFICANT" if p_chi2 < 0.05 else "NOT SIGNIFICANT"
        print(f"  Stale Framing (Chi-Square): p-value = {p_chi2:.4f} -> {sig}")
    else:
        print("  Stale Framing: Skipped (needs variance)")

    print("\n" + "="*60)
    print(" ⚔️ PART 3: DIRECT A/B TEST (POST-CUTOFF WINDOW ONLY)")
    print("="*60)
    print("Question: Did parametric priming significantly worsen synthesis of NEW evidence compared to Naive RAG?\n")
    
    post_df = combined_df[combined_df['temporal_window'] == 'Post-Cutoff']
    naive_post = post_df[post_df['Condition'] == 'Naive RAG (Baseline 1)']
    primed_post = post_df[post_df['Condition'] == 'Primed RAG (Baseline 3)']
    
    if len(naive_post) > 0 and len(primed_post) > 0:
        # Mann-Whitney U for Omission
        try:
            stat_u, p_u = stats.mannwhitneyu(naive_post['omission_score'], primed_post['omission_score'])
            sig_u = "SIGNIFICANT" if p_u < 0.05 else "NOT SIGNIFICANT"
            print(f"  Omission Difference (Mann-Whitney U): p-value = {p_u:.4f} -> {sig_u}")
        except ValueError as e:
             print(f"  Omission Difference: Skipped ({e})")
             
        # Chi-Square for Stale Framing
        contingency_ab = pd.crosstab(post_df['Condition'], post_df['stale_framing'])
        if contingency_ab.shape[1] > 1 and contingency_ab.shape[0] > 1:
            chi2_ab, p_chi2_ab, _, _ = stats.chi2_contingency(contingency_ab)
            sig_chi = "SIGNIFICANT" if p_chi2_ab < 0.05 else "NOT SIGNIFICANT"
            print(f"  Stale Framing Difference (Chi-Square): p-value = {p_chi2_ab:.4f} -> {sig_chi}")
        else:
            print("  Stale Framing Difference: Skipped (needs variance)")
    else:
        print("  Not enough Post-Cutoff data to compare.")

    # 4. Comparative Visualizations
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    order = ['Pre-Cutoff', 'Near-Cutoff', 'Post-Cutoff']
    pivot_omission = stats_df.pivot(index='temporal_window', columns='Condition', values='mean_omission').reindex(order)
    pivot_stale = stats_df.pivot(index='temporal_window', columns='Condition', values='stale_pct').reindex(order)

    pivot_omission.plot(kind='bar', ax=ax1, color=['#9370DB', '#32CD32'])
    ax1.set_title("Mean Omission Score Comparison")
    ax1.set_ylabel("Omission Score (0.0 - 1.0)")
    ax1.tick_params(axis='x', rotation=0)

    pivot_stale.plot(kind='bar', ax=ax2, color=['#9370DB', '#32CD32'])
    ax2.set_title("% of Syntheses with Stale Framing")
    ax2.set_ylabel("Percentage (%)")
    ax2.tick_params(axis='x', rotation=0)

    plt.tight_layout()
    plot_path = os.path.join(results_dir, "forcing_comparison_plot.png")
    plt.savefig(plot_path)
    print(f"\n[OK] Comparative plot saved to {plot_path}")

if __name__ == "__main__":
    run_forcing_comparison()