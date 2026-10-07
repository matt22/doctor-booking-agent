# Deployment and operations

## Objectives

- Maintain a public portfolio demo with minimal idle cost.
- Deploy one immutable Docker image.
- Avoid Kubernetes and permanently allocated application compute.
- Keep infrastructure replaceable and configuration explicit.

## Environment model

| Environment | Runtime | Database | Purpose |
| --- | --- | --- | --- |
| Local | Docker Compose or local Vite plus Docker API/database | PostgreSQL container | Development and integration tests |
| CI | GitHub-hosted runner | Ephemeral PostgreSQL service | Tests, image build and smoke checks |
| Production | Scale-to-zero container runtime | Managed PostgreSQL | Public demo |

## Docker responsibilities

Docker will:

- Pin the production Python and system runtime.
- Build React/Tailwind assets in a temporary Node stage.
- Install locked Python dependencies.
- Package FastAPI and compiled assets together.
- Define the non-root process and startup command.
- Provide the exact artifact exercised by CI and production.

Docker will not provide hosting, HTTPS, durable storage, secrets, autoscaling or deployment automation. Those remain platform responsibilities.

## Current hosting direction

The leading option is a scale-to-zero container service paired with Neon PostgreSQL. An AWS-oriented deployment may instead package FastAPI for AWS Lambda as a container image and use API Gateway, with Neon remaining the database.

Ordinary RDS is not the baseline because its free eligibility is time-limited and an allocated instance becomes billable. The deployment contract will avoid requiring cloud-specific database features.

## Configuration

Expected runtime configuration:

| Variable | Purpose | Secret? |
| --- | --- | --- |
| `APP_ENV` | Environment selection | No |
| `DATABASE_URL` | Pooled PostgreSQL connection | Yes |
| `PUBLIC_BASE_URL` | Absolute public origin | No |
| `INTENT_PROVIDER` | `deterministic` or configured model adapter | No |
| `MODEL_API_KEY` | Optional model credential | Yes |
| `EMAIL_PROVIDER_API_KEY` | Optional delivery credential | Yes |
| `TOKEN_HASH_PEPPER` | Optional keyed token hashing | Yes |
| `ADMIN_*` | Managed identity configuration | Mixed |

Secrets must live in the deployment platform’s secret store and GitHub Actions secrets where deployment requires them. They must never enter the image or repository.

## CI pipeline

Pull requests will eventually run:

1. Python formatting, linting and static typing.
2. TypeScript formatting, linting and type checking.
3. Unit, integration and concurrency tests.
4. Agent evaluation cases with a deterministic test double by default.
5. Frontend accessibility and browser smoke tests.
6. Production Docker build.
7. Container startup and health verification.
8. Dependency and image vulnerability scans.

Merges to `main` will build once, tag the image with the Git commit SHA, publish it and deploy that exact digest.

## Database migration policy

- Alembic migrations are versioned with the application.
- Deployment runs compatibility checks before routing traffic.
- Destructive migrations require a staged expand/migrate/contract process.
- Synthetic seed data is repeatable and separate from schema migration.
- Database credentials use TLS and the provider’s pooled endpoint.

## Cost controls

- Minimum application instances set to zero.
- Maximum instances limited conservatively.
- Strict model request/output limits.
- Per-IP and per-session request throttling.
- Provider budgets and alerts enabled before public launch.
- No background polling that prevents scale-to-zero.
- Health monitoring paced to avoid keeping the service continuously warm.

## Observability

Collect metadata rather than content:

- Request count, status and latency.
- Search outcome counts without query text.
- Booking success/conflict/cancellation counts.
- Model success, timeout, invalid-output and fallback counts.
- Email attempt outcome without recipient address.
- Database connection and query latency.

Logs will use correlation IDs but exclude conversation text, email addresses and management tokens.

## Recovery and degradation

- The deterministic UI remains available when the model integration is disabled.
- A failed email attempt does not roll back a confirmed booking.
- A database outage returns a clear retryable response rather than cached availability.
- Synthetic schedules can be recreated from seed data.
- Future slots are generated on demand from schedule templates, and a weekly scheduled workflow resets stale demo bookings without keeping the service warm.
- Minimal booking data can be exported for provider migration.

