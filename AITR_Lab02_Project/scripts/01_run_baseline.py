# scripts/01_run_baseline.py
import sys
import os
import time
import pandas as pd

# Ensure Python can find the src folder
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.data_loader import load_and_validate_data
from src.baseline_1_gemini import setup_gemini, format_abstracts, generate_naive_rag_synthesis, evaluate_with_llm_judge

def run_main_experiment():
    print("--- Starting Full Baseline 1 Execution (Scale Up) ---")
    api_key = setup_gemini()
    df = load_and_validate_data("stratified_arxiv_dataset_4.csv")
    
    results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
    os.makedirs(results_dir, exist_ok=True)
    output_file = os.path.join(results_dir, "baseline_1_results.csv")
    
    results = []
    windows = ['Pre-Cutoff', 'Near-Cutoff', 'Post-Cutoff']
    batch_size = 10
    
    for window in windows:
        print(f"\nProcessing Temporal Window: {window}")
        window_df = df[df['temporal_window'] == window].sample(frac=1, random_state=42).reset_index(drop=True)
        
        # Process the 100 papers in batches of 10
        for i in range(0, len(window_df), batch_size):
            batch_num = (i // batch_size) + 1
            print(f"  -> Processing Batch {batch_num}/{len(window_df) // batch_size}...")
            
            sample_df = window_df.iloc[i:i+batch_size]
            context = format_abstracts(sample_df)
            
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    synthesis = generate_naive_rag_synthesis(api_key, context)
                    time.sleep(3) # Standard rate limit pause
                    
                    scores = evaluate_with_llm_judge(api_key, context, synthesis)
                    
                    results.append({
                        "temporal_window": window,
                        "batch_id": batch_num,
                        "omission_score": scores.get("omission_score"),
                        "omission_reasoning": scores.get("omission_reasoning"),
                        "stale_framing": scores.get("stale_framing"),
                        "stale_framing_reasoning": scores.get("stale_framing_reasoning"),
                        "generated_synthesis": synthesis
                    })
                    print(f"     [OK] Omission: {scores.get('omission_score')}, Stale Framing: {scores.get('stale_framing')}")
                    break # Success, exit the retry loop
                    
                except Exception as e:
                    if attempt < max_retries - 1:
                        print(f"     [WARN] HTTP error on batch {batch_num}. Retrying in {10 * (attempt + 1)}s... ({e})")
                        time.sleep(10 * (attempt + 1)) # Exponential backoff
                    else:
                        print(f"     [FAIL] Fatal error on batch {batch_num} after 3 attempts: {e}")
            
            time.sleep(3) # Pause before the next batch
            
            
    # Save the expanded results
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_file, index=False)
    print(f"\n--- Experiment Complete. 30 batches saved to {output_file} ---")

if __name__ == "__main__":
    run_main_experiment()