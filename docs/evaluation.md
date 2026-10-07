# Evaluation strategy

## Purpose

Evaluation demonstrates that the assistant reliably converts requests into safe, useful actions. It replaces vague claims that the agent has been “trained” with measurable behavior.

## Evaluation layers

### Intent extraction

Cases will cover:

- Exact doctor and service requests.
- Relative dates and time windows.
- Misspellings and common service aliases.
- Missing required information.
- Conflicting preferences.
- Unsupported doctors and services.
- Cancellation intent.
- Irrelevant and adversarial instructions.

Each case defines expected structured fields and allowable clarification behavior.

### Domain behavior

- Only eligible doctors are returned for a service.
- Only open slots appear.
- Ranking honors the documented preference order.
- Useful alternatives differ in an explainable way.
- A lost booking race returns conflict.
- Cancellation releases availability.
- Invalid tokens do not reveal whether a booking exists.

### Safety behavior

- The assistant does not diagnose symptoms.
- Emergency-like language receives a clear boundary response.
- The assistant does not request medical history, payment or insurance information.
- Prompt injection cannot create arbitrary tool calls or bypass confirmation.
- Model output referring to nonexistent identifiers is rejected.

### Privacy behavior

- Email addresses do not appear in database rows or application logs.
- Raw tokens do not appear in database rows or logs.
- Conversation bodies are not persisted.
- Administrative views expose only necessary fields.

## Example evaluation case

```json
{
  "name": "preferred doctor after work",
  "input": "Sports physio with Dr Nova next Tuesday after 4",
  "expected": {
    "intent": "search_appointments",
    "service_code": "sports_physiotherapy",
    "doctor": "dr_nova",
    "earliest_time": "16:00",
    "requires_clarification": false
  }
}
```

Relative dates will be evaluated against an injected clock and timezone so results are deterministic.

## Metrics

- Intent and field accuracy.
- Clarification precision: asks only when information is genuinely required.
- Unsupported-entity rejection rate.
- Invalid-slot suggestion rate, targeted at zero.
- Booking integrity under concurrent requests.
- Fallback completion rate when model inference is unavailable.
- Accessibility violations on the primary journey.

## CI policy

Deterministic tests run on every pull request. Live provider evaluations run manually or on a controlled schedule because they cost money and can vary. Their results are recorded separately from blocking unit tests.

