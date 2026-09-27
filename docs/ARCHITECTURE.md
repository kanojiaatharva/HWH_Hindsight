# Architecture & Memory Model

## System Overview
The system relies on a clean separation between the user interface, the API gateway, the LLM reasoning layer, and the memory storage layer.

1. **Frontend (Next.js)**: A React-based SPA that provides the Incident Workspace. It handles state for the active incident and communicates via REST.
2. **API (FastAPI)**: A Python backend that orchestrates the flow.
3. **Agent Orchestrator (Groq)**: Analyzes the current symptoms against retrieved memories.
4. **Memory Layer (Hindsight Cloud)**: The source of truth for historical incident experiences.

## Memory Lifecycle
1. **Creation (Retain)**: When an incident is resolved (or when user feedback is provided), a structured `ResolvedIncident` payload is transformed into a narrative string and pushed to Hindsight's `/retain` API.
2. **Retrieval (Recall)**: When a new incident occurs, the symptoms are sent to Hindsight's `/recall` API.
3. **Application**: The LLM combines the current symptoms and the recalled memories to determine the root cause, using the historical metadata to explicitly formulate a "Failed Approaches" list.

## Data Model (Pydantic)
- `IncidentReport`: Contains the live symptoms and a `memory_enabled` flag.
- `ResolvedIncident`: Contains `root_cause`, `resolution_steps`, and `failed_approaches`. This is what is passed to Hindsight.
- `IncidentFeedback`: Contains user corrections to be retained as new learning.

## Fallback Mechanism
If the `HINDSIGHT_API_KEY` is not present, the `HindsightClient` gracefully falls back to an in-memory string-matching array. This ensures the demo never crashes due to environment configuration issues during a live presentation.
