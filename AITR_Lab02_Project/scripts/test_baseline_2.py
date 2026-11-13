# scripts/test_baseline_2.py
import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.data_loader import load_and_validate_data
from src.baseline_2_legacy import setup_legacy_model, generate_legacy_rag_synthesis

print("--- Testing Baseline 2 (Legacy Model) ---")
try:
    df = load_and_validate_data("stratified_arxiv_dataset_4.csv")
    test_batch = df.head(2)
    
    context = ""
    for _, row in test_batch.iterrows():
        context += f"ID: {row['paper_id']} | Abstract: {row['abstract']}\n\n"
    context = context.strip()

    api_key = setup_legacy_model()
    print("[OK] Legacy Model Endpoint Initialized")

    print("Generating legacy synthesis...")
    synthesis = generate_legacy_rag_synthesis(api_key, context)
    
    print(f"\n[OK] Synthesis generated successfully. Length: {len(synthesis)} chars")
    print(f"Preview:\n{synthesis[:200]}...")

except Exception as e:
    print(f"\n[FAIL] Legacy Baseline test failed: {e}")