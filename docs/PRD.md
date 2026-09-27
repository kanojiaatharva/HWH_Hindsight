# Incident Déjà Vu: Product Requirements Document

## 1. Product Vision
An AI incident response workspace that structurally improves over time by leveraging Hindsight to recall organizational memory, preventing engineers from repeating past mistakes during critical outages.

## 2. Target Persona
Site Reliability Engineers (SREs), DevOps Engineers, and on-call developers who diagnose production incidents under time pressure.

## 3. Core Problems
- Runbooks are static and often out-of-date.
- Institutional knowledge walks out the door when senior engineers leave.
- During outages, responders often try "quick fixes" (like restarting a pod) that temporarily mask symptoms but fail to resolve the root cause, extending Time To Resolution (TTR).

## 4. Why Memory is Essential (The Hindsight Advantage)
A standard LLM can suggest generic debugging steps (e.g., "check the logs"). Incident Déjà Vu uses Hindsight to recall *exactly* what happened the last time a specific microservice failed with a specific error pattern. Without Hindsight, the product devolves into a generic chatbot; with it, the product becomes an evolving, localized intelligence platform.

## 5. Key Features
1. **Context-Aware Diagnosis**: Combines active incident symptoms with Hindsight's recalled memories to find pattern matches.
2. **"Failed Approaches" Warning**: Specifically surfaces what *did not* work in the past, saving crucial debugging time.
3. **Memory ON/OFF Toggle**: Clearly demonstrates the value of historical context by allowing users to compare outputs.
4. **Correction Loop**: Allows engineers to submit feedback on a diagnosis, which is immediately retained in Hindsight for future incidents.
