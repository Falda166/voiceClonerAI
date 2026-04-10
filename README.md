# OpenAutoHAB AI

OpenAutoHAB AI is a self-hostable orchestration platform that safely bootstraps and manages openHAB automation using deterministic logic plus optional AI assistance.

## What you get

- Network discovery jobs with strict CIDR limits and dry-run support.
- Device inventory with confidence scoring and deduplication keying.
- Recommendation engine for openHAB mappings (Thing/Item suggestions).
- Approval workflow before any risky mutation.
- Execution plans with preflight, snapshot, verification, and rollback metadata.
- openHAB adapter abstraction plus HomeMatic normalization abstraction.
- Structured audit logging, correlation IDs, and Prometheus metrics.
- Fully local Docker Compose stack (Postgres, Redis, API, Worker, UI, openHAB).

## Architecture

Monorepo layout (single repo, multi-service):

- `backend/` FastAPI orchestration API, deterministic validation, adapters, audit and auth.
- `worker/` async job poller/executor process.
- `frontend/` Angular operational UI.
- `docs/` ADRs, architecture, deployment, security, user guides.
- `.github/` CI and contribution templates.

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

Open:

- UI: http://localhost:8080
- API: http://localhost:8000/api/v1/health
- Metrics: http://localhost:8000/metrics
- openHAB: http://localhost:18080

Default admin credentials (development only): `admin / admin123!`.

## Safety defaults

- Discovery is explicit and CIDR-bounded.
- Dry-run is default for mutating actions.
- Emergency stop and read-only flags are available.
- AI output is treated as untrusted; mutations require deterministic validation and explicit approval.

## Developer workflow

```bash
make bootstrap
make test
make lint
```

See `docs/` for architecture, threat model, and release checklist.
