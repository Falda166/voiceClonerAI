# Local deployment

1. `cp .env.example .env`
2. `docker compose up --build`
3. Open `http://localhost:8080`

## Network requirements
- API: 8000
- UI: 8080
- openHAB: 18080

## Privileges
Run with standard Docker privileges; do not run containers as root in production.
