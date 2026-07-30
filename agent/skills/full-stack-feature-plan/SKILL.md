---
name: full-stack-feature-plan
description: Create a detailed, repository-grounded sequential backend/frontend implementation plan from a pasted feature specification, acceptance criteria, ADR summary, ticket, or product brief. Use when the user wants an implementation plan with exact codebase seams, dependencies, task checklists, tests, QA, risks, and rollout—not source-code implementation.
disable-model-invocation: true
---

# Full-Stack Feature Plan

Turn the text supplied after `/skill:full-stack-feature-plan` into an implementation-ready, sequential plan grounded in the current repository.

This skill plans work only. Do not modify application source, migrations, generated clients, lockfiles, or unrelated documentation. Always save the completed plan as a Markdown file in the current working directory. Read-only subagent artifacts outside project source are allowed.

## Invocation

```text
/skill:full-stack-feature-plan <feature specification, ticket, ADR summary, or acceptance criteria>
```

The text after the command is the authoritative product input. Preserve explicit scope, non-goals, accepted risks, and terminology. Do not silently replace the requested design with an older repository pattern or a preferred alternative.

## Output goal

Produce a plan that another coding agent can execute without repeating broad repository discovery. The final result must:

- separate backend and frontend work while showing their dependency order;
- use sequential task IDs and checkbox task lists;
- identify exact existing and likely new paths;
- distinguish verified repository facts from recommendations;
- surface contradictions and decisions that block a safe contract;
- define model, API, service, state-transition, permission, concurrency, integration, notification, testing, QA, rollout, and rollback work where applicable;
- include repository-native validation commands;
- avoid pretending missing infrastructure, screens, roles, settings, or integrations already exist;
- write the final plan to `<feature-name-slug>.md` in the current working directory.

## Operating rules

1. Read repository instructions before planning:
   - root `AGENTS.md` or equivalent;
   - area-specific backend/frontend guidance;
   - README, manifests, task runner, and API generation instructions as needed.
2. Inspect the current implementation directly. Do not rely on filenames or feature text alone.
3. Treat generated files as generated. Identify their source and regeneration command; never plan manual edits to generated output unless repository guidance explicitly requires it.
4. Prefer existing architecture and house patterns, but call out when those patterns are unsafe or insufficient for the requested feature.
5. Never copy a permission class without checking queryset/object tenant scoping.
6. For time, booking, inventory, money, or other contested resources, include transaction, locking, stale-state, idempotency, and concurrent-request behavior.
7. For external integrations, separate local domain state from provider synchronization state. Plan retries, idempotency, partial failure, compensation, secret configuration, observability, and reconciliation.
8. For periodic jobs, require durable deduplication when duplicate delivery would be harmful. A cache TTL alone is not durable unless the feature explicitly accepts that limitation.
9. For structured chat/timeline/UI cards, identify the durable source of truth and typed payload seam. Do not recommend mutable business state encoded only in prose or unvalidated message JSON.
10. Record absent concepts explicitly—for example, no company-admin role, no employer settings UI, no timezone field, or an existing app with conflicting semantics.
11. Do not expand backlog items into the implementation plan. Keep them under non-goals or deferred work.
12. Do not estimate calendar time unless the user asks. Relative dependencies and effort/risk are sufficient.
13. If the supplied text is detailed enough, produce the plan without blocking on follow-up questions. Put unresolved owner decisions in a clearly marked pre-implementation section and recommend a safe default when possible.
14. Cite paths clearly. Add line references when they materially support a surprising finding or risk; do not flood every checklist item with line numbers.
15. Derive the output filename from the feature's primary name, not from the entire request. Convert it to a lowercase kebab-case slug, remove punctuation, collapse repeated hyphens, and append `.md`. Example: `Interview Scheduling: Self-Service Candidate Booking` becomes `interview-scheduling-self-service-candidate-booking.md`.
16. Resolve the output path against the current working directory. Never place the plan in a subdirectory unless the user explicitly requests a different path.
17. Before writing, check whether the exact output file exists. Do not overwrite it silently. If it exists and overwrite permission was not provided, stop and ask whether to replace it; do not choose a different filename automatically.

