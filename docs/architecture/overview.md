# Architecture Overview

## Monorepo decision
A monorepo is used for coherent versioning across API, worker, UI, and docs. This reduces integration drift for safety-critical workflows (approval, rollback, audit).

## Service boundaries
- Backend API: orchestration and deterministic validation.
- Worker: asynchronous polling/execution jobs.
- Frontend: operator console.
- PostgreSQL: durable state.
- Redis: queue/cache.
- openHAB: automation runtime.

## Trust boundaries
- UI to API over authenticated HTTP.
- API to openHAB over tokenized HTTP.
- AI gateway output is untrusted and validated before proposal persistence.
- No direct model output to mutating actions.
