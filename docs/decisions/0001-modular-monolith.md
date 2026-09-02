# ADR 0001: Use a modular monolith

- Status: Accepted
- Date: 2026-09-01

## Context

The project needs clear frontend, API, agent, booking and persistence boundaries but expects portfolio-scale traffic and one maintainer.

## Decision

Deploy one FastAPI application with internal domain modules. Compile the React frontend into the production image.

## Consequences

- One release artifact, domain and operational surface.
- Easier local development and lower hosting cost.
- Internal interfaces must prevent modules from becoming tightly coupled.
- Modules can be extracted later only if measured requirements justify it.

