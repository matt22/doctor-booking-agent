# First-release acceptance criteria

Each criterion is written to become an automated test or a scripted manual check. The milestone column shows when the criterion must first pass. All criteria must pass before the public release (Milestone 5).

Criteria assume the synthetic catalogue in [Synthetic catalogue](synthetic-catalogue.md), an injected clock, and the clinic timezone.

## Search

| ID | Criterion | Milestone |
| --- | --- | --- |
| SRCH-1 | A structured search by service returns only slots belonging to doctors who provide that service. | 1 |
| SRCH-2 | Results never include a slot that is `blocked`, already started, or held by an active booking. | 1 |
| SRCH-3 | A search filtered by doctor returns only that doctor's slots when matching availability exists. | 1 |
| SRCH-4 | A date filter and an earliest/latest time window are applied in clinic-local time. | 1 |
| SRCH-5 | Results are ordered by the documented ranking policy, and identical inputs produce identical ordering. | 1 |
| SRCH-6 | When no slot matches exactly, the response offers up to three alternatives, each labelled with how it differs (other doctor, other date or outside the time window). | 1 |
| SRCH-7 | When no eligible slot exists within the 14-day window, the response says so plainly and suggests broadening the search. | 1 |
| SRCH-8 | An unknown service or doctor is rejected with a message listing valid options; nothing is guessed. | 1 |
| SRCH-9 | Every displayed time shows the clinic timezone label. | 1 |

## Booking

| ID | Criterion | Milestone |
| --- | --- | --- |
| BOOK-1 | Booking requires an explicit confirmation step that shows doctor, service, date, time and timezone. | 1 |
| BOOK-2 | A successful booking returns a public reference and a management token, and the token is not retrievable again. | 1 |
| BOOK-3 | The database stores only the token's digest; no raw token appears in any table. | 1 |
| BOOK-4 | Booking a slot with a service its doctor does not provide returns a validation error and creates no booking. | 1 |
| BOOK-5 | Two concurrent requests for the same slot result in exactly one booking and one `409 Conflict`. Verified against real PostgreSQL. | 2 |
| BOOK-6 | After a conflict, the interface explains that the slot was taken and offers refreshed results. | 1 |
| BOOK-7 | A booked slot no longer appears in any search result. | 1 |

## Cancellation

| ID | Criterion | Milestone |
| --- | --- | --- |
| CNCL-1 | A valid management token cancels its booking and the slot reappears in search results. | 1 |
| CNCL-2 | The token is accepted only in the request body. | 1 |
| CNCL-3 | Unknown, malformed and already-used tokens return the same neutral response, status code and approximate timing. | 2 |
| CNCL-4 | A public booking reference alone cannot cancel a booking. | 1 |
| CNCL-5 | Repeated failed token attempts from one client are rate-limited. | 2 |

## Conversational interpretation

| ID | Criterion | Milestone |
| --- | --- | --- |
| CONV-1 | The deterministic interpreter resolves every catalogue alias to its service code. | 3 |
| CONV-2 | Relative expressions ("tomorrow", "next Tuesday", "after 4") resolve correctly against the injected clock. | 3 |
| CONV-3 | When a required field is missing, the response asks one clarification question and shows structured controls. | 3 |
| CONV-4 | Model output that fails schema validation, or names an entity outside the catalogue, is discarded and never reaches the booking engine. | 3 |
| CONV-5 | With the model disabled, timed out or over quota, the full search and booking journey still completes. | 3 |
| CONV-6 | No conversational input can create, confirm or cancel a booking without the explicit confirmation step. | 3 |
| CONV-7 | Symptom-like input receives a neutral non-diagnostic response; emergency-like input directs the visitor to emergency services. | 3 |
| CONV-8 | Published evaluation results meet: field accuracy ≥ 95% on the deterministic suite, zero invalid-slot suggestions, zero unsupported entities accepted. | 3 |

## Email

| ID | Criterion | Milestone |
| --- | --- | --- |
| MAIL-1 | The email opt-in is unchecked by default. | 4 |
| MAIL-2 | At most one delivery attempt is made per booking, including under retries and duplicate requests. | 4 |
| MAIL-3 | No email address appears in any database row or application log after a booking with email. | 4 |
| MAIL-4 | An email provider failure leaves the booking confirmed and tells the visitor the email was not confirmed. | 4 |
| MAIL-5 | The interface states that the delivery provider processes the address. | 4 |

## Administration

| ID | Criterion | Milestone |
| --- | --- | --- |
| ADMN-1 | Every admin route rejects unauthenticated requests. | 2 |
| ADMN-2 | The admin booking list shows reference, doctor, service, slot and status, and never shows token digests. | 2 |
| ADMN-3 | An admin can cancel a booking by reference, and the slot becomes bookable. | 2 |
| ADMN-4 | An admin can block and unblock a slot; blocking a booked slot warns and leaves the booking in place. | 2 |
| ADMN-5 | Every admin action writes an audit event with actor, action and timestamp. | 2 |

## Privacy and operations

| ID | Criterion | Milestone |
| --- | --- | --- |
| PRIV-1 | No conversation text is persisted to the database or written to logs. | 3 |
| PRIV-2 | Logs contain correlation IDs and metadata only; tokens and email addresses are redacted if they appear. | 2 |
| OPS-1 | `/health/live` responds without a database; `/health/ready` reports database availability. | 1 |
| OPS-2 | A database outage produces a retryable unavailable state, never cached availability. | 2 |
| OPS-3 | Slot generation is idempotent: running it twice creates no duplicate slots. | 1 |
| OPS-4 | The production image runs as a non-root user and passes the container smoke test in CI. | 5 |
| OPS-5 | No secret appears in the repository, image layers or browser bundle. | 5 |

## Accessibility

| ID | Criterion | Milestone |
| --- | --- | --- |
| A11Y-1 | The primary journey (search, select, confirm, cancel) can be completed with a keyboard alone. | 1 |
| A11Y-2 | Automated accessibility checks report no serious or critical violations on the primary journey. | 2 |
| A11Y-3 | Result updates, errors and conflicts are announced to screen readers. | 2 |
| A11Y-4 | The layout works from 320 px wide without horizontal scrolling. | 1 |
