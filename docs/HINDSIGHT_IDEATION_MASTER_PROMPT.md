# Hindsight Ideation Master Prompt

> **Purpose:** This is the authoritative instruction set for the IDEATION + RESEARCH PHASE of the Hindsight project. Treat every section as mandatory. Do not skip, summarize, or abbreviate any part.

---

You are now entering the **IDEATION + RESEARCH PHASE** of this project.

The repository root is the current workspace.

> [!CAUTION]
> **IMPORTANT:**
> - Do NOT start implementing the application yet.
> - Do NOT generate frontend/backend code.
> - Do NOT install dependencies.
> - Do NOT modify the existing application architecture.
> - Do NOT create random prototype files.

Your job right now is to **EXECUTE** the ideation process defined in this file.

Treat this file as the authoritative instruction set for this phase.

---

## STEP 1 — INSPECT THE ENTIRE REPOSITORY

First inspect the repository carefully.

Read and analyze:

- README files
- `package.json` / `pom.xml` / `requirements.txt` / configuration files
- Existing source code
- Existing documentation
- Existing architecture
- Existing UI/code if present
- Environment/configuration files
- All relevant files inside `/docs`

Also inspect the supplied PDFs in the repository, especially:

- **Hackathon Content Submission.pdf**
- **HackwithHyderabad 3.0 Problem Statement.pdf**

These documents are important inputs to the ideation process.

Understand the actual challenge, constraints, judging context, submission requirements, and the Hindsight-specific expectations before generating ideas.

**Do not assume the project idea yet.**

---

## STEP 2 — UNDERSTAND THE ACTUAL OPPORTUNITY

Determine:

1. What the HackwithHyderabad problem statement is actually asking for.
2. What constraints the challenge places on the solution.
3. What Hindsight contributes.
4. Where persistent agent memory can create genuinely new functionality.
5. Which parts of the challenge are suitable for a memory-first solution.
6. Which obvious/generic solutions should be avoided.
7. What could make a solution technically distinctive.

**Separate clearly:**

```
FACTS FROM THE DOCUMENTS
vs.
YOUR ENGINEERING INFERENCE
vs.
YOUR PROPOSED IDEAS.
```

**Do not invent facts that are not present in the supplied documents.**

---

## STEP 3 — EXECUTE THE MASTER IDEATION PROMPT

Now execute the **COMPLETE** process defined inside this file.

**Do not skip sections.**

In particular, perform:

- Opportunity analysis
- Problem analysis
- 20 project concepts
- Memory necessity test
- Technical novelty analysis
- Before/after memory analysis
- Real-world value analysis
- Buildability analysis
- Memory architecture analysis
- Memory lifecycle design
- Memory failure analysis
- UX analysis
- 30-second WOW test
- "Impossible without memory" test
- Technical architecture
- Data flow
- Database considerations
- API considerations
- Security considerations
- Evaluation strategy
- Demo strategy
- Naming
- Concept comparison
- Final concept selection
- Implementation roadmap

---

## STEP 4 — BE AGGRESSIVE ABOUT IDEA QUALITY

> [!WARNING]
> Do NOT settle for: *"an AI chatbot with Hindsight."*

**Reject ideas where:**

- Memory is decorative
- Memory only stores chat history
- RAG would solve the problem equally well
- A normal database would provide essentially the same value
- The idea is just CRUD + LLM
- The idea cannot demonstrate memory clearly
- The idea has no meaningful longitudinal interaction
- The idea depends on fake or unverifiable claims

**The final concept should preferably satisfy:**

```
MEMORY REMOVED
        ↓
CORE FUNCTIONALITY BREAKS OR DEGRADES SIGNIFICANTLY
```

The project should make it **obvious** why Hindsight exists in the architecture.

---

## STEP 5 — USE THE ACTUAL PROBLEM STATEMENT

**Do NOT generate ideas in isolation from the HackwithHyderabad challenge.**

For every serious candidate ask:

> *"How directly does this solve the actual challenge?"*

Then ask:

> *"Where does persistent memory create an advantage that a conventional AI implementation would not have?"*

**Look for opportunities involving:**

- Repeated interactions
- Long-term user context
- Historical decisions
- Evolving preferences
- Accumulated experience
- Institutional knowledge
- Recurring workflows
- Previous failures
- Personalized strategies
- Longitudinal analysis
- Multi-session agents
- Human-agent collaboration
- Learning from previous interactions
- Memory-driven decisions

**But only use these when they fit the actual problem.**

---

## STEP 6 — CREATE THE FINAL ANALYSIS DOCUMENT

After completing the analysis, create:

```
/docs/IDEATION_ANALYSIS.md
```

This document should contain the **complete result** of your analysis.

**Use this structure:**

```markdown
# Hindsight Project Ideation Analysis

## 1. Repository Analysis

## 2. Hackathon Problem Analysis

## 3. Hindsight Opportunity

## 4. Constraints

## 5. Problems Worth Solving

## 6. 20 Candidate Concepts

## 7. Memory Necessity Analysis

## 8. Technical Novelty Analysis

## 9. Demo Potential

## 10. Buildability Analysis

## 11. Top 5 Concepts

## 12. Detailed Tradeoff Analysis

## 13. Selected Concept

## 14. Why Memory Is Essential

## 15. Before vs After Memory

## 16. Impossible Without Memory Moment

## 17. Core User Journey

## 18. Memory Lifecycle

## 19. Memory Failure Scenarios

## 20. High-Level Architecture

## 21. Data Flow

## 22. Security Considerations

## 23. MVP Scope

## 24. Future Scope

## 25. Evaluation Strategy

## 26. 3-Minute Demo Plan

## 27. Project Naming

## 28. One-Line Pitch

## 29. One-Minute Pitch

## 30. Implementation Roadmap

## 31. Open Questions
```

---

## STEP 7 — DO NOT WRITE IMPLEMENTATION CODE

At this stage you may define:

- Components
- Technologies
- APIs
- Database entities
- Memory mechanisms
- Architecture
- Repository structure
- Implementation phases

> [!CAUTION]
> But **DO NOT** actually implement them.
>
> - No React components.
> - No Spring controllers.
> - No Python services.
> - No database migrations.
> - No API endpoints.
> - No Docker setup.
> - No deployment.
>
> **This is still the planning phase.**

---

## STEP 8 — FINAL QUALITY CHECK

Before finishing, verify:

- [ ] The idea directly relates to the actual challenge.
- [ ] Hindsight is functionally important.
- [ ] Memory is not just chat history.
- [ ] The concept has a clear before/after-memory demonstration.
- [ ] The project is technically interesting.
- [ ] The MVP is realistically buildable.
- [ ] The architecture is not unnecessarily complicated.
- [ ] Security/privacy risks have been considered.
- [ ] No unsupported statistics or fabricated results were introduced.
- [ ] The final idea can be explained in one sentence.
- [ ] The 3-minute demo clearly demonstrates the value of memory.
- [ ] The analysis is stored in `/docs/IDEATION_ANALYSIS.md`.

---

## FINAL BEHAVIOR

When finished:

1. **Save** the complete analysis to:
   ```
   /docs/IDEATION_ANALYSIS.md
   ```

2. **Do NOT** start implementation.

3. In your final response, provide **only**:
   - The selected concept
   - A 2–4 paragraph explanation of why it was selected
   - The core role of Hindsight
   - The central demo moment
   - The main technical challenge
   - The path to the analysis document

4. Then **STOP**.

> [!IMPORTANT]
> **WAIT FOR MY APPROVAL BEFORE WRITING ANY APPLICATION CODE.**