import os
import httpx
from models import ResolvedIncident
import json
from datetime import datetime
from typing import Optional, List, Dict

class HindsightClient:
    def __init__(self):
        self.api_key = os.getenv("HINDSIGHT_API_KEY")
        self.base_url = "https://api.hindsight.vectorize.io/v1/default"
        self.bank_id = os.getenv("HINDSIGHT_BANK_ID", "default")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        } if self.api_key else {}

        # In-memory fallback for local development if no API key is provided
        self.local_memories = []
        self._seed_demo_memories()

    def _seed_demo_memories(self):
        """Pre-seed demo memories for immediate recall during judge demo."""
        demo_incidents = [
            {
                "content": "Incident INC-0047: prod-api-3 returning 502 errors with CPU at 95%. "
                          "Root cause was connection pool exhaustion in auth-service v2.3.1 due to memory leak. "
                          "Resolution: kubectl rollout restart deploy/sidecar-proxy -n prod, then kubectl scale deploy/auth-service --replicas=3 -n prod. "
                          "Time to resolve: 4 minutes. "
                          "Failed approaches: Restarting nginx (symptoms returned in 10 minutes), Scaling prod-api pods (bottleneck was upstream).",
                "metadata": {
                    "incident_id": "INC-0047",
                    "type": "resolved_incident",
                    "services": ["prod-api", "auth-service"],
                    "severity": "High",
                    "root_cause": "Connection pool exhaustion in auth-service"
                }
            },
            {
                "content": "Incident INC-0051: Payment service latency spiked to 5000ms after Friday deploy. "
                          "Root cause was bad database migration that locked transactions table. "
                          "Resolution: Rollback deployment to v1.42, manually kill stuck db connections. "
                          "Time to resolve: 12 minutes. "
                          "Failed approaches: Scaling payment pods (database was the bottleneck, not compute).",
                "metadata": {
                    "incident_id": "INC-0051",
                    "type": "resolved_incident",
                    "services": ["payment-service"],
                    "severity": "Critical",
                    "root_cause": "Bad database migration"
                }
            },
            {
                "content": "Incident INC-0058: Intermittent 504 timeouts on checkout-service. "
                          "Root cause was pod memory limits too low causing OOM kills. "
                          "Resolution: Increased memory limits from 512Mi to 1Gi in Helm chart. "
                          "Time to resolve: 8 minutes. "
                          "Failed approaches: Restarting pod only (temporarily fixed until OOM hit again).",
                "metadata": {
                    "incident_id": "INC-0058",
                    "type": "resolved_incident",
                    "services": ["checkout-service", "cart-service"],
                    "severity": "High",
                    "root_cause": "Pod memory limits too low"
                }
            }
        ]
        self.local_memories = demo_incidents

    def _sanitize_content(self, content: str) -> str:
        """Remove sensitive data from content before retention."""
        import re
        # Remove potential API keys, tokens, passwords
        patterns = [
            (r'(?i)(api[_-]?key|token|password|secret)["\s:=]+["\']?[\w\-\.]+', r'\1=***REDACTED***'),
            (r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', r'***IP_REDACTED***'),
            (r'Bearer\s+[\w\-\.]+', r'Bearer ***REDACTED***'),
        ]
        sanitized = content
        for pattern, replacement in patterns:
            sanitized = re.sub(pattern, replacement, sanitized)
        return sanitized

    async def retain(self, incident: ResolvedIncident, tags: Optional[List[str]] = None):
        """
        Store a resolved incident as a retrievable memory in Hindsight.
        Uses the correct /v1/default/banks/{bank_id}/memories endpoint.
        """
        # Convert structured incident into narrative format for better recall quality
        memory_content = (
            f"Incident {incident.id}: {incident.root_cause}. "
            f"Resolution steps: {'; '.join(incident.resolution_steps)}. "
            f"Time to resolve: {incident.time_to_resolve_mins} minutes. "
            f"Failed approaches: {'; '.join(incident.failed_approaches) if incident.failed_approaches else 'None documented'}."
        )

        # Sanitize before storing
        sanitized_content = self._sanitize_content(memory_content)

        payload = {
            "items": [
                {
                    "content": sanitized_content,
                    "timestamp": datetime.now().isoformat(),
                    "metadata": {
                        "incident_id": incident.id,
                        "type": "resolved_incident",
                        "time_to_resolve_mins": incident.time_to_resolve_mins,
                        "root_cause": incident.root_cause
                    },
                    "tags": tags or ["incident", "production"],
                    "entities": [
                        {"text": incident.id, "type": "CONCEPT"}
                    ]
                }
            ]
        }

        if not self.api_key:
            print(f"[Hindsight Mock] Retained memory locally: {incident.id}")
            self.local_memories.append({
                "content": sanitized_content,
                "metadata": payload["items"][0]["metadata"]
            })
            return {"success": True, "mock": True, "bank_id": "mock", "items_count": 1}

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                url = f"{self.base_url}/banks/{self.bank_id}/memories"
                response = await client.post(
                    url,
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                print(f"[Hindsight] Successfully retained incident {incident.id}")
                return response.json()
            except httpx.HTTPStatusError as e:
                print(f"[Hindsight] HTTP error during retain: {e.response.status_code} - {e.response.text}")
                # Fallback to local
                self.local_memories.append({
                    "content": sanitized_content,
                    "metadata": payload["items"][0]["metadata"]
                })
                return {"success": False, "error": str(e), "fallback_used": True}
            except Exception as e:
                print(f"[Hindsight] Error during retain: {e}")
                self.local_memories.append({
                    "content": sanitized_content,
                    "metadata": payload["items"][0]["metadata"]
                })
                return {"success": False, "error": str(e), "fallback_used": True}

    async def recall(self, query: str, max_results: int = 3, tags: Optional[List[str]] = None) -> Dict:
        """
        Retrieve relevant past incidents using Hindsight's recall API.
        Uses the correct /v1/default/banks/{bank_id}/memories/recall endpoint.
        """
        payload = {
            "query": query[:500],  # Max 500 tokens
            "types": ["world", "experience"],
            "budget": "mid",
            "max_tokens": 4096,
        }

        if tags:
            payload["tags"] = tags
            payload["tags_match"] = "any"

        if not self.api_key:
            print(f"[Hindsight Mock] Recalling from local memory for: '{query[:50]}...'")
            # Simple keyword matching for the mock
            results = []
            query_words = set(query.lower().split())

            for mem in self.local_memories:
                content_words = set(mem['content'].lower().split())
                # Calculate simple relevance score
                overlap = len(query_words & content_words)
                if overlap > 0:
                    results.append({
                        "text": mem['content'],
                        "metadata": mem.get('metadata', {}),
                        "scores": {"final": 0.85 - (len(results) * 0.1)},
                        "type": "experience",
                        "id": mem['metadata'].get('incident_id', 'unknown')
                    })

            # Sort by overlap and limit results
            results = sorted(results, key=lambda x: x['scores']['final'], reverse=True)[:max_results]
            return {"results": results, "mock": True}

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                url = f"{self.base_url}/banks/{self.bank_id}/memories/recall"
                response = await client.post(
                    url,
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                print(f"[Hindsight] Recalled {len(data.get('results', []))} memories")
                return data
            except httpx.HTTPStatusError as e:
                print(f"[Hindsight] HTTP error during recall: {e.response.status_code} - {e.response.text}")
                return {"results": [], "error": str(e), "fallback_used": True}
            except Exception as e:
                print(f"[Hindsight] Error during recall: {e}")
                return {"results": [], "error": str(e), "fallback_used": True}
