# Product scope

## Product statement

Doctor Booking Agent is an educational simulation showing how a conversational assistant can safely coordinate with deterministic software. It is a portfolio demonstration, not a healthcare service.

## Target audience

- Reviewers assessing full-stack, AI-agent and cloud engineering skills.
- Developers interested in safe tool-using assistant patterns.
- Visitors exploring a realistic but synthetic booking flow.

## Primary user journey

1. A visitor opens the booking page and sees the simulation disclaimer.
2. The visitor describes a service, doctor or time preference, or uses structured controls.
3. The system requests clarification when a required constraint is missing.
4. The system shows verified slots and explains important differences.
5. The visitor selects a slot and reviews a confirmation summary.
6. The visitor optionally supplies an email address for a single confirmation attempt.
7. The system commits the booking and returns a reference and management token.
8. The visitor can later cancel with that token.

## Administrator journey

1. An administrator authenticates through a protected route.
2. The administrator views current synthetic bookings and availability.
3. The administrator can cancel a booking or mark a slot unavailable.
4. The action is recorded with timestamp, action type and administrative identity.

## In scope for the first public release

- Synthetic clinics, doctors, services and schedules.
- Natural-language interpretation with deterministic fallback.
- Structured search and filtering.
- Treatment/service eligibility matching.
- Ranked available-slot suggestions.
- Transactional booking and cancellation.
- Optional one-attempt confirmation email.
- Hashed booking-management token.
- Minimal authenticated administration.
- Responsive and accessible interface.
- Docker packaging and automated deployment.
- Automated tests and agent evaluation cases.

## Explicitly out of scope

- Real providers or real appointments.
- Diagnosis, triage or medical advice.
- Emergency handling beyond directing the visitor to appropriate emergency services.
- Patient accounts or identity verification.
- Medical histories or clinical notes.
- Insurance, eligibility or payment processing.
- Calendar synchronization with real clinicians.
- Recurring marketing messages.
- Storage of visitor email addresses.
- Production healthcare compliance claims.

## Functional requirements

### Search

- Accept natural-language and structured requests.
- Support service, doctor, date range and time-window preferences.
- Resolve only services and doctors in the catalogue.
- Return no unavailable or ineligible slot.
- Offer a useful alternative when an exact match is unavailable.

### Booking

- Require explicit confirmation.
- Prevent concurrent double booking at the database layer.
- Return a non-sensitive public reference and a private management token.
- Never display the private token again after the successful response.

### Email

- Make email confirmation opt-in and unchecked by default.
- Use the address for one delivery attempt only.
- Do not write the address to the application database or application logs.
- Record only that an attempt occurred and when.
- Explain that the delivery provider processes the address.

### Cancellation

- Accept the management token in a request body.
- Compare only its cryptographic hash.
- Make the slot available after a successful cancellation.
- Return the same neutral failure for unknown and invalid tokens.

## Non-functional requirements

- Portfolio-scale operation within free allowances where practical.
- Graceful degradation when AI, email or database services are unavailable.
- Reproducible local and production execution through Docker.
- Keyboard-accessible and screen-reader-compatible core journey.
- No secrets or personal data in browser bundles, source control or logs.
- Observable health, error and latency metrics without logging request content.

## Product language

Use “assistant,” “simulation,” “service” and “appointment.” Avoid claims such as “diagnosis,” “recommended treatment,” “real doctor” or “guaranteed booking.”

