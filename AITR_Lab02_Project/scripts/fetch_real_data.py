import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import pandas as pd

def fetch_arxiv_papers(query="large language models", max_results=2000):
    # Using a broader query to ensure we get enough older papers
    url = f'http://export.arxiv.org/api/query?search_query=all:{urllib.parse.quote(query)}&start=0&max_results={max_results}'
    
    with urllib.request.urlopen(url) as response:
        xml_data = response.read()
        
    root = ET.fromstring(xml_data)
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    
    papers = []
    for entry in root.findall('atom:entry', ns):
        paper_id = entry.find('atom:id', ns).text.split('/abs/')[-1]
        title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
        abstract = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
        published = entry.find('atom:published', ns).text[:10] # YYYY-MM-DD
        
        papers.append({
            'paper_id': paper_id,
            'published_date': published,
            'title': title,
            'abstract': abstract
        })
    return pd.DataFrame(papers)

if __name__ == "__main__":
    print("Fetching a large pool of real papers from arXiv API (this may take a minute)...")
    
    # We query for "large language models" or "NLP" to get a better temporal spread
    df = fetch_arxiv_papers(query="large language models OR retrieval", max_results=2000)
    
    cutoff_date = pd.to_datetime('2023-10-01')
    df['published_date'] = pd.to_datetime(df['published_date'])
    
    # Stratify into temporal windows
    def assign_window(date):
        if date < cutoff_date - pd.Timedelta(days=90):
            return 'Pre-Cutoff'
        elif date <= cutoff_date + pd.Timedelta(days=90):
            return 'Near-Cutoff'
        else:
            return 'Post-Cutoff'
            
    df['temporal_window'] = df['published_date'].apply(assign_window)
    
    print("\nInitial Pool Distribution:")
    print(df['temporal_window'].value_counts())
    
    # --- FORCE BALANCING TO 100 EACH ---
    try:
        df_pre = df[df['temporal_window'] == 'Pre-Cutoff'].sample(n=100, random_state=42)
        df_near = df[df['temporal_window'] == 'Near-Cutoff'].sample(n=100, random_state=42)
        df_post = df[df['temporal_window'] == 'Post-Cutoff'].sample(n=100, random_state=42)
        
        # Combine back into a perfectly balanced 300-paper dataset
        balanced_df = pd.concat([df_pre, df_near, df_post]).reset_index(drop=True)
        
        # Format date back to string
        balanced_df['published_date'] = balanced_df['published_date'].dt.strftime('%Y-%m-%d')
        
        output_path = "src/stratified_arxiv_dataset_4.csv"
        balanced_df.to_csv(output_path, index=False)
        
        print(f"\n[OK] Perfectly balanced dataset saved to {output_path} with distribution:")
        print(balanced_df['temporal_window'].value_counts())
        
    except ValueError as e:
        print(f"\n[FAIL] Could not balance dataset. Not enough papers in one of the windows: {e}")
        print("Try increasing max_results or changing the search query.")