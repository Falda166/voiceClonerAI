#!/usr/bin/env bash
set -euo pipefail

cp -n .env.example .env || true
echo 'Bootstrap complete. Edit .env and run: docker compose -f docker-compose.dev.yml up --build'
