# 🇧🇩 BrandKotha — Creator & Brand Freelancing Marketplace

[![Turborepo](https://img.shields.io/badge/monorepo-Turborepo-ef4444.svg)](https://turbo.build/)
[![FastAPI](https://img.shields.io/badge/backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/database-PostgreSQL_16-336791.svg)](https://www.postgresql.org/)
[![Next.js](https://img.shields.io/badge/frontend-Next.js_15-000000.svg)](https://nextjs.org/)
[![pnpm](https://img.shields.io/badge/package_manager-pnpm-f69220.svg)](https://pnpm.io/)

A dedicated, mobile-first two-sided freelancing and PR collaboration marketplace built specifically for content creators (10K–150K followers) and brands across Bangladesh. Features transparent BDT (৳) pricing, 100-point deterministic match scoring, real-time WebSocket chat, verified mutual reviews, and a feature-flagged monetization engine.

---

## 👥 Engineering Team (Team A)

| Name | Role / Focus Area |
| :--- | :--- |
| **Kalpona Koly** | Frontend Architecture, UI/UX & Responsive Components |
| **Mahir Tajuar Akash** | Database Design, Schema Migrations & Data Integrity |
| **Rawfun Shovon** | Real-time Messaging, WebSockets & Background Workers |
| **Sarwar Jahin** | Backend Core, Security Architecture & DevOps CI/CD |

---

## 🏗️ Monorepo Architecture

```text
brand-kotha/
├── apps/
│   ├── api/                 # Python 3.12+ FastAPI Modular Monolith
│   └── web/                 # Next.js 15 (App Router, Tailwind CSS, Zustand)
├── packages/
│   └── api-client/          # Auto-generated TypeScript API SDK (@brandkotha/api-client)
├── docker/                  # Docker Compose (PostgreSQL 16, Redis 7, Dev Containers)
├── docs/                    # Official PRD, TRD v2.0, ER Diagrams & Architecture Records
│   ├── BrandKotha_PRD_and_TRD_v2.md
│   ├── ARCHITECTURE.md
│   └── BrandKotha_PRD_and_TRD_v2.pdf
├── scripts/                 # Bootstrap & Client Generation Scripts
│   ├── setup.sh
│   └── generate-client.sh
├── Makefile                 # 1-command developer automation
├── turbo.json               # Monorepo build pipeline & dependency graph
└── pnpm-workspace.yaml      # pnpm workspace definition
```

---

## ⚡ Prerequisites

Before running the project, make sure you have the following installed on your machine:

1. **Docker & Docker Compose** (Recommended for local database and cache):
   * [Install Docker Desktop / Engine](https://docs.docker.com/get-docker/)
2. **Node.js 20+** and **pnpm 9+**:
   ```bash
   node -v   # Should be >= 20.0.0
   npm install -g pnpm
   ```
3. **Python 3.12+** (For local backend development):
   ```bash
   python3 --version   # Should be >= 3.12.0
   ```

---

## 🚀 Quickstart Guide (Choose Option A or Option B)

### Option A: Complete Docker Setup (1 Command — Easiest)

If you don't want to install Python packages locally, run the whole stack in Docker:

```bash
# 1. Clone the repository
git clone <repo-url>
cd brand-kotha

# 2. Copy the environment variables template
cp .env.example .env

# 3. Start PostgreSQL 16, Redis 7, FastAPI, and Next.js
make docker-up
```

* **Frontend Web App:** [http://localhost:3000](http://localhost:3000)
* **Backend Interactive API Docs (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc Specification:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
* **To stop:** `make docker-down`

---

### Option B: Local Hybrid Development (Recommended for Fast Hot-Reload)

This option runs PostgreSQL & Redis in Docker while running the FastAPI backend and Next.js frontend directly on your computer with hot-reloading:

```bash
# 1. Bootstrap environment (Creates .env, sets up Python venv, installs pnpm packages)
make setup

# 2. Start PostgreSQL 16 & Redis 7 in Docker and boot both apps:
make dev
```

---

## 🛠️ Common Developer Commands (`make`)

| Command | Action |
| :--- | :--- |
| `make dev` | Start DB & Redis in Docker + run FastAPI & Next.js locally |
| `make docker-up` | Run the complete stack (DB, Redis, API, Web) inside Docker |
| `make docker-down` | Stop and remove all running Docker containers |
| `make docker-logs` | Follow real-time logs from all running Docker services |
| `make api-dev` | Start only the FastAPI backend standalone (`http://localhost:8000`) |
| `make web-dev` | Start only the Next.js frontend standalone (`http://localhost:3000`) |
| `make test` | Run Pytest unit tests for backend and TypeScript typechecks |
| `make lint` | Run Ruff (Python linter/formatter) and ESLint (Next.js) |
| `make db-migrate` | Apply latest Alembic database migrations |
| `make db-makemigrations` | Auto-generate a new Alembic migration based on model changes |
| `make codegen` | Export FastAPI `/openapi.json` and regenerate TypeScript API client |
| `make clean` | Remove temporary cache files, build outputs, and `.pyc` files |

---

## 🔑 Key Architectural Concepts

### 1. Deterministic 100-Point Match Score
Located in [`apps/api/app/modules/matching/engine.py`](apps/api/app/modules/matching/engine.py):
* **Niche Alignment (50 Points):** $+50$ if creator niche matches campaign category; $0$ otherwise.
* **Platform Alignment (25 Points):** $+25$ if creator platform matches campaign platform; $0$ otherwise.
* **Budget & Rate Fit (25 Points):** $+25$ if creator rate $\le$ campaign budget; $+12$ if within $20\%$ negotiable threshold; $0$ otherwise.

### 2. Built-in Monetization Switch (`charge_enabled`)
* Located in [`.env`](.env) and database singleton `platform_settings`:
  * `CHARGE_ENABLED=False` $\rightarrow$ Platform runs 100% free during trial cohorts to build search liquidity in Dhaka & Chattogram.
  * `CHARGE_ENABLED=True` $\rightarrow$ Activates paywall for creator/brand monthly subscriptions, profile/campaign boosts, and transaction commissions via bKash, SSLCommerz, and aamarPay.

### 3. Dedicated Admin Panel
* Located inside the web app at [`/admin`](http://localhost:3000/admin).
* Protected by layout guards and FastAPI role checks (`Depends(require_role(UserRole.ADMIN))`).
* Allows platform operators to inspect payments, review audit logs, and toggle platform settings without direct database access.

---

## 📚 Project Documentation

* 📖 **[Comprehensive PRD & TRD v2.0](docs/BrandKotha_PRD_and_TRD_v2.md)**: Full requirements, personas, workflows, database schema dictionary, and launch criteria.
* 🏛️ **[Architecture & ADR Guide](docs/ARCHITECTURE.md)**: Layer boundaries, WebSocket real-time messaging, and design decisions.

---

## 🤝 Contribution Guidelines

1. **Branch Naming:**
   * Feature: `feat/short-description` (e.g., `feat/pitch-workflow`)
   * Bugfix: `fix/short-description` (e.g., `fix/chat-unread-badge`)
2. **Pre-commit Checklist:**
   ```bash
   make lint    # Ensure zero linter errors
   make test    # Ensure all unit tests pass
   ```
3. Open a Pull Request targeting `main`.
