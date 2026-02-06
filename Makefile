PYTHON := python3
PIP := pip
COMPOSE := docker-compose

.PHONY: setup test dev build lint spec-check

setup:
	$(PYTHON) -m venv .venv
	. .venv/bin/activate && $(PIP) install --upgrade pip && $(PIP) install -r requirements.txt

test:
	$(COMPOSE) run --rm app pytest -q

dev:
	$(COMPOSE) up app postgres redis weaviate

build:
	$(COMPOSE) build

lint:
	. .venv/bin/activate && ruff . && mypy .

spec-check:
	@echo "Spec check stub: ensure all code changes reference specs/ requirements"
	@grep -R "specs/" -n swarm skills || echo "Warning: no explicit spec references found yet."
