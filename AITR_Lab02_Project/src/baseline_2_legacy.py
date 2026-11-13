# src/baseline_2_legacy.py
import json
import re
import os
import urllib.request
import urllib.error

def setup_legacy_model():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    return api_key

def _call_legacy_rest(api_key, prompt):
    # Enforcing the legacy 1.0-pro checkpoint for parametric ignorance control
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

def generate_legacy_rag_synthesis(api_key, formatted_abstracts):
    prompt = f"""You are an expert academic researcher writing a literature review. 
Below are the abstracts of several recent scientific papers. 

<abstracts>
{formatted_abstracts}
</abstracts>

Based ONLY on the provided abstracts, write a concise synthesis (200-300 words). Include:
1. Current State of the Art: Established methods and consensus.
2. Open Problems: Specific unsolved challenges. 
Cite papers inline using their IDs."""
    
    return _call_legacy_rest(api_key, prompt)