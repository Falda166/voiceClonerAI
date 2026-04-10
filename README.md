# OpenAutoHAB AI

OpenAutoHAB AI is a self-hostable orchestration platform for safe AI-assisted openHAB bootstrap with HomeMatic integration.

## Why monorepo
This project uses a **monorepo** to keep backend, frontend, deployment, and architecture docs versioned together for deterministic releases and reproducible local demos.

## Quick start
```bash
cp .env.example .env
docker compose up --build
```

- UI: http://localhost:8080
- API: http://localhost:8080/api/v1/health

Default admin login (dev only):
- `admin` / `admin123`

## Core safety controls
- Global dry-run defaults.
- Explicit approval entities before execution.
- Audit logs for every write.
- Rollback snapshot generated per execution plan.
- AI output is structured + validated before persistence.

## Repo layout
- `backend/` FastAPI orchestration API + adapters + validation.
- `frontend/` Angular operations UI.
- `docs/` architecture, ADRs, threat model, deployment, user docs.
- `deploy/` reverse proxy configuration.
- `scripts/` bootstrap and seed utilities.

## Local demo flow
1. Login in UI.
2. Run discovery job for your local CIDR (safe plugin mode).
3. Load discovered devices.
4. Generate recommendation for a device through API.
5. Create approval and execute plan.

See `docs/user/first-deployment.md` for detailed walkthrough.
