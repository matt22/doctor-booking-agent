# Synthetic catalogue

The fixed demo data used by seeding, search, the deterministic interpreter and evaluation cases. Every clinic, doctor and schedule here is fictional.

The implementation will hold this catalogue in one versioned file, `data/catalogue.yaml`. The seed loader, the service alias table and the evaluation fixtures all read from that file, so they cannot drift apart.

## Clinic

| Field | Value |
| --- | --- |
| Name | Harbourside Demo Clinic |
| Timezone | `Europe/London` |
| Booking window | Next 14 days |

`Europe/London` changes between GMT and BST, so slot generation must be tested across a daylight-saving transition.

## Services

| Code | Display name | Minutes | Aliases |
| --- | --- | --- | --- |
| `general_consultation` | General consultation | 20 | GP appointment, check-up, checkup, general appointment |
| `blood_test` | Blood test | 15 | bloods, blood work, blood draw |
| `travel_vaccination` | Travel vaccination consultation | 20 | travel jabs, travel vaccines, vaccinations |
| `smoking_cessation` | Stop-smoking consultation | 20 | quit smoking, stop smoking |
| `skin_check` | Skin check | 30 | dermatology, mole check |
| `musculoskeletal_assessment` | Musculoskeletal assessment | 30 | MSK, joint assessment |
| `sports_physiotherapy` | Sports physiotherapy | 45 | sports physio, physio, physiotherapy |
| `nutrition_consultation` | Nutrition consultation | 45 | nutritionist, dietitian, diet advice |

Alias matching is case-insensitive and ignores surrounding punctuation. Each alias maps to exactly one service.

## Doctors

| Doctor | Slot minutes | Services | Weekly hours (clinic time) | Active |
| --- | --- | --- | --- | --- |
| Dr Aisha Shah | 45 | sports physiotherapy, musculoskeletal assessment | Mon, Tue, Thu 12:00–19:30 | Yes |
| Dr Tom Okafor | 45 | sports physiotherapy, musculoskeletal assessment, nutrition consultation | Wed, Fri 08:00–14:00 | Yes |
| Dr Elena Rossi | 20 | general consultation, blood test, travel vaccination, stop-smoking consultation | Mon–Fri 09:00–13:00 | Yes |
| Dr Sam Patel | 30 | general consultation, blood test, skin check | Mon–Thu 13:00–18:00, Sat 09:00–12:00 | Yes |
| Dr Mei Lin | 45 | nutrition consultation | Tue, Thu 10:00–16:00 | Yes |
| Dr Grace Moreno | 45 | sports physiotherapy | Mon–Fri 09:00–17:00 | **No** |

Slots run back to back from each block's start time. A block that does not divide evenly ends at the last whole slot.

## Deliberate gaps

The catalogue is shaped so that alternative and rejection paths are exercised, not only exact matches.

| Scenario | What the data guarantees | Exercises |
| --- | --- | --- |
| Dr Shah, sports physio, Tuesday after 4 pm | Available; this is the README example | Exact match |
| Sports physio, Wednesday after 4 pm | Only Dr Okafor works Wednesdays, mornings only | Alternative date or time window |
| Any service on Sunday | No doctor works Sundays | Alternative date |
| Skin check with any doctor except Dr Patel | Only Dr Patel provides it | Alternative date only; no alternative doctor exists |
| Travel vaccination after 1 pm | Dr Rossi works mornings only | Outside-time-window alternatives |
| Dr Moreno | Inactive doctor with a schedule | Inactive doctors never appear and are treated as unknown |
| Dr Lin for a blood test | Dr Lin does not provide it | Ineligible doctor and service pair is rejected |
| Saturday general consultation | Only Dr Patel, 09:00–12:00 | Narrow availability |

## Unsupported requests

These must be rejected or clarified, never mapped to a service.

- **Services outside the catalogue:** dentist, MRI scan, chiropractor, eye test, counselling.
- **Ambiguous phrases:** "assessment", "an appointment", "see someone". These need a clarification question.
- **Unknown doctors:** any name not in the active doctor list, including Dr Moreno.
- **Symptom descriptions:** for example "my knee hurts" or "I have a rash". These get the neutral non-diagnostic response from CONV-7 and are not silently mapped to a service.
- **Emergency language:** for example "chest pain" or "can't breathe". These get the emergency-services boundary response.

## Seed validation rules

The seed loader rejects the catalogue if any of these fail:

1. Every service duration is no longer than the slot length of each doctor who provides it.
2. Every alias is unique across all services.
3. Every doctor has at least one service and, if active, at least one schedule block.
4. Schedule blocks for a doctor do not overlap.
5. Every service is provided by at least one active doctor.
