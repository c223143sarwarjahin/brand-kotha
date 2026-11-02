.PHONY: help dev dev-local docker-up docker-down docker-logs api-dev web-dev db-migrate db-makemigrations test lint codegen clean setup

# Default target
help:
	@echo "========================================================================"
	@echo " BrandKotha Developer Monorepo Commands (Team A)"
	@echo "========================================================================"
	@echo " setup             Bootstrap full environment (Python venv + pnpm install)"
	@echo " dev               Start local full stack (DB + Redis in Docker, Apps locally)"
	@echo " docker-up         Start complete stack in Docker (Postgres, Redis, API, Web)"
	@echo " docker-down       Stop all Docker containers"
	@echo " docker-logs       Follow Docker container logs"
	@echo " api-dev           Run FastAPI backend standalone (http://localhost:8000)"
	@echo " web-dev           Run Next.js frontend standalone (http://localhost:3000)"
	@echo " db-migrate        Apply latest Alembic database migrations"
	@echo " db-makemigrations Create a new Alembic migration based on models"
	@echo " test              Run Pytest backend and frontend test suites"
	@echo " lint              Run Ruff (Python) and ESLint (Next.js)"
	@echo " codegen           Generate typed TypeScript API client from FastAPI OpenAPI"
	@echo " clean             Clean build artifacts, caches, and temp files"
	@echo "========================================================================"

setup:
	@bash scripts/setup.sh

# Start infra in Docker, run apps locally with hot-reloading
dev:
	@echo "Starting PostgreSQL 16 and Redis 7 in Docker..."
	@docker compose -f docker/docker-compose.yml up -d postgres redis
	@echo "Services ready. Starting FastAPI & Next.js..."
	@pnpm run dev

# Full containerized stack
docker-up:
	@docker compose -f docker/docker-compose.yml up --build -d

docker-down:
	@docker compose -f docker/docker-compose.yml down

docker-logs:
	@docker compose -f docker/docker-compose.yml logs -f

# Standalone App Commands
api-dev:
	@cd apps/api && python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

web-dev:
	@pnpm --filter @brandkotha/web dev

# Database Migrations
db-migrate:
	@cd apps/api && alembic upgrade head

db-makemigrations:
	@cd apps/api && alembic revision --autogenerate -m "Auto migration"

# Quality Assurance
test:
	@echo "Running backend Pytest suite..."
	@cd apps/api && pytest -v
	@echo "Running frontend typecheck..."
	@pnpm run typecheck

lint:
	@echo "Running Python Ruff linter & formatter check..."
	@cd apps/api && ruff check . && ruff format --check .
	@echo "Running Frontend linter..."
	@pnpm run lint

codegen:
	@bash scripts/generate-client.sh

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type d -name ".ruff_cache" -exec rm -rf {} +
	@rm -rf apps/web/.next apps/web/out packages/*/dist
