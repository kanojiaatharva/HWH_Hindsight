# Contributing to Incident Déjà Vu

Thank you for considering contributing to Incident Déjà Vu! This document outlines the process for contributing to this project.

## Development Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- Git

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kanojiaatharva/HWH_Hindsight.git
   cd HWH_Hindsight
   ```

2. **Backend setup:**
   ```bash
   cd backend
   python -m venv venv
   # Windows: .\venv\Scripts\Activate.ps1
   # Linux/Mac: source venv/bin/activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   cp .env.example .env
   # Add your API keys to .env
   ```

3. **Frontend setup:**
   ```bash
   cd frontend
   npm install
   ```

4. **Run both services:**
   ```bash
   # Terminal 1 - Backend
   cd backend && uvicorn main:app --reload --port 8000

   # Terminal 2 - Frontend
   cd frontend && npm run dev
   ```

   Or use Docker:
   ```bash
   docker compose up --build
   ```

## Code Quality

### Backend (Python)
- **Linting:** We use [Ruff](https://docs.astral.sh/ruff/) for linting and formatting.
  ```bash
  ruff check backend/
  ruff format backend/
  ```
- **Type Hints:** All functions should have type annotations.
- **Tests:** Run with `pytest`:
  ```bash
  cd backend && pytest tests/ -v
  ```

### Frontend (TypeScript/React)
- **Linting:** ESLint is configured.
  ```bash
  cd frontend && npm run lint
  ```

## Pull Request Process

1. **Fork** the repository and create a feature branch from `main`.
2. **Write tests** for any new functionality.
3. **Ensure all tests pass** before submitting.
4. **Update documentation** if your changes affect the public API or architecture.
5. **Submit a PR** with a clear description of the changes and their motivation.

## Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add memory retention for user corrections
fix: handle empty recall results gracefully
docs: update architecture diagram
test: add edge case tests for diagnosis endpoint
refactor: extract memory formatting into utility
```

## Architecture Overview

Before contributing, please read:
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — System design and memory lifecycle
- [`docs/PRD.md`](docs/PRD.md) — Product requirements and feature rationale

## Reporting Issues

When reporting bugs, please include:
- Steps to reproduce
- Expected vs. actual behavior
- Environment details (OS, Python version, Node version)
- Relevant log output

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). Please read it before participating.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
