# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] — 2026-09-28

### Added
- **Core memory-powered incident diagnosis** with Hindsight `retain` and `recall` APIs
- **Failed Approaches Warning** — surfaces past failed fixes to prevent repeated mistakes
- **Memory ON/OFF toggle** — clearly demonstrates Hindsight's value in the UI
- **Correction/Feedback loop** — user corrections are retained as new memories via the `retain` API
- **Graceful degradation** — in-memory fallback when API keys are not configured
- **Data sanitization pipeline** — redacts API keys, tokens, and IP addresses before memory retention
- **Docker Compose setup** — one-command deployment of both frontend and backend
- **CI/CD pipeline** — GitHub Actions for automated testing and linting
- **Comprehensive test suite** — API endpoint tests, memory lifecycle tests, edge case coverage

### Architecture
- **Frontend**: Next.js 16 with React 19, TailwindCSS, Lucide Icons
- **Backend**: FastAPI with async Python, Pydantic v2 models
- **Memory Layer**: Hindsight Cloud API via custom async HTTP client
- **LLM Reasoning**: Groq (Llama-3.3-70b-versatile) with structured JSON output
- **Orchestration**: PM2 ecosystem for local development, Docker Compose for deployment

## [0.2.0] — 2026-09-27

### Added
- PM2 process management with `ecosystem.config.cjs`
- Backend start script (`start.cjs`) for PM2 integration
- Seed data with 4 realistic incident records (3 resolved + 1 active)

### Fixed
- Groq model updated to `llama-3.3-70b-versatile` (available model)
- Memory recall keyword matching improved for demo reliability

## [0.1.0] — 2026-09-26

### Added
- Initial FastAPI backend with `/api/diagnose`, `/api/feedback`, `/api/incidents` endpoints
- Next.js frontend with dark-themed Incident Workspace UI
- Hindsight client with `retain()` and `recall()` methods
- Mock/fallback mode for offline development
- Basic test suite with 4 tests
- Architecture documentation and PRD
- Demo script for judge presentation

### Research
- Completed full ideation analysis (66K-word document in `docs/IDEATION_ANALYSIS.md`)
- Evaluated 20 candidate concepts for memory-first applications
- Selected "Incident Déjà Vu" as the strongest use of persistent agent memory
