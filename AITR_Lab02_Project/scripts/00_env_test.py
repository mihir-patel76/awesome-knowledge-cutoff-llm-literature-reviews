import pandas as pd
import scipy
import google.generativeai as genai
import sys
import os

print("--- Environment Test ---")
print(f"Python version: {sys.version.split()[0]}")
print(f"pandas version: {pd.__version__}")
print(f"scipy version: {scipy.__version__}")
try:
    print(f"google-generativeai version: {genai.__version__}")
except AttributeError:
    print("google-generativeai version: (installed but version hidden)")

# Test reading the dataset
try:
    # Look for the dataset in the parent directory
    dataset_path = os.path.join(os.path.dirname(__file__), '..', 'stratified_arxiv_dataset_3.csv')
    df = pd.read_csv(dataset_path)
    print(f"[OK] Dataset loaded. Shape: {df.shape}")
    
    # Test groupby
    bins = df.groupby('temporal_window').size()
    print(f"[OK] Temporal bins detected:\n{bins}")
    
    # Test sample
    sample = df.sample(n=min(10, len(df)), random_state=42)
    print(f"[OK] Sampling successful. Sample shape: {sample.shape}")
    
except FileNotFoundError:
    print("[FAIL] stratified_arxiv_dataset_3.csv not found.")
except Exception as e:
    print(f"[FAIL] Data manipulation test failed: {e}")

print("--- End of Test ---")
