# Contributing

## Branching
- Use feature branches from `main`.
- Keep commits focused and atomic.

## Local checks
Run before opening PR:

```bash
make test
make lint
```

## Coding standards
- Python: strict typing for new modules.
- No silent side effects for mutating endpoints.
- Every risky action must support dry-run and audit traces.

## Pull request requirements
- Include risk analysis and rollback implications.
- Include screenshots for UI-impacting changes.
- Update docs for behavior changes.