## Workflow

### 1. Parse the feature contract

Extract and retain:

- actor/user stories;
- acceptance criteria;
- state transitions;
- entry points and screens;
- data ownership and tenant boundaries;
- settings/defaults/fallbacks;
- integrations and failure behavior;
- notifications and scheduled work;
- explicit non-goals/backlog;
- rollout requirements and accepted risks.

Build a private requirements matrix before inspecting code. Look for internal contradictions, especially where one acceptance criterion requires data that another section removes.

### 2. Establish repository context

Inspect at minimum:

- project structure and area guidance;
- current apps/modules with related names;
- authentication, role, company/tenant, and ownership models;
- relevant models, serializers/controllers/views, services, filters, routes, tasks, notifications, and tests;
- frontend routes, navigation, pages, shared components, API client generation, state management, forms, tables/lists, chat/rendering, notification settings, i18n, and tests;
- configuration, secret handling, task scheduling, and deployment fixtures;
- current Git status so read-only planning does not overwrite or misreport user work.

When an existing module shares the requested feature name, verify whether it represents the same domain. Recommend a separate app/module when reuse would create misleading models, routes, schemas, or ownership.

### 3. Use read-only parallel reconnaissance for broad features

For a substantial backend/frontend feature, use subagents when available.

Before execution:

```text
subagent({ action: "list" })
```

Launch a small fresh-context fanout, normally:

1. backend context builder/scout;
2. frontend context builder/scout;
3. architecture/risk reviewer.

Every child must:

- inspect the repository directly;
- not modify project/source files;
- return exact paths, existing patterns, missing infrastructure, task sequence, tests, ambiguities, and risks;
- avoid deciding unapproved product questions silently.

Keep the parent as final synthesizer. Personally read the load-bearing files and verify important or contradictory child claims. If subagents are unavailable or fail, continue with direct repository inspection rather than lowering the evidence standard.

### 4. Identify blocking decisions

Create a short **Pre-implementation decisions** section only for choices that materially affect schema, API, permissions, concurrency, UX, or infrastructure.

For each decision:

- state the contradiction or missing contract;
- explain why it matters;
- list viable options;
- mark the recommended option;
- show which later tasks depend on it.

Typical examples:

- booking horizon, lead time, slot cadence, and timezone display;
- missing fallback availability;
- ambiguous free-text versus structured actions;
- absent company-admin authorization;
- proposal expiration/multiple-active-record behavior;
- provider credential type and API ownership;
- whether provider calls are synchronous or asynchronous;
- candidate versus manager timezone presentation.

Do not turn routine engineering judgments into user blockers. Make and state safe implementation recommendations for ordinary details.

### 5. Design the backend sequence

Order backend tasks by dependency. Use identifiers such as `BE-1`, `BE-2`, and nested sections.

Cover applicable work in this order:

1. app/module and domain boundary;
2. enums and transition/actor matrix;
3. models, constraints, indexes, migrations, factories, and admin;
4. settings and ownership APIs;
5. core domain computation/services;
6. tenant-scoped serializers, filters, permissions, views, and routes;
7. structured message/event integration;
8. transaction-safe user actions and stale/conflict responses;
9. external provider client and asynchronous synchronization;
10. cancellation/compensation/retry/reconciliation;
11. role-specific list/detail APIs and ordering/filtering;
12. notifications, preferences, templates, deep links, periodic sweeps, and durable deduplication;
13. OpenAPI/client generation;
14. backend tests and repository validation commands.

For every major backend task include:

- dependencies;
- likely files;
- checkbox implementation items;
- permission/tenant rules;
- constraints and indexes where relevant;
- error/status semantics;
- tests and validation.

For stateful actions, explicitly plan:

- allowed source and destination states;
- actor authorization;
- `transaction.atomic()` boundary or equivalent;
- row/resource locking strategy;
- stale version or availability recheck;
- idempotent repeated request behavior;
- stable conflict response, normally `409`;
- post-commit side effects.

### 6. Design the frontend sequence

Start frontend implementation only after the backend/OpenAPI contract needed by the UI is stable, unless the repository intentionally supports a handwritten temporary adapter.

