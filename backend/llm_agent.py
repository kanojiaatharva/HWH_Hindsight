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

async def diagnose_incident(current_incident: str, recalled_context: dict, memory_enabled: bool = True):
    """
    Diagnose an incident using LLM reasoning with optional Hindsight memory context.

    Args:
        current_incident: Description of the current incident
        recalled_context: Hindsight recall results with 'results' key
        memory_enabled: Whether memory context should influence the diagnosis
    """
    # Extract results from Hindsight API format
    results = recalled_context.get("results", [])

    if not GROQ_API_KEY:
        print("[LLM Mock] Groq API Key missing. Returning mock diagnosis.")
        if memory_enabled and len(results) > 0:
            # Return memory-aware mock response
            first_memory = results[0]
            return {
                "pattern_match": True,
                "confidence_score": 0.87,
                "similar_incidents": [
                    {
                        "id": first_memory.get("id", "INC-0047"),
                        "symptoms": "502 errors on prod-api with CPU spike",
                        "root_cause": first_memory.get("metadata", {}).get("root_cause", "connection pool exhaustion")
                    }
                ],
                "recommended_fix": "kubectl rollout restart deploy/sidecar-proxy -n prod\nkubectl scale deploy/auth-service --replicas=3 -n prod",
                "failed_approaches": ["Restarting nginx - symptoms return in 10 mins", "Scaling prod-api pods - bottleneck was upstream"],
                "root_cause_analysis": "Connection pool exhaustion in auth-service. Historical pattern indicates upstream bottleneck."
            }
        else:
            # Return generic mock response without memory
            return {
                "pattern_match": False,
                "confidence_score": 0.0,
                "similar_incidents": [],
                "recommended_fix": "Check application logs and metrics.\nInspect recent deployments.\nVerify service health and dependencies.",
                "failed_approaches": [],
                "root_cause_analysis": "Generic troubleshooting required. No historical context available."
            }

    client = AsyncGroq(api_key=GROQ_API_KEY)

    # Format memories for LLM context
    if memory_enabled and results:
        memories_formatted = []
        for result in results[:5]:  # Limit to top 5
            memory_text = result.get("text", "")
            metadata = result.get("metadata", {})
            score = result.get("scores", {}).get("final", 0.0)
            memories_formatted.append({
                "incident_id": metadata.get("incident_id", "unknown"),
                "content": memory_text,
                "relevance_score": score,
                "root_cause": metadata.get("root_cause", "unknown")
            })
        memories_str = json.dumps(memories_formatted, indent=2)
    else:
        memories_str = "No historical memories available or memory disabled."

    prompt = f"""CURRENT INCIDENT:
{current_incident}

MEMORY STATUS: {"ENABLED - Historical context available" if memory_enabled else "DISABLED - No historical context"}

RECALLED PAST EXPERIENCES (HINDSIGHT):
{memories_str}

Analyze the current incident. If historical memories are available and relevant, explicitly reference them and extract:
1. Previously failed approaches to AVOID
2. Previously successful approaches to RECOMMEND
3. Root cause patterns from similar incidents

If no relevant memories exist or memory is disabled, provide generic troubleshooting advice."""

    try:
        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Updated to available Groq model
            messages=[
                {"role": "system", "content": DIAGNOSIS_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3  # Lower temperature for more consistent output
        )

        result_json = response.choices[0].message.content
        diagnosis = json.loads(result_json)

        # Ensure all required fields are present
        diagnosis.setdefault("pattern_match", False)
        diagnosis.setdefault("confidence_score", 0.0)
        diagnosis.setdefault("similar_incidents", [])
        diagnosis.setdefault("recommended_fix", "Check logs and metrics")
        diagnosis.setdefault("failed_approaches", [])
        diagnosis.setdefault("root_cause_analysis", "Analysis pending")

        return diagnosis

    except Exception as e:
        print(f"LLM Error: {e}")
        return {
            "pattern_match": False,
            "confidence_score": 0.0,
            "similar_incidents": [],
            "recommended_fix": "Generic troubleshooting: Check logs and metrics.",
            "failed_approaches": [],
            "root_cause_analysis": f"Unable to diagnose due to LLM error: {str(e)}"
        }
