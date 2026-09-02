# ADR 0004: Package with Docker without Kubernetes

- Status: Accepted
- Date: 2026-09-01

## Context

The project benefits from a reproducible runtime and production-like integration tests but does not need cluster orchestration.

## Decision

Build one hardened, multistage Docker image and use Docker Compose for local dependencies. Deploy the image to a managed scale-to-zero runtime. Do not add Kubernetes manifests.

## Consequences

- Runtime consistency without cluster cost or operational overhead.
- Hosting, HTTPS, autoscaling and secrets remain managed-platform concerns.
- The container stays portable across suitable providers.
- Kubernetes experience is intentionally outside this project’s scope.

