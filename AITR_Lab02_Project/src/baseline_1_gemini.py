import json
import re
import os
import urllib.request
import urllib.error

def setup_gemini():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    return api_key

def format_abstracts(df_batch):
    context = ""
    for _, row in df_batch.iterrows():
        context += f"ID: {row['paper_id']} | Abstract: {row['abstract']}\n\n"
    return context.strip()

def _call_gemini_rest(api_key, prompt):
    # Switched to the faster 3.5-flash-lite model to prevent read timeouts
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
    
    try:
        # Bumped timeout to 120 seconds
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['candidates'][0]['content']['parts'][0]['text']
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        raise RuntimeError(f"HTTP {e.code}: {error_body}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e.reason}")

def generate_naive_rag_synthesis(api_key, formatted_abstracts):
    prompt = f"""You are an expert academic researcher writing a literature review. 
Below are the abstracts of several recent scientific papers. 

<abstracts>
{formatted_abstracts}
</abstracts>

Based ONLY on the provided abstracts, write a concise synthesis (200-300 words). Include:
1. Current State of the Art: Established methods and consensus.
2. Open Problems: Specific unsolved challenges. 
Cite papers inline using their IDs."""
    
    return _call_gemini_rest(api_key, prompt)

def evaluate_with_llm_judge(api_key, formatted_abstracts, synthesis_text):
    prompt = f"""You are an objective academic evaluator. 

Source Abstracts:
{formatted_abstracts}

Generated Synthesis:
{synthesis_text}

Evaluate the synthesis. Output ONLY JSON format matching this exact structure:
{{
  "omission_score": <float 0.0 to 1.0>,
  "omission_reasoning": "<string>",
  "stale_framing": <int 1 if stale/hallucinated, 0 if accurate>,
  "stale_framing_reasoning": "<string>"
}}"""

    response_text = _call_gemini_rest(api_key, prompt)
    
    match = re.search(r'\{.*\}', response_text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
            
    return {
        "omission_score": None,
        "omission_reasoning": f"Failed to parse JSON. Raw: {response_text}",
        "stale_framing": None,
        "stale_framing_reasoning": "Failed to parse JSON."
    }