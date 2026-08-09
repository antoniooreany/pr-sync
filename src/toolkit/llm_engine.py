import json
import os
import urllib.request
import urllib.error
from typing import Optional

def generate_smart_pr_summary(diff: str, commits: list[str]) -> Optional[str]:
    """Uses Gemini API to generate a smart summary and risk analysis."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    prompt = f"""You are an expert software engineer reviewing a pull request.
Based on the following commits and git diff, generate a concise and meaningful PR description.
Do NOT just list the commits. Group the changes logically into features, bug fixes, and chores.
Analyze the risks based on the files changed.

Commits:
{chr(10).join(commits)}

Diff:
{diff[:4000]}  # limit diff length to avoid token limits

Respond with ONLY the markdown content for these two sections:
## Smart Summary
<your logical grouping of changes>

## Risk Analysis
<your assessment of risks>
"""
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.2
        }
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        # Fallback gracefully
        print(f"Gemini API Error: {e}")
        return None

