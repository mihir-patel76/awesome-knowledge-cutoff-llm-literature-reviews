import pandas as pd
import scipy.stats as stats
import os
import sys

def generate_paper_results():
    results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
    b1_path = os.path.join(results_dir, "baseline_1_results.csv")
    b2_path = os.path.join(results_dir, "baseline_2_results.csv")
    
    if not os.path.exists(b1_path) or not os.path.exists(b2_path):
        print("Error: Missing result CSVs. Run Baseline 1 and 2 first.")
        sys.exit(1)
        
    df_modern = pd.read_csv(b1_path).dropna(subset=['omission_score', 'stale_framing'])
    df_legacy = pd.read_csv(b2_path).dropna(subset=['omission_score', 'stale_framing'])

    print("="*60)
    print(" 📊 PART 1: STATISTICAL PROOF (QUANTITATIVE) ")
    print("="*60)
    
    def run_stats(df, model_name):
        print(f"\n[{model_name} Model]")
        # 1. Omission (Kruskal-Wallis)
        windows = df['temporal_window'].unique()
        omission_groups = [df[df['temporal_window'] == w]['omission_score'] for w in windows]
        
        if len(omission_groups) > 1:
            try:
                stat_k, p_k = stats.kruskal(*omission_groups)
                sig = "SIGNIFICANT (p < 0.05)" if p_k < 0.05 else "NOT SIGNIFICANT"
                print(f"  Omission Decay (Kruskal-Wallis): p-value = {p_k:.4f} -> {sig}")
            except ValueError:
                print("  Omission Decay: Skipped (Zero variance in scores)")
        
        # 2. Stale Framing (Chi-Square)
        contingency = pd.crosstab(df['temporal_window'], df['stale_framing'])
        if contingency.shape[1] > 1 and contingency.shape[0] > 1:
            chi2, p_chi2, _, _ = stats.chi2_contingency(contingency)
            sig = "SIGNIFICANT (p < 0.05)" if p_chi2 < 0.05 else "NOT SIGNIFICANT"
            print(f"  Stale Framing (Chi-Square): p-value = {p_chi2:.4f} -> {sig}")
        else:
            print("  Stale Framing: Skipped (Zero variance in scores)")

    run_stats(df_modern, "Modern (Gemini 3.5)")
    run_stats(df_legacy, "Legacy Control (Gemini 1.0)")
    
    print("\n" + "="*60)
    print(" 📝 PART 2: QUALITATIVE EVIDENCE (TEXT SAMPLES) ")
    print("="*60)
    
    # Filter for Modern model failing on Post-Cutoff data
    failures = df_modern[(df_modern['temporal_window'] == 'Post-Cutoff') & (df_modern['stale_framing'] == 1)]
    
    if failures.empty:
        print("\nNo stale framing failures found in the Post-Cutoff window for the modern model.")
    else:
        print(f"\nFound {len(failures)} instances of stale framing in Post-Cutoff window. Showing top 2 examples:\n")
        samples = failures.head(2)
        
        for idx, row in samples.iterrows():
            print(f"--- Example {idx + 1} ---")
            print(f"Batch ID: {row.get('batch_id', 'N/A')}")
            print(f"Generated Synthesis (Excerpt): {str(row['generated_synthesis'])[:300]}...")
            print(f"\nJudge's Omission Reasoning:\n> {row['omission_reasoning']}")
            print(f"\nJudge's Stale Framing Reasoning:\n> {row['stale_framing_reasoning']}")
            print("-" * 40 + "\n")

if __name__ == "__main__":
    generate_paper_results()