# Delivery roadmap

## Milestone 0 — planning and architecture

- Publish product scope and non-goals.
- Define architecture, data boundaries and deployment direction.
- Record major decisions and [unresolved questions](open-questions.md).
- Agree on first-release acceptance criteria.

Exit criterion: documentation is coherent enough to scaffold without inventing product behavior during implementation.

## Milestone 1 — deterministic vertical slice

- Scaffold FastAPI, React, Tailwind and PostgreSQL.
- Add synthetic service, doctor and slot seed data.
- Implement structured availability search.
- Add transactional booking and token-based cancellation.
- Build the first responsive end-to-end journey.

Exit criterion: the complete booking flow works locally without AI or email.

## Milestone 2 — quality and administration

- Add protected administrative booking management.
- Add concurrency, security and accessibility tests.
- Add metadata-only observability.
- Establish database migration and seed workflows.

Exit criterion: automated tests verify booking integrity and administration boundaries.

## Milestone 3 — conversational interpretation

- Implement deterministic intent parsing and clarifications.
- Add provider-neutral model adapter.
- Add strict structured-output validation.
- Add graceful fallback and quota controls.
- Publish evaluation cases and results.

Exit criterion: natural-language requests improve convenience without becoming a source of operational truth.

## Milestone 4 — optional email

- Select a delivery provider and review its privacy/retention terms.
- Implement unchecked opt-in and one-attempt semantics.
- Prove the address is absent from database and logs.
- Add delivery state messaging and failure tests.

Exit criterion: confirmation can be attempted without application-level address persistence.

## Milestone 5 — container and public deployment

- Build hardened multistage Docker image.
- Add GitHub Actions tests, image scanning and deployment.
- Provision managed PostgreSQL and secrets.
- Configure budget alerts, rate limits and maximum scale.
- Run production smoke and recovery tests.

Exit criterion: the public demo is reproducible, monitored and bounded in cost.

## Deferred ideas

- Multiple clinics and timezones.
- Calendar export generated client-side.
- Additional languages.
- Provider-specific deployment examples.
- Database branches for pull-request previews.
- Voice input, only if it preserves the privacy boundary.

