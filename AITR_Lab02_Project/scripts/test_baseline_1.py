# scripts/test_baseline_1.py
import sys
import os
import time

# Ensure Python can find the src folder
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.data_loader import load_and_validate_data
from src.baseline_1_gemini import setup_gemini, format_abstracts, generate_naive_rag_synthesis, evaluate_with_llm_judge

print("--- Testing Baseline 1 & LLM Judge ---")
try:
    # 1. Load data and take a tiny sample (2 papers) to save tokens/time
    df = load_and_validate_data("stratified_arxiv_dataset_4.csv")
    test_batch = df.head(2)
    formatted_context = format_abstracts(test_batch)
    print(f"[OK] Formatted context length: {len(formatted_context)} characters")

    # 2. Setup Gemini
    model = setup_gemini()
    print("[OK] Gemini Model Initialized")

    # 3. Generate Synthesis
    print("Generating synthesis (this may take a few seconds)...")
    synthesis = generate_naive_rag_synthesis(model, formatted_context)
    print(f"[OK] Synthesis generated. Length: {len(synthesis)} characters")
    # Sleep to respect free-tier rate limits
    time.sleep(4)

    # 4. Run LLM Judge
    print("Running LLM-as-a-judge evaluation...")
    scores = evaluate_with_llm_judge(model, formatted_context, synthesis)
    
    print("\n--- Final Judge Output ---")
    import json
    print(json.dumps(scores, indent=2))
    print("--------------------------")

except Exception as e:
    print(f"\n[FAIL] Baseline test failed: {e}")