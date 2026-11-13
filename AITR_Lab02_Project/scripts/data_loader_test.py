import sys
import os

# Ensure Python can find the src folder
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.data_loader import load_and_validate_data

print("--- Testing Data Loader ---")
try:
    df = load_and_validate_data("stratified_arxiv_dataset_4.csv")
    print(f"[OK] Data loaded successfully. Shape: {df.shape}")
    print(f"[OK] Temporal bins: {dict(df['temporal_window'].value_counts())}")
except Exception as e:
    print(f"[FAIL] Data loading failed: {e}")