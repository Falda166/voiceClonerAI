.PHONY: bootstrap test lint typecheck up down

bootstrap:
	python -m venv .venv || true
	. .venv/bin/activate && pip install -r backend/requirements.txt
	cd frontend && npm install

test:
	cd backend && pytest -q

lint:
	cd backend && ruff check app tests

typecheck:
	cd backend && mypy app

up:
	docker compose up --build

down:
	docker compose down -v
