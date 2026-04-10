# Threat Model

## Key risks
- Unauthorized mutation via stolen admin token.
- Prompt injection or malicious model output.
- Unsafe scanning across unauthorized subnets.
- openHAB credential leakage.

## Controls
- JWT auth, API key internal auth.
- Deterministic AI output validators.
- Scan scope restriction + safe plugin defaults.
- Audit logs and rollback snapshots.
