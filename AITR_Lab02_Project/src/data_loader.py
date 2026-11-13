import pandas as pd
import os

def load_and_validate_data(filename="stratified_arxiv_dataset_4.csv"):
    filepath = os.path.join(os.path.dirname(__file__), '..', filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset not found at {filepath}")
    
    df = pd.read_csv(filepath)
    
    required_cols = {'paper_id', 'published_date', 'temporal_window', 'title', 'abstract'}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Missing columns. Expected {required_cols}, found {df.columns}")
        
    expected_windows = {'Pre-Cutoff', 'Near-Cutoff', 'Post-Cutoff'}
    found_windows = set(df['temporal_window'].unique())
    if not expected_windows.issubset(found_windows):
        raise ValueError(f"Missing temporal windows. Found {found_windows}")
        
    return df
