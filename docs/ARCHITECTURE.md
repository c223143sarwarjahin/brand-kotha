# BrandKotha — Architecture & Monorepo Engineering Guide

**Version:** 2.0 (Production Engineering Baseline)  
**Authors:** Team A (Kalpona Koly, Mahir Tajuar Akash, Rawfun Shovon, Sarwar Jahin)  
**Target Domain:** `brandkotha.com`

---

## 1. Monorepo Architecture Overview

BrandKotha is organized as a decoupled, polyglot monorepo using **Turborepo** and **pnpm workspaces** for TypeScript/Node.js, with native virtual environments for the Python FastAPI backend.

```text
brand-kotha/
├── apps/
│   ├── api/                 # Python 3.12+ FastAPI Modular Monolith
│   └── web/                 # Next.js 15 (App Router, Tailwind CSS, TypeScript)
├── packages/
│   └── api-client/          # Auto-generated typed TypeScript SDK (@brandkotha/api-client)
├── docker/                  # Local PostgreSQL 16 & Redis 7 container configs
├── docs/                    # PRD, TRD v2.0, Architecture blueprints & ER diagrams
│   ├── BrandKotha_PRD_and_TRD_v2.md
│   ├── ARCHITECTURE.md
│   └── BrandKotha_PRD_and_TRD_v2.pdf
├── scripts/                 # Bootstrap & code generation scripts
├── Makefile                 # Standard developer command interface
└── turbo.json               # Monorepo build pipeline & dependency graph
```

---

## 2. Architectural Decision Records (ADRs)

### ADR 001: Modular Monolith vs. Microservices
* **Decision:** Implement a Clean Layered Modular Monolith with FastAPI.
* **Context:** Over-distributing into microservices adds distributed transaction complexity, network serialization latency, and deployment friction that harms fast MVP iteration in Bangladesh.
* **Consequence:** Clean domain boundaries (`auth`, `profiles`, `campaigns`, `pitches`, `chat`, `reviews`, `billing`, `admin`) exist as in-memory Python packages with zero network overhead. Background work is offloaded asynchronously to Celery workers via Redis.

### ADR 002: Single Source of Truth for API Contracts
* **Decision:** FastAPI Pydantic v2 models define all API requests, responses, and error shapes.
* **Context:** Manually synchronizing TypeScript interfaces with Python data schemas causes runtime bugs and schema drift.
* **Consequence:** The frontend consumes `@brandkotha/api-client` generated directly from `/openapi.json`. When a backend model updates, running `make codegen` automatically updates the frontend types.

### ADR 003: Deterministic 100-Point Match Score Formula
* **Decision:** Implement an explainable, deterministic scoring algorithm rather than a black-box AI model:
  $$\text{Total Score} = \text{Niche Alignment (50)} + \text{Platform Alignment (25)} + \text{Budget Fit (25)}$$
* **Context:** SME brands and creators in Bangladesh need clear, explainable reasons why a creator matches a campaign brief.
* **Rules:**
  * **Niche (50 pts):** $+50$ if creator niche equals campaign category; $0$ otherwise.
  * **Platform (25 pts):** $+25$ if creator primary platform equals campaign platform; $0$ otherwise.
  * **Budget & Rate (25 pts):** $+25$ if `creator.rate <= campaign.budget`. If creator rate exceeds budget by $\le 20\%$, awards $+12$ (negotiable fit); otherwise $0$.

### ADR 004: Server-Side Monetization Switch (`charge_enabled`)
* **Decision:** Build complete payment flows (bKash Tokenized Checkout, SSLCommerz, aamarPay) behind a server-side boolean flag (`charge_enabled`).
* **Context:** BrandKotha runs 100% free during closed and open trial cohorts to build marketplace liquidity and network effects in Dhaka and Chattogram.
* **Consequence:** Switching to monetization requires zero code changes or database migrations—an admin simply toggles the setting in the Owner Screen.

---

## 3. Database Schema Dictionary (PostgreSQL 16)

Primary keys utilize time-ordered **UUIDv7** for indexing locality and zero ID-guessing vulnerabilities. All monetary currencies are stored as integer Bangladeshi Taka (`INT` in BDT).

