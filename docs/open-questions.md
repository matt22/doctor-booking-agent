# Open questions

Questions that must be answered before, or during, implementation. Each entry carries a recommended answer. Once accepted, a recommendation is folded into the relevant document or recorded as an ADR, and the entry is marked resolved.

| # | Question | Needed by | Status |
| --- | --- | --- | --- |
| 1 | How do service durations relate to slots? | Milestone 1 | Proposed |
| 2 | Which service does a booking record? | Milestone 1 | Proposed |
| 3 | What is the single source of truth for slot availability? | Milestone 1 | Proposed |
| 4 | How does the public demo keep future availability? | Milestone 1 | Proposed |
| 5 | Which timezone interprets relative dates and times? | Milestone 1 | Proposed |
| 6 | Where are rate limits enforced? | Milestone 2 | Proposed |
| 7 | What cold-start latency is acceptable? | Milestone 5 | Open |
| 8 | Which external providers are used? | Milestones 2–5 | Deferred |

## 1. Service duration and slot length

**Problem.** `SERVICE.duration_minutes` exists, but `APPOINTMENT_SLOT` has fixed start and end times. The plan does not say whether a long service can occupy a short slot or several consecutive slots.

**Recommendation.** Use one fixed slot length per doctor, and require every service a doctor offers to fit within a single slot. The seed data guarantees this: a doctor's slot length is at least the longest duration among that doctor's services. A booking always claims exactly one slot.

**Why.** Multi-slot bookings need contiguous-range claims, partial-overlap constraints and more complex conflict handling. That adds concurrency risk without improving the demonstration. Variable-length scheduling can be added later behind the same booking interface.

**Consequence.** Search filters slots by doctor eligibility only. A seed validation check rejects any service longer than its doctor's slot length.

## 2. Service recorded on a booking

**Problem.** `BOOKING` has no service reference, so the system cannot show what was booked or verify eligibility at confirmation time.

**Recommendation.** Add `BOOKING.service_id` (FK to `SERVICE`, not null). Inside the booking transaction, confirm that a `DOCTOR_SERVICE` row exists for the slot's doctor and the requested service. If it does not, reject the request with a validation error, not a conflict.

## 3. Source of truth for availability

**Problem.** `APPOINTMENT_SLOT.availability_state` and `BOOKING.cancelled_at` can both describe whether a slot is free, and they can disagree.

**Recommendation.**

- Whether a slot is booked comes only from bookings. Enforce it with a partial unique index:

  ```sql
  CREATE UNIQUE INDEX booking_one_active_per_slot
      ON booking (slot_id)
      WHERE cancelled_at IS NULL;
  ```

- `APPOINTMENT_SLOT.availability_state` records only administrative state: `open` or `blocked`. It is never changed by booking or cancelling.
- A slot is bookable when it is `open`, starts in the future, and has no active booking.
- Booking creation inserts the row and maps a unique-violation error to an HTTP `409 Conflict`. No application-level read-then-write check is relied on.

**Why.** The constraint lives in one place, cancellation becomes a single-column update, and the race-condition test checks just one invariant.

**Consequence.** If an administrator blocks a slot that has an active booking, the booking stays. The admin can cancel it separately. The admin view should warn about this case.

## 4. Keeping future availability in the demo

**Problem.** Seeded slots pass into the past, and visitors can book every future slot. The cost rules (scale to zero, no background polling) leave nothing to replenish availability.

**Recommendation.** Combine two mechanisms:

1. **Rolling slot generation on demand.** Doctors carry a weekly schedule template in the seed data. When a search or slot listing runs, the API makes sure slots exist for the next 14 days. It inserts any missing slots with `ON CONFLICT DO NOTHING` on `(doctor_id, starts_at)`, and this runs at most once per hour, tracked by a single timestamp row. No idle process is needed.
2. **Scheduled demo reset.** A scheduled GitHub Actions workflow runs weekly. It cancels active synthetic bookings older than seven days and deletes past slots that have no booking. It reuses the deployment's database secret and runs outside the application process, so scale-to-zero is not affected.

**Why.** On-demand generation keeps the demo working however long it sits idle. The reset bounds booking build-up from abuse or testing without adding a server-side scheduler.

**Consequence.** Add `UNIQUE (doctor_id, starts_at)` on `appointment_slot`, and add a schedule-template table or seed structure. Per-IP booking limits (question 6) also prevent the 14-day window being exhausted quickly.

## 5. Timezone for relative expressions

**Problem.** "Next Tuesday after 4 pm" depends on a reference timezone. Multiple timezones are deferred, but one must still be chosen.

**Recommendation.** Interpret all dates and times in the clinic's timezone (`CLINIC.timezone`). The first release ships a single clinic. The interface shows the timezone beside every time ("Times shown in Europe/London"). Store times as `timestamptz`, and give the intent interpreter an injected clock and the clinic's timezone so evaluations stay deterministic.

**Consequence.** The browser's timezone is ignored for interpretation. Visitors in other zones see clearly labelled clinic-local times.

## 6. Rate-limit enforcement

**Problem.** Per-IP and per-session limits kept in process memory do not survive scale-to-zero restarts, and they are not shared between instances.

**Recommendation.** Enforce limits in two layers:

- **Platform layer:** use the hosting platform's edge or request limits where available as the first defense.
- **Application layer:** use a small Postgres fixed-window counter table keyed by a hashed client identifier and route group. Apply it only to state-changing and token-verification routes: booking, cancellation, admin, and model-backed search. Read-only catalogue routes rely on the platform layer.

Store client identifiers as keyed hashes, never raw IP addresses, and delete expired windows during the weekly reset (question 4).

**Why.** A counter in Postgres works the same on every instance and needs no extra infrastructure. Limiting it to low-volume routes keeps database load negligible.

## 7. Cold-start latency

**Problem.** A scaled-to-zero container and a suspended Neon database both need time to wake on the first request. The plan has a retryable unavailable state but no latency target.

**Proposed starting point.** Aim for a first meaningful response within 10 seconds of a cold request. The frontend is served as static assets and renders the shell and disclaimer immediately, then shows a "waking the demo" state while it calls `/health/ready`. Measure real cold-start times during Milestone 5 before committing to a figure, and avoid keep-warm pings that defeat scale-to-zero.

## 8. Deferred provider choices

These choices do not block earlier milestones, and the architecture keeps them behind adapters or configuration:

| Choice | Decide by | Notes |
| --- | --- | --- |
| Administrator identity provider | Milestone 2 | Prefer a managed provider or platform-level access protection over application-owned passwords |
| Language model provider | Milestone 3 | Must support strict structured output and configurable data retention |
| Email delivery provider | Milestone 4 | Review retention and privacy terms before integration |
| Container hosting provider | Milestone 5 | Must support scale-to-zero, secrets and image digests |
| Booking reference format | Milestone 1 | Suggest a short, unambiguous code without guessable sequence (for example `DBA-7K3M9Q`); it is not an authenticator |
