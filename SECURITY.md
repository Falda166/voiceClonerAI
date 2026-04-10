# Security Policy

## Supported Versions
Latest `main` is supported.

## Reporting a Vulnerability
Please open a private security advisory or contact maintainers with:
- impacted component,
- reproduction steps,
- expected risk.

## Security controls
- BCrypt password storage.
- JWT auth and admin authorization for privileged flows.
- Explicit approval gates for risky mutations.
- Structured audit logs with correlation IDs.
- Read-only mode and emergency stop flags.