Use identifiers such as `FE-1`, `FE-2`, and cover applicable work in this order:

1. generated API regeneration and DTO/hook verification;
2. routes, navigation, feature flags, and i18n skeleton;
3. shared status/date/formatting primitives;
4. settings/configuration screens;
5. feature entry points;
6. shared structured renderers and role-specific actions;
7. provider pending/failure/retry states;
8. manager/admin list and actions;
9. worker/candidate cross-context list and links;
10. notification preferences and notification routing;
11. realtime/cache invalidation;
12. focused component/integration tests, typecheck, lint, and user-flow validation.

For every new screen/component include the relevant state checklist:

- initial loading;
- background refresh;
- true empty;
- filtered empty;
- populated;
- validation error;
- permission/read-only state;
- mutation pending;
- recoverable API failure/retry;
- stale/conflict state;
- external integration pending/success/failure;
- mobile/responsive behavior where relevant.

Inspect all role-specific rendering paths. Do not assume employer and worker chat/list implementations share one component.

### 7. Add QA and rollout

Create an ordered end-to-end QA sequence organized by user flow, not only by technical layer.

Include applicable checks for:

- initial/no-configuration state;
- happy path from every entry point;
- tenant isolation and actor permissions;
- concurrent actions and stale choices;
- external provider failure and retry;
- cancellation during provider work;
- list filtering/sorting and cross-context links;
- notification preferences, deduplication, and deep links;
- timezone/DST behavior;
- realtime update behavior.

Create a staged rollout plan:

1. additive schema/backfill;
2. backend APIs with feature disabled;
3. schema/client generation;
4. frontend behind a shared flag;
5. provider credential smoke test;
6. enable creation/actions;
7. enable scheduled jobs last;
8. monitor named metrics/errors;
9. rollback by disabling entry points/jobs without deleting durable records.

### 8. Validate the plan before responding

Perform a final adversarial pass:

- Does every acceptance criterion map to at least one task and one verification step?
- Are explicit non-goals excluded?
- Are backend/frontend dependencies ordered correctly?
- Are generated-file workflows correct?
- Are tenant filters explicit rather than implied by permission classes?
- Are concurrency and stale-state cases covered?
- Are provider partial failures represented in persisted state?
- Are reminder/retry operations idempotent?
- Are all current repository gaps accurately described?
- Are exact validation commands taken from repository guidance?
- Did the plan avoid inventing already-existing screens or roles?

## Required final response structure

Use this shape, adapting headings only when the feature has no backend or frontend component:

```markdown
# <Feature> — implementation plan

## Important codebase findings
1. <verified finding with path>

## 0. Pre-implementation decisions
### 0.1 <decision>
- [ ] <option/decision task>
- **Recommended:** <safe default>
- **Blocks:** BE-x, FE-y

# 1. Backend implementation plan
## BE-1. <task name>
**Depends on:** ...
**Likely files:** ...
- [ ] ...
### Tests
- [ ] ...

# 2. Frontend implementation plan
## FE-1. <task name>
**Depends on:** ...
**Likely files:** ...
- [ ] ...
### Screen states/tests
- [ ] ...

# 3. End-to-end QA sequence
## QA-1. <flow>
- [ ] ...

# 4. Rollout and rollback
1. ...

## Recommended execution order
<one concise dependency sequence>
```

The plan should be detailed enough to hand to implementation agents, but avoid repeating the entire product specification verbatim. Prefer concrete tasks, contracts, paths, and verification over generic advice.

## Plan artifact and response

Always save the plan instead of returning the full document only inline:

1. Identify the feature's primary title from the supplied text.
2. Convert it to a lowercase kebab-case slug.
3. Write the complete plan to `<current-working-directory>/<feature-name-slug>.md`.
4. Verify that the file exists and contains the expected top-level sections.
5. Do not modify any other project file.
6. In the chat response, report:
   - the exact output path;
   - the derived feature name;
   - a one-sentence summary of what the plan covers;
   - any unresolved blocker that prevented writing, if applicable.

If the exact file already exists, ask for overwrite permission before writing it. Do not silently overwrite it and do not invent a suffixed filename.
