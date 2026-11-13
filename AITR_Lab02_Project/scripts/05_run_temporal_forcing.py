# scripts/05_run_temporal_forcing.py
import sys
import os
import time
import json
import urllib.request
import urllib.error
import pandas as pd

# Ensure Python can find the src folder
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.data_loader import load_and_validate_data
from src.baseline_1_gemini import setup_gemini, format_abstracts, evaluate_with_llm_judge

def _call_gemini_rest(api_key, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['candidates'][0]['content']['parts'][0]['text']
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        raise RuntimeError(f"HTTP {e.code}: {error_body}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e.reason}")

def generate_temporal_forcing_synthesis(api_key, formatted_abstracts):
    # THE TARGETED MODIFICATION: Forcing parametric reconciliation
    prompt = f"""You are an expert academic researcher. Below are recent scientific abstracts. 
Synthesize these findings and explicitly contextualize how they advance, challenge, or update the historical consensus of the field prior to 2023.

<abstracts>
{formatted_abstracts}
</abstracts>

Write a concise synthesis (200-300 words). Include:
1. Current State of the Art: Established methods and consensus.
2. Open Problems: Specific unsolved challenges. 
Cite papers inline using their IDs."""
    
    return _call_gemini_rest(api_key, prompt)

def run_temporal_forcing_experiment():
    print("--- Starting Experimental Run (Temporal Forcing) ---")
    api_key = setup_gemini()
    df = load_and_validate_data("stratified_arxiv_dataset_4.csv")
    
    results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
    os.makedirs(results_dir, exist_ok=True)
    output_file = os.path.join(results_dir, "temporal_forcing_results.csv")
    
    results = []
    windows = ['Pre-Cutoff', 'Near-Cutoff', 'Post-Cutoff']
    batch_size = 10
    
    for window in windows:
        print(f"\nProcessing Temporal Window: {window}")
        
        # FIXED: Random shuffle before sequential batching to prevent chronological bias
        window_df = df[df['temporal_window'] == window].sample(frac=1, random_state=42).reset_index(drop=True)
        
        for i in range(0, len(window_df), batch_size):
            batch_num = (i // batch_size) + 1
            print(f"  -> Processing Batch {batch_num}/{len(window_df) // batch_size}...")
            
            sample_df = window_df.iloc[i:i+batch_size]
            context = format_abstracts(sample_df)
            
            # FIXED: Exponential backoff to prevent data drops on HTTP 503
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    synthesis = generate_temporal_forcing_synthesis(api_key, context)
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
                    break # Success, exit retry loop
                    
                except Exception as e:
                    if attempt < max_retries - 1:
                        print(f"     [WARN] HTTP error on batch {batch_num}. Retrying in {10 * (attempt + 1)}s... ({e})")
                        time.sleep(10 * (attempt + 1))
                    else:
                        print(f"     [FAIL] Fatal error on batch {batch_num} after 3 attempts: {e}")
            
            time.sleep(3) # Pause before next batch
            
    # Save the expanded results
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_file, index=False)
    print(f"\n--- Experiment Complete. Batches saved to {output_file} ---")

if __name__ == "__main__":
    run_temporal_forcing_experiment()
