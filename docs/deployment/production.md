# Production Deployment

- Use dedicated secrets manager (Vault/SOPS/K8s Secrets).
- Enforce TLS at ingress.
- Restrict outbound firewall from API service.
- Rotate JWT and API keys regularly.
- Backup Postgres volume and audit logs.
