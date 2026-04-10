# Contributing

## Standards
- Keep deterministic validation in place for all AI-assisted mutations.
- Every write path must remain audit logged.
- Avoid undocumented third-party APIs.

## Development
```bash
make bootstrap
make up-dev
make test
```

## Branching and PR
- Feature branches from `main`.
- Add/update ADR when changing architecture boundaries.
- Include security impact section in PR description.
