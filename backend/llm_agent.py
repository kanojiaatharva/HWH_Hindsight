import os
from groq import AsyncGroq
import json

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

DIAGNOSIS_SYSTEM_PROMPT = """You are an expert Incident Response Agent powered by Hindsight. 
Your goal is to diagnose production incidents by heavily relying on past recalled incidents (memories).
When similar past incidents are provided, point out the pattern match, suggest the root cause that was identified last time, and list the exact recommended fix.
CRITICAL: You must also explicitly list 'Failed Approaches' based on what didn't work in the past, to save the operator time.

Respond in JSON format with the following keys:
- pattern_match: boolean indicating if a strong match was found.
- confidence_score: float between 0.0 and 1.0.
- similar_incidents: list of dicts with 'id', 'symptoms', and 'root_cause'.
- recommended_fix: string explaining exactly what to do (can include CLI commands).
- failed_approaches: list of strings detailing what should NOT be tried.
- root_cause_analysis: brief explanation of the likely underlying issue.
"""

async def diagnose_incident(current_incident: str, recalled_memories: dict):
    if not GROQ_API_KEY:
        print("[LLM Mock] Groq API Key missing. Returning mock diagnosis.")
        return {
            "pattern_match": True,
            "confidence_score": 0.87,
            "similar_incidents": [{"id": "INC-0047", "symptoms": "502 errors", "root_cause": "connection pool exhaustion"}],
            "recommended_fix": "kubectl rollout restart deploy/sidecar-proxy -n prod",
            "failed_approaches": ["Restarting nginx - symptoms return in 10 mins"],
            "root_cause_analysis": "Connection pool exhaustion in auth-service."
        }

    client = AsyncGroq(api_key=GROQ_API_KEY)
    
    memories_str = json.dumps(recalled_memories.get("memories", []), indent=2)
    prompt = f"CURRENT INCIDENT:\n{current_incident}\n\nRECALLED PAST EXPERIENCES (HINDSIGHT):\n{memories_str}"

    try:
        response = await client.chat.completions.create(
            model="qwen-2.5-32b", # or "llama3-70b-8192", depending on available groq models
            messages=[
                {"role": "system", "content": DIAGNOSIS_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        result_json = response.choices[0].message.content
        return json.loads(result_json)
    except Exception as e:
        print(f"LLM Error: {e}")
        return {
            "pattern_match": False,
            "confidence_score": 0.0,
            "similar_incidents": [],
            "recommended_fix": "Generic troubleshooting: Check logs and metrics.",
            "failed_approaches": [],
            "root_cause_analysis": "Unable to diagnose due to LLM error."
        }
