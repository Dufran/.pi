# Worked slicing example

Use this only as a granularity example; do not copy its domain details into unrelated plans.

## Requirement and evidence

- **REQ-04 (sourced):** “A user can archive a project after confirming the action.”
- **Verified evidence:** `projects/services.py:40-67` contains the existing project status transition, while `projects/views.py:90-118` exposes only the current single-step update flow.
- **Gap:** the inspected UI has no confirmation flow and the API does not expose an archive-specific contract.

## Good tracer-bullet item

### ACT-003 — [FULL] Let users safely archive a project

- **Outcome:** A user can initiate archiving, review a confirmation that explains the impact, confirm it, and see the archived state.
- **Scope:** Add the narrow API operation by reusing the existing status-transition service, expose the confirmation interaction, refresh the resulting project state, and include authorization and regression tests.
- **Acceptance:** Unauthorized users cannot archive; cancelling leaves the project unchanged; confirming archives it once; failures preserve the current UI state and present an actionable error.
- **Traceability:** REQ-04 and the cited existing transition behavior.

This is cohesive because it delivers one demonstrable behavior through the necessary UI, API, domain, and test layers.

## Valid ownership split

Split the item into `[BE]` and `[FE]` only when team guidance, ownership metadata, separate deployables, or an agreed API contract lets both parts be implemented and validated independently. Define the request, response, errors, permissions, and state-refresh behavior before splitting.

## Bad alternatives

- `[FE] Add archive button` — leaves an unusable control without the required behavior.
- `[BE] Add archive serializer field` — too small and framed around a file-level mechanism rather than an outcome.
- `[QA] Add archive tests` — tests belong with the behavior unless a separate QA/release boundary is verified.
- `[FULL] Implement project lifecycle management` — too broad; combines unrelated transitions and policy decisions.

## Traceability

| Requirement | Item | Coverage |
|---|---|---|
| REQ-04 | ACT-003 | Confirmation, authorization, transition reuse, resulting state, and failure behavior |
