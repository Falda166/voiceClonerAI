# OpenAutoHAB AI Product Specification (MVP)

## Personas
- Home lab operator (self-hosting admin)
- Integrator/installer
- Security-conscious reviewer

## Main use cases
- Discover compatible devices and bridges.
- Propose openHAB mappings.
- Require approvals before changes.
- Execute with rollback snapshots.

## Non-goals (MVP)
- Zero-touch autonomous writing without approvals.
- Deep vendor-private API reverse engineering.
- Cloud-only model dependence.

## Assumptions
- openHAB is reachable over network.
- Operators own scan target networks.
- Some devices will be ambiguous or partially discoverable.

## Failure and recovery assumptions
- openHAB/HomeMatic can be offline.
- AI providers can fail or timeout.
- Recovery through retries, dry-run, rollback snapshot, and operator-driven reapply.

## Deployment models
- Local Docker Compose (supported now)
- Remote/Kubernetes (documented target, not default)

## Requirements snapshots
- OS: Linux/macOS/WSL2 for self-hosting.
- Browser: latest Chromium/Firefox/Safari.
- Hardware minimum: 2 vCPU / 4GB RAM, recommended 4 vCPU / 8GB.
- Optional acceleration: NVIDIA GPU for local inference roadmap.

## Entity definitions (implemented subset)
- Device: normalized discovered endpoint candidate.
- DiscoveryResult: represented via discovery job findings and persisted devices.
- Fingerprint: metadata_json + confidence score fields.
- Recommendation: structured proposal with confidence + validator_status.
- Approval: explicit approve/reject gate.
- ExecutionPlan: grouped steps with dry_run + status.
- RollbackSnapshot: pre-change capture per plan.
- AuditLog: immutable event record.
- OpenHAB artifact: represented as recommendation payload target.
- HomeMatic bridge/device: represented via adapter response normalization.
- AI request/response: AIProposal dataclass.

## Naming conventions
- Python modules: snake_case.
- API paths: kebab-less, versioned `/api/v1/...`.
- ENV vars: `OAH_` prefix.

## Security conventions
- No plaintext secrets in git.
- JWT for admin auth, API key for internal traffic.
- log entries must not include secret material.

## Compatibility strategy
- Adapter abstraction isolates openHAB/HomeMatic/HF provider drift.
- Experimental features must be behind flags.
