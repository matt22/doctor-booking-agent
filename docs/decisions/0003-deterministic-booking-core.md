# ADR 0003: Keep AI outside the booking authority boundary

- Status: Accepted
- Date: 2026-09-01

## Context

Language models are useful for interpreting preferences but can return unsupported or invented details. Appointment availability and booking confirmation require deterministic correctness.

## Decision

Use a language model only to return validated structured intent. Application code resolves catalogue entities, queries availability, ranks candidates and commits bookings. The baseline remains usable without model inference.

## Consequences

- The model cannot directly modify data or confirm a booking.
- More explicit service taxonomy and fallback UI are required.
- Model providers can be changed without rewriting the domain.
- Evaluations can distinguish interpretation quality from booking correctness.

