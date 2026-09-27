import os
import httpx
from models import ResolvedIncident
import json

class HindsightClient:
    def __init__(self):
        self.api_key = os.getenv("HINDSIGHT_API_KEY")
        self.base_url = "https://api.hindsight.vectorize.io/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # In-memory fallback for local development if no API key is provided
        self.local_memories = []

    async def retain(self, incident: ResolvedIncident):
        """
        Store a resolved incident as a retrievable memory in Hindsight.
        """
        # We convert the structured data into a narrative format to improve recall quality
        memory_content = (
            f"Incident ID {incident.id}: {incident.root_cause}. "
            f"Resolution involved: {', '.join(incident.resolution_steps)}. "
            f"Failed approaches: {', '.join(incident.failed_approaches)}."
        )
        
        payload = {
            "content": memory_content,
            "metadata": {
                "incident_id": incident.id,
                "type": "resolved_incident"
            }
        }
        
        if not self.api_key:
            print("[Hindsight Mock] Retained memory locally.")
            self.local_memories.append(payload)
            return {"status": "success", "mock": True}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/retain", 
                    headers=self.headers, 
                    json=payload
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"Hindsight API error: {e}")
                # Fallback
                self.local_memories.append(payload)
                return {"status": "error_fallback_used"}

    async def recall(self, query: str):
        """
        Retrieve relevant past incidents and observations based on the query.
        """
        payload = {
            "query": query,
            "top_k": 3,
            "namespace": "incidents"
        }
        
        if not self.api_key:
            print("[Hindsight Mock] Recalled from local memory.")
            # Simple keyword matching for the mock
            results = []
            for mem in self.local_memories:
                if any(word in mem['content'].lower() for word in query.lower().split()):
                    results.append({"content": mem['content'], "metadata": mem['metadata'], "similarity": 0.85})
            return {"memories": results[:3], "mock": True}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/recall", 
                    headers=self.headers, 
                    json=payload
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"Hindsight API error: {e}")
                return {"memories": [], "error": str(e)}
