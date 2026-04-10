# Architecture Overview

## Components
1. **API service**: discovery orchestration, adapters, approvals, execution planning.
2. **Worker service**: background tasks (scheduler/long-running jobs placeholder).
3. **Frontend**: admin UI for discovery, review, approval, rollback visibility.
4. **PostgreSQL**: source of truth for state and audit records.
5. **Redis**: queue/cache/session support.
6. **openHAB**: external automation control plane via documented REST endpoints.
7. **HomeMatic**: integration domain through dedicated adapter abstraction.
8. **AI gateway**: local/remote HF model routing, never authoritative for mutations.

## Trust boundaries
- Browser ↔ API: JWT, CSRF not required for bearer-token-only approach.
- API ↔ openHAB/HomeMatic: outbound integration boundary with timeout/circuit policies.
- AI gateway ↔ deterministic validator: model output is advisory only.

## Safety model summary
- Dry-run is default.
- All mutating operations create audit entries.
- Execution plan must be approved before apply.
- Rollback snapshot captured before apply.
