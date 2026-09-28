# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | ✅ Current release |

## Reporting a Vulnerability

If you discover a security vulnerability in Incident Déjà Vu, please report it responsibly.

**Do NOT open a public GitHub issue for security vulnerabilities.**

Instead, please email the maintainers directly or use GitHub's private vulnerability reporting feature.

## Security Design Principles

Incident Déjà Vu processes production incident data, which can contain sensitive operational information. The following security measures are implemented:

### 1. Data Sanitization
All incident data is sanitized before retention in Hindsight memory:
- API keys and tokens are redacted (`***REDACTED***`)
- Internal IP addresses are masked (`***IP_REDACTED***`)
- Bearer tokens are stripped
- See [`hindsight_client.py`](backend/hindsight_client.py) — `_sanitize_content()` method

### 2. Environment Variables
- Sensitive credentials (API keys) are stored in `.env` files, **never committed to version control**
- `.env.example` provides a template without real values
- The `.gitignore` explicitly excludes all `.env*` files

### 3. API Security
- CORS is configured for cross-origin requests (configurable per deployment)
- The Hindsight API key is transmitted via `Authorization: Bearer` header over HTTPS
- No user authentication is implemented in the MVP (intended for internal/demo use)

### 4. Graceful Degradation
- If API keys are missing, the system falls back to local in-memory mode
- No data is transmitted to external services without valid credentials
- All external API calls are wrapped in error handlers with safe fallbacks

### 5. Dependency Management
- All dependencies are pinned to specific versions in `requirements.txt`
- No known CVEs in the current dependency set (as of last audit)

## Recommendations for Production Deployment

If deploying beyond demo/hackathon use:

1. **Add authentication** — Implement JWT-based auth for the API endpoints
2. **Restrict CORS** — Replace `allow_origins=["*"]` with specific frontend origin
3. **Enable HTTPS** — Deploy behind a TLS-terminating reverse proxy
4. **Audit logging** — Log all retain/recall operations for compliance
5. **Rate limiting** — Add rate limiting on the `/api/diagnose` endpoint
6. **Network isolation** — Run the backend in a private subnet with frontend-only public access
