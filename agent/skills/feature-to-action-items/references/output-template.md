# Action-items artifact template

```markdown
---
title: <Feature> action items
date: YYYY-MM-DD
feature: <feature/story reference>
repository: <repository name>
commit: <sha or unknown>
status: implementation-ready | needs-decision
---

# <Feature> action items

## Executive summary

- **Outcome:** <user/business outcome>
- **Scope:** <surfaces and actions included>
- **Slicing mode:** tracer-bullet vertical / ownership / hybrid — <why this fits the repository and request>
- **Recommended first slice:** <smallest demonstrable item from the current frontier>
- **Plan status:** <implementation-ready or blockers>

## Requirements and decisions

### Action matrix

Include for multi-surface, multi-state, or multi-action features. Otherwise use a compact requirements list.

| Surface / entity state | Action | Inputs | Result / side effects | Requirement IDs | Source evidence | Evidence status |
|---|---|---|---|---|---|---|

### Constraints and explicit non-goals

- <constraint or out-of-scope behavior>

### Ambiguities, contradictions, and assumptions

| ID | Type | Statement/evidence | Impact | Blocking item IDs | Decision status | Resolution or owner needed |
|---|---|---|---|---|---|---|

## Existing code and gap map

| Capability | Classification | Repository evidence | Required change | Confidence |
|---|---|---|---|---|
| <single-item flow> | Reuse as-is / Extend / New / Refactor prerequisite / Decision needed | `<path:line-range>` | <change or none> | High / Medium / Low |

## Shared contracts

### <Contract name>

- **Request:** `<shape>`
- **Response:** `<shape>`
- **Validation:** <rules and owner>
- **Eligibility/authorization:** <rules>
- **Partial failure:** <semantics and stable error identifiers>
- **Side effects:** <notifications, emails, records, events>
- **Retry/idempotency:** <behavior>
- **Consumers:** <item IDs>

Omit this section when no cross-item contract is needed.

## Proposed backlog

| Order | Working ID | Jira-compatible title | Owner | Size | Blocked by | Requirement IDs |
|---:|---|---|---|---|---|---|
| 1 | ACT-001 | `[FE] Add …` | Frontend | M | None | REQ-01, REQ-02 |

## Detailed action items

### ACT-001 — [FE] <Outcome-oriented title>

- **Outcome:** <observable capability delivered>
- **Why:** <user need, risk, or prerequisite>
- **Verified repository facts:**
  - `<path:line-range>` — <fact>
- **Inferences / unknowns:**
  - <claim, rationale, and validation needed>
- **Proposed approach:**
  - <design proposal; cite analogous conventions where available>
- **Implementation scope:**
  - <bounded change>
  - <bounded change>
- **Non-goals:**
  - <behavior intentionally excluded>
- **Contract/API impact:** <none or reference to shared contract>
- **Acceptance criteria:**
  - [ ] <observable behavior>
  - [ ] <negative/error behavior>
- **Tests / validation:**
  - <specific automated test or command>
  - <manual/integration validation if needed>
- **Blocked by:** <direct hard-gating working item IDs, or none>
- **Parallelization:** <what can happen concurrently and why>
- **Requirement traceability:** <REQ IDs, supplied AC aliases, and decision IDs>
- **Size:** S | M | L
- **Risks / open questions:** <none or explicit items>

## Requirement traceability

| Requirement ID | Requirement summary | Source evidence | Evidence status | Action item(s) | Coverage status |
|---|---|---|---|---|---|
| REQ-01 | <summary> | <source anchor or short quote> | Sourced / Inferred | ACT-001 | Covered / Blocked / Out of scope |

## Dependency graph and implementation sequence

- **Current frontier:** <items with no unsatisfied blockers>
- **Graph validation:** <acyclic; note any blocked decision nodes>

### Phase 1 — <name>

- ACT-001
- <demonstrable exit condition>

### Phase 2 — <name>

- ACT-002, ACT-003 (parallel where safe)

## Deferred / out of scope

- <item and reason>

## Review checkpoint

- Does the granularity feel right, or is any item too coarse/fine?
- Are all `Blocked by` edges genuine hard gates?
- Should any items be merged or split?

## Validation and evidence gaps

- **Repository instructions read:** <paths>
- **Code paths inspected:** <summary>
- **Commands run:** <commands/results>
- **Not validated:** <gaps and impact>
```

## Compact title-only view

When the user asks for only the action-item list, return this compact view instead of the detailed template:

```markdown
## Jira work-item titles

1. `[FE] Add …`
2. `[BE] Add …`
3. `[QA] Verify …`
```

When detailed and compact views are both requested, the detailed artifact is authoritative. Never invent tracker IDs.
