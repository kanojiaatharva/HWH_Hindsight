# Incident Déjà Vu

An AI incident responder that learns from every outage, turning yesterday's failed approaches into today's immediate fixes.

## Problem
When production breaks, on-call engineers often waste critical minutes trying the same "quick fixes" (like restarting a proxy) that their colleagues tried during a similar incident months ago, only to find they don't solve the root cause. Traditional runbooks get stale, and normal RAG chatbots just recite those stale runbooks.

## Solution
Incident Déjà Vu is a memory-first incident response agent built on Hindsight. It doesn't just read documentation; it remembers what actually worked (and what failed) during past incidents. When a new incident looks similar to a past one, it recalls the exact root cause and specifically warns the engineer against trying approaches that failed last time.

## Why Hindsight is Essential
Without Hindsight, this is just a stateless chatbot that suggests generic troubleshooting steps. With Hindsight, it becomes a longitudinal learning system. It retains the experience of every resolved incident, meaning the agent's advice is structurally transformed by the historical context of the specific organization it serves.

## Architecture & Memory Lifecycle
1. **Understand**: The agent receives symptoms (e.g., "502 errors on prod-api").
2. **Recall**: It queries Hindsight for semantically similar past incidents.
3. **Reason**: The LLM (powered by Groq) combines the live symptoms with the recalled experiences to deduce the pattern match.
4. **Act**: The UI presents the root cause and a recommended fix, importantly highlighting **Failed Approaches** to avoid.
5. **Retain**: If the user corrects the agent, the feedback is sent back through the `retain` API, permanently updating the agent's memory.

## Tech Stack
- **Frontend**: Next.js (React), TailwindCSS, Lucide Icons.
- **Backend**: FastAPI, Python.
- **Memory**: Hindsight Cloud API (via Python HTTP Client).
- **Intelligence**: Groq (Qwen-2.5-32b or Llama-3-70b).

## Setup & Running

**1. Clone and Env Setup**
```bash
cd backend
python -m venv venv
# Activate venv: source venv/bin/activate (Linux/Mac) or .\venv\Scripts\Activate.ps1 (Windows)
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add GROQ_API_KEY and HINDSIGHT_API_KEY
```

**2. Start Backend**
```bash
cd backend
uvicorn main:app --reload
```

**3. Start Frontend**
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000` to access the Incident Workspace.

## Demo Flow
Open the UI and toggle "Hindsight Memory" to see the difference between a stateless response and a memory-aware response.
Run the Judge Demo by clicking "Reset Demo" and typing a symptom like "prod-api returning 502 errors" to see it instantly recall a past memory (INC-0047).

## Testing
Run backend tests with:
```bash
cd backend
pytest tests/
```
