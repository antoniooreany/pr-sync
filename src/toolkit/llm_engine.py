import json
import os
import urllib.request
import urllib.error
from typing import Optional

def _get_best_gemini_model(api_key: str) -> str:
    """Query the API to find an available flash model."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        req = urllib.request.Request(url, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=15.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            
            # Prefer flash models
            for model in data.get("models", []):
                name = model.get("name", "")
                methods = model.get("supportedGenerationMethods", [])
                if "generateContent" in methods and "flash" in name and "vision" not in name:
                    return name
                    
            # Fallback to pro
            for model in data.get("models", []):
                name = model.get("name", "")
                methods = model.get("supportedGenerationMethods", [])
                if "generateContent" in methods and "pro" in name and "vision" not in name:
                    return name
                    
    except Exception as e:
        print(f"Failed to list Gemini models: {e}")
        
    return "models/gemini-1.5-flash"  # absolute fallback

def generate_smart_pr_summary(diff: str, commits: list[str]) -> Optional[str]:
    """Uses Gemini API to generate a smart summary and risk analysis."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
        
    model_name = _get_best_gemini_model(api_key)
    # model_name already contains 'models/' prefix
    url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={api_key}"
    
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
    except urllib.error.HTTPError as e:
        print(f"Gemini API Error: {e}")
        try:
            print(f"Response body: {e.read().decode('utf-8')}")
        except:
            pass
        return None
    except Exception as e:
        # Fallback gracefully
        print(f"Gemini API Error: {e}")
        return None

