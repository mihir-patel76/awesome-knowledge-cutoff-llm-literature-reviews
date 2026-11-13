# scripts/07_evaluation_audit.py
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import os
import sys

def audit_and_evaluate():
    print("--- Starting Rigorous Evaluation Audit & Metrics Computation ---")
    results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
    
    b1_path = os.path.join(results_dir, "baseline_1_results.csv")
    b3_path = os.path.join(results_dir, "temporal_forcing_results.csv")
    
    if not os.path.exists(b1_path) or not os.path.exists(b3_path):
        print("[ERROR] Required files not found. Please provide the actual result CSVs.")
        sys.exit(1)
        
    df1 = pd.read_csv(b1_path)
    df3 = pd.read_csv(b3_path)
    df1['Condition'] = 'Naive RAG (Baseline 1)'
    df3['Condition'] = 'Primed RAG (Baseline 3)'
    
    df = pd.concat([df1, df3], ignore_index=True)
    
    print("\n[STEP 1] Data Integrity Audit")
    
    # 1. Missing Values Check
    missing = df[['omission_score', 'stale_framing', 'temporal_window']].isnull().sum()
    if missing.any():
        print(f"[WARN] Found missing values. Dropping rows:\n{missing}")
        df = df.dropna(subset=['omission_score', 'stale_framing', 'temporal_window'])
    else:
        print("  - [PASS] No missing values in critical columns.")
        
    # 2. Partition Alignment Check
    valid_windows = {'Pre-Cutoff', 'Near-Cutoff', 'Post-Cutoff'}
    actual_windows = set(df['temporal_window'].unique())
    if not actual_windows.issubset(valid_windows):
        raise ValueError(f"[FAIL] Data Leakage/Invalid Partitions Detected: {actual_windows}")
    print("  - [PASS] Temporal partitions are aligned and valid.")
    
    # 3. Metric Boundaries Check
    if not df['omission_score'].between(0.0, 1.0).all():
        raise ValueError("[FAIL] omission_score contains values outside [0.0, 1.0]")
    if not df['stale_framing'].isin([0, 1]).all():
        raise ValueError("[FAIL] stale_framing contains non-binary values.")
    print("  - [PASS] Metric directions and boundaries are valid.")
    
    print("\n[STEP 2] Computing Non-Parametric Statistics")
    
    post_df = df[df['temporal_window'] == 'Post-Cutoff']
    naive_post = post_df[post_df['Condition'] == 'Naive RAG (Baseline 1)']
    primed_post = post_df[post_df['Condition'] == 'Primed RAG (Baseline 3)']
    
    # Mann-Whitney U for Omission Score
    try:
        stat_u, p_u = stats.mannwhitneyu(naive_post['omission_score'], primed_post['omission_score'])
        print(f"  - Mann-Whitney U (Omission): p = {p_u:.4f}")
    except ValueError as e:
        print(f"  - Mann-Whitney U: Skipped ({e})")
        
    # Chi-Square for Stale Framing
    contingency = pd.crosstab(post_df['Condition'], post_df['stale_framing'])
    if contingency.shape[1] > 1 and contingency.shape[0] > 1:
        chi2, p_chi2, _, _ = stats.chi2_contingency(contingency)
        print(f"  - Chi-Square (Stale Framing): p = {p_chi2:.4f}")
    else:
        print("  - Chi-Square: Skipped (Zero variance in stale framing)")
        
    print("\n[STEP 3] Exporting Traceable Artifacts")
    
    # Traceable CSV Export
    traceable_path = os.path.join(results_dir, "traceable_audit_results.csv")
    df.to_csv(traceable_path, index=False)
    print(f"  - [OK] Clean, audited dataset saved to: {traceable_path}")
    
    # Publication-Quality Figure Export
    stats_df = df.groupby(['Condition', 'temporal_window']).agg(
        mean_omission=('omission_score', 'mean'),
        stale_pct=('stale_framing', lambda x: (x.sum() / x.count()) * 100)
    ).reset_index()
    
    order = ['Pre-Cutoff', 'Near-Cutoff', 'Post-Cutoff']
    pivot_omission = stats_df.pivot(index='temporal_window', columns='Condition', values='mean_omission').reindex(order)
    
    plt.figure(figsize=(8, 6))
    pivot_omission.plot(kind='bar', color=['#2c3e50', '#e74c3c'], edgecolor='black')
    plt.title("Post-Audit Omission Decay: Naive vs. Primed RAG", fontsize=14, fontweight='bold')
    plt.ylabel("Mean Omission Score", fontsize=12)
    plt.xlabel("Temporal Window", fontsize=12)
    plt.xticks(rotation=0)
    plt.legend(title="Method", loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    plot_path = os.path.join(results_dir, "publication_audit_figure.png")
    plt.savefig(plot_path, dpi=300)
    print(f"  - [OK] Publication-ready figure saved to: {plot_path}")

if __name__ == "__main__":
    audit_and_evaluate()
