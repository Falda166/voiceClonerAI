# Threat Model

## Assets
- openHAB configuration state
- credentials/tokens
- audit logs
- rollback snapshots

## Threats
- Unauthorized configuration mutation
- Prompt injection into model outputs
- Secret leakage in logs
- Over-broad network scan scope

## Mitigations
- Admin auth required for high-risk endpoints
- Dry-run and explicit approval gates
- Deterministic validation of AI outputs
- Correlation IDs + audit trail
- CIDR scan scope hard limits
