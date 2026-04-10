# API Notes

Base path: `/api/v1`

Core endpoints:
- `POST /auth/login`
- `POST /discovery/jobs`
- `GET /devices`
- `POST /recommendations/{device_uid}`
- `POST /approvals`
- `POST /execution/plans`
- `POST /execution/plans/{id}/run`
- `GET /audit-logs`

OpenAPI is served by FastAPI at `/docs` and `/openapi.json`.