| Entity | Primary Key | Key Foreign Keys & Indexes | Core Invariants & Rules |
| :--- | :--- | :--- | :--- |
| `users` | `id` (UUID PK) | Index: `(role, status)` | `UNIQUE(email)`, `UNIQUE(phone)`. Argon2id password hashes. |
| `profiles` | `id` (UUID PK) | FK $\rightarrow$ `users.id` (1:1 cascade) | `UNIQUE(handle)`. Composite index on `(niche, platform, rate, followers)`. |
| `campaigns` | `id` (UUID PK) | FK $\rightarrow$ `users.id` (`brand_id`) | Composite search index on `(status, category, platform, budget)`. |
| `applications` | `id` (UUID PK) | FK $\rightarrow$ `campaigns.id`, FK $\rightarrow$ `users.id` | **Single-Pitch Invariant:** `UNIQUE(campaign_id, creator_id)`. |
| `conversations`| `id` (UUID PK) | FK $\rightarrow$ `users.id` (`user_one_id`, `user_two_id`) | **Canonical Pair Invariant:** `CHECK(user_one_id < user_two_id)` & `UNIQUE(user_one_id, user_two_id)`. |
| `messages` | `id` (UUID PK) | FK $\rightarrow$ `conversations.id`, FK $\rightarrow$ `users.id` | Partial Index: `WHERE read_at IS NULL` for instant unread badge counts. |
| `reviews` | `id` (UUID PK) | FK $\rightarrow$ `applications.id` | **1 Review Per Side:** `UNIQUE(application_id, from_user_id)`. Gated on `ACCEPTED` pitch status. |
| `payments` | `id` (UUID PK) | FK $\rightarrow$ `users.id` | `UNIQUE(gateway_provider, gateway_trx_id)`, `UNIQUE(idempotency_key)`. |
| `platform_settings` | `id` (INT PK) | Singleton constraint: `CHECK(id = 1)` | Stores `charge_enabled`, commission %, lead fee, and tier rates. |
| `audit_logs` | `id` (UUID PK) | Index: `(created_at, actor_id)` | Append-only immutable log for all administrative modifications. |

---

## 4. Real-Time Chat & Concurrency Controls

1. **State Machine Locking:** Transitions from `PENDING` $\rightarrow$ `ACCEPTED` use PostgreSQL `SELECT ... FOR UPDATE` row locks to prevent duplicate acceptance races.
2. **WebSocket Messaging Architecture:**
   * Incoming WebSocket connections at `/api/v1/ws/chat` authenticate via short-lived JWT ticket tokens.
   * Redis 7 Pub/Sub acts as the central fan-out message bus across horizontally scaled Uvicorn workers.
   * Messages are persisted transactionally in PostgreSQL before broadcast to active client connections.

---

## 5. Security & Threat Mitigation

* **BOLA / IDOR:** Repository queries strictly bind `current_user.id` to prevent cross-tenant access.
* **Password Security:** Argon2id (memory cost 64 MiB, 3 iterations, 4 parallelism threads).
* **Payment Webhook Verification:** Server-to-server HMAC-SHA256 signature and `val_id` verification against gateway servers.
* **Rate Limiting:** Redis sliding-window limiters: 5 req/min on registration, 10 req/min on login, 30 pitches/day per creator.

---

## 6. Implementation Status & Upcoming Sprint Roadmap

### Current Status (Baseline Scaffolding Complete)
| Component | Implementation Status | Notes |
| :--- | :--- | :--- |
| **Database Schema** | **Applied & Active** | Alembic migration `001_initial_schema.py` executed on PostgreSQL 16. |
| **Matching Engine** | **Completed & Tested** | Pure Python 50/25/25 scoring engine verified with unit test suite. |
| **Health & Core API** | **Active** | `/api/v1/health/live` and `/ready` endpoints returning HTTP 200. |
| **Web Frontend** | **Scaffolded (Static Mockups)** | Next.js 15 pages render static UI mockups to validate mobile layout & UX. |
| **Docker Services** | **Operational** | PostgreSQL 16 and Redis 7 healthy in Docker Desktop. |

### Next Sprint Tasks
1. **Module `auth`:** Implement `POST /api/v1/auth/register`, `POST /api/v1/auth/login`, and session cookie rotation.
2. **Module `campaigns` & `pitches`:** Implement campaign CRUD, single-pitch submission invariant, and Brand Accept/Decline state transitions.
3. **Frontend Integration:** Wire TanStack Query v5 to consume live FastAPI endpoints, replacing static page mockups with PostgreSQL-backed data.
