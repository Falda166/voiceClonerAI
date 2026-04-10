# Security Policy

## Reporting
Please report vulnerabilities privately to project maintainers before public disclosure.

## Supported versions
`0.1.x` is currently supported.

## Security posture
- Passwords hashed using bcrypt.
- JWT auth for admin API.
- API key support for internal service calls.
- Audit logging for mutating endpoints.
- Secret redaction and no plaintext secret commits.
