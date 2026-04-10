.PHONY: bootstrap up up-dev test lint

bootstrap:
	./scripts/bootstrap.sh

up:
	docker compose up --build

up-dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

test:
	docker compose run --rm backend pytest

lint:
	docker compose run --rm backend python -m compileall app
