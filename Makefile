# One target for the agent hook, pre-commit and CI: `make check`.
.PHONY: check lint types test fmt run mlflow overlay rename

check: lint types test

lint:
	uv run ruff format --check .
	uv run ruff check .

types:
	uv run mypy

test:
	uv run pytest

fmt:
	uv run ruff format .
	uv run ruff check --fix .

run:
	uv run python -m nir_project --config configs/smoke.yaml

mlflow:
	uv run mlflow ui --backend-store-uri sqlite:///mlflow.db

OVERLAY_VERSION ?= v0.1.0
overlay:
	sh scripts/connect_overlay.sh $(OVERLAY_VERSION)

rename:
	@test -n "$(NAME)" || { echo "usage: make rename NAME=<new_package_name>"; exit 1; }
	uv run python scripts/rename.py $(NAME)
