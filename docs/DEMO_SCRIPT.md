# Demo Script for Incident Déjà Vu

## Preparation
1. Ensure `backend` (uvicorn) and `frontend` (npm run dev) are running.
2. Open `http://localhost:3000`.
3. Click "Reset Demo" in the sidebar to ensure a clean state.

## Phase 1: The Problem (Memory OFF)
*Goal: Show what a generic AI response looks like.*
1. Point out the top toggle "Hindsight Memory" and click it to turn it **OFF**.
2. In the chat box, type: `"prod-api-3 is returning 502 errors. CPU is at 95%."`
3. Hit **Diagnose**.
4. *Script*: "Without Hindsight, the agent gives generic LLM advice. It tells us to check the logs, maybe restart the proxy. Standard stuff. This is what you get with ChatGPT."
5. Notice the UI explicitly states: "Memory is currently OFF. The agent will respond generically."

## Phase 2: The Magic (Memory ON)
*Goal: Show longitudinal learning and exact historical recall.*
1. Click the "Hindsight Memory" toggle to turn it **ON**.
2. The agent will re-diagnose automatically (or hit enter again).
3. *Script*: "Now we turn Hindsight on. The agent queries its memory and instantly finds INC-0047 from 15 days ago."
4. Highlight the **PATTERN MATCH** UI element showing high confidence.
5. Highlight the **DO NOT TRY** section.
6. *Script*: "Look at this. Because it remembers the past incident, it warns the engineer *not* to restart NGINX because 15 days ago, that only masked the symptoms for 10 minutes. It tells us the exact root cause: connection pool exhaustion."

## Phase 3: The Learning Loop (Correction)
*Goal: Show that the agent learns from mistakes via the retain API.*
1. Scroll down to the feedback section: "WAS THIS HELPFUL?"
2. In the correction box, type: `"Actually, this time the connection pool was fine, it was an expired SSL certificate on the internal load balancer."`
3. Click **Correct**.
4. *Script*: "The agent just called Hindsight's retain API. This correction is now a permanent memory. If this happens tomorrow, it will check the certs first."
5. Click **Reset Demo** to conclude.
