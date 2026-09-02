# ADR 0002: Use PostgreSQL

- Status: Accepted
- Date: 2026-09-01

## Context

Bookings require relational integrity, transactions, concurrent slot claims, useful date/time queries and a portable managed hosting option.

## Decision

Use PostgreSQL through SQLAlchemy 2, with Alembic migrations. Use a PostgreSQL container locally and a managed scale-to-zero-compatible provider for the public demo.

## Consequences

- Database constraints become the final booking-integrity boundary.
- Provider migration remains practical through standard PostgreSQL tools.
- Serverless runtimes must use a pooled connection endpoint.
- SQLite may be used only for isolated unit tests that do not claim PostgreSQL-equivalent concurrency behavior.

