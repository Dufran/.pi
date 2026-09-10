---
name: feature-to-action-items
description: Turn a complete product feature description plus repository/codebase context into evidence-backed, implementation-ready Markdown work items with Jira-compatible titles. Use when asked to break a feature, story, PRD, acceptance criteria, or technical proposal into vertical, frontend, backend, shared, migration, test, or rollout items grounded in the existing codebase.
---

# Feature to Action Items

Convert a feature specification and its codebase context into a coherent implementation backlog. Inspect the repository before proposing work. Produce concise Jira-compatible titles plus enough detail for an engineer to implement each item without rereading the entire feature specification.

This is a Markdown-only planning skill. It does not implement the feature, connect to Jira or another tracker, or create/update tracker issues. Use local working IDs such as `ACT-001`; never invent tracker identifiers.

## Inputs

Infer these when possible:

- **Feature source:** pasted description, linked file, issue, PRD, prototype, or acceptance criteria.
- **Codebase scope:** current repository by default, or paths/repository supplied by the user.
- **Delivery:** return the plan inline unless the user requests a file, supplies an output path, or repository instructions establish a plan-artifact convention. When writing without an explicit path, use `docs/plans/<feature-slug>-action-items.md` when `docs/` exists, or `<feature-slug>-action-items.md` at the repository root.
- **Title style:** Jira-compatible by default. Preserve known project keys only as source references; never invent issue IDs.
- **Slicing mode:** follow an explicit user/team convention. Otherwise prefer narrow tracer-bullet vertical slices that produce demonstrable behavior across the relevant layers. Use ownership-sliced `[FE]`/`[BE]` items when the request asks for them or repository/team evidence shows independently reviewable ownership or deployment boundaries.
- **Desired granularity:** implementation-sized items that are independently assignable, reviewable, testable, and usually fit one pull request or fresh implementation context. Default to medium-grained items rather than file-by-file chores.

Ask a question only if the feature source or repository scope is unavailable or two materially different interpretations would change the backlog. Never overwrite an existing artifact implicitly. If the user requested an exact existing path, ask whether to update it; otherwise choose a numbered filename and report the chosen path.

## Safety and evidence rules

- Read repository instructions before inspecting code.
- Snapshot Git status when Git is available. Do not modify source code, install dependencies, run migrations, contact production services, or stage/commit files.
- Treat the feature description as intent and the repository as implementation evidence. Neither automatically overrides the other; report conflicts.
- Cite repository evidence as `path:line-range` wherever practical.
- Label claims as **verified**, **inferred**, or **unknown**. Do not fabricate endpoints, components, services, models, hooks, tests, or conventions.
- Reuse existing behavior where the code supports it. Do not turn “what already works” into rebuilding tasks.
- Preserve explicit product decisions and out-of-scope boundaries.
- Never resolve a product contradiction based only on what seems conservative. If ambiguity affects observable behavior, authorization, persisted data, external side effects, API contracts, or backlog decomposition, ask for a decision when possible. Otherwise mark dependent items blocked and set the plan to `needs-decision`. Only make reversible implementation assumptions that do not alter the product contract, and label them explicitly.
- Do not create Jira issues, assign people, or estimate story points unless explicitly requested and the required tracker context is available.

## Workflow

### 1. Normalize the feature contract

Extract a compact requirements model before looking for solutions:

- actors and user outcomes;
- surfaces/pages and eligible entities/statuses;
- action matrix by surface;
- state transitions and lifecycle rules;
- fields, validation, placeholders, and content rules;
- success, partial failure, retry, and empty states;
- notifications and side effects;
- permissions, tenancy, authorization, and concurrency expectations;
- performance/volume assumptions;
- dependencies and reusable existing flows;
- out-of-scope items;
- rollout order and operational checks;
- every atomic normative product requirement found in prose, acceptance criteria, constraints, and explicit non-goals.

Convert each atomic normative requirement into a stable `REQ-##` entry. Preserve supplied acceptance-criterion IDs as aliases. Record a source anchor or short quote for every entry; label newly inferred requirements as inferred rather than source requirements. Build a requirements list or matrix proportional to the feature. Note duplicated statements, ambiguities, and contradictions, especially where validation ownership, lifecycle behavior, permissions, data persistence, or failure handling are described inconsistently.

### 2. Establish repository context

Inspect the minimum evidence needed to understand the change:

- root and scoped `AGENTS.md`/`CLAUDE.md`, README, architecture docs, ADRs, and contribution guidance;
- manifests, framework configuration, routing, API conventions, state management, test setup, and generated-client conventions;
- files named in the feature description;
- current single-item implementations, their serializers/forms, services, lifecycle hooks, notifications, permissions, and tests;
- analogous implementations and established success/error response patterns;
- relevant frontend ownership, interaction and accessibility patterns, state boundaries, data fetching, forms, and shared components;
- relevant data constraints, transactions, idempotency, lifecycle guards, and concurrency behavior.

Trace actual call paths rather than trusting filenames in the feature description. Search for referenced symbols and inspect their callers and tests. If a cited path or symbol is stale or absent, say so.

For a broad repository, use read-only parallel investigation only when an approved delegation tool is available. Discover available workers first, give them fresh, non-overlapping scopes, and prohibit edits. Otherwise inspect the same scopes sequentially. Typical scopes are requirements/traceability, backend/data/side effects, frontend/state/interactions, and test/rollout/cross-cutting concerns. Artifact production must not depend on delegation being available; the executing agent synthesizes the final backlog.

### 3. Produce a verified gap map

For each requested behavior, classify the codebase state:

- **Reuse as-is** — already provides the required behavior and contract.
- **Extend** — existing flow is close but needs a bounded change.
- **New** — no suitable implementation exists.
- **Refactor prerequisite** — extraction or contract cleanup is truly needed before safe reuse.
- **Decision needed** — requirements conflict or architecture evidence is insufficient.
- **Out of scope** — explicitly excluded; do not create an implementation item.

Record affected paths, existing tests, API/client-generation implications, shared contracts, notifications, authorization, and likely review boundaries. Separate repository facts from suggested design. Within each item, every claim about an existing path, symbol, behavior, test, convention, or ownership boundary must either have a repository citation or be labeled inferred/unknown. Clearly label proposed new names and contracts as proposals; do not present them as existing codebase facts.

### 4. Design the work-item graph

Create items around coherent outcomes, not individual files. Every item must be independently understandable and should usually fit one pull request or fresh implementation context.

Choose and state the slicing mode:

- **Tracer-bullet vertical slices:** preferred when no team convention overrides it. Each item delivers the smallest complete, demonstrable or independently verifiable behavior across every relevant layer, including its tests.
- **Ownership slices:** allowed when explicitly requested or supported by evidence such as `CODEOWNERS`, separate deployables, explicit team guidance, or a stable API/schema boundary that lets frontend and backend land and validate independently. Define their shared contract first and avoid unusable half-features.
- **Hybrid:** use a small shared prerequisite followed by vertical slices only when repository evidence shows the prerequisite genuinely unlocks several outcomes.

Prefer this decomposition order:

1. shared contract or prerequisite only when multiple later items truly depend on it;
2. reusable UI, state, API, or domain primitives justified by multiple consumers;
3. one item per cohesive user outcome or tightly coupled behavior family;
4. cross-cutting validation, formatting, automation, or policy behavior when genuinely shared;
5. focused integration, regression, or rollout work when it cannot live naturally in an implementation item.

Use prefixes consistent with the repository/team when known:

- `[FE]` frontend;
- `[BE]` backend;
- `[FULL]` inseparable vertical slice;
- `[API]`, `[DATA]`, `[QA]`, or `[OPS]` only when those are real ownership boundaries.

#### Split an item when

- different owners can implement it independently after a stable contract is agreed and the ownership boundary is verified;
- it has a distinct deploy/review boundary;
- it changes a separate domain lifecycle or permission boundary;
- it has independent acceptance and validation;
- bundling it would create an oversized or ambiguous item.

#### Keep work together when

- splitting would leave an unusable half-feature;
- changes share one small component/service and one acceptance outcome;
- a “shared abstraction” would be speculative or only have one consumer;
- tests naturally belong to the implementation they validate.

Do not create tickets for trivial wiring, one serializer field, one button, or “add tests” in isolation unless the repository's ownership model requires it. Do not use vague titles such as “backend changes,” “update UI,” or “handle edge cases.” Keep local cleanup inside the behavior item unless cited evidence shows a prerequisite refactor is required for later items to land safely.

#### Handle wide refactors

A wide mechanical refactor that cannot stay green as an ordinary slice is an exception. Use an expand–migrate–contract sequence:

1. **Expand:** introduce the new form beside the old without breaking callers.
2. **Migrate:** move callers in independently green, blast-radius-bounded batches.
3. **Contract:** remove the old form only after every migration item completes.

The contract item is blocked by all migration batches. Use an integration branch or final integrate-and-verify item only when individual migration batches cannot remain green on their own. Do not use this pattern for ordinary feature work or speculative cleanup.

### 5. Define contracts before dependent items

Where frontend and backend are split, state the shared contract once:

- request and response shape;
- identifiers and ordering;
- partial-success semantics;
- per-item error codes/messages;
- authorization and eligibility behavior;
- idempotency/retry expectations;
- validation ownership;
- generated client/schema changes;
- notification and transaction semantics.

Dependent items must reference that contract rather than each inventing their own. Use stable error codes for UI behavior when the repository already follows that convention; do not require UI parsing of arbitrary human-readable errors.

### 6. Validate completeness and implementation order

Give every item a `Blocked by` field containing only direct, hard prerequisites. Preferred order, shared context, or “would be convenient first” are not blockers. Validate that the graph is acyclic, identify items that can run in parallel, and name the current **frontier**: all items whose blockers are already satisfied.

Before writing, check:

- every normalized `REQ-##` maps to an action item, decision, or explicit out-of-scope entry;
- every action item maps to a sourced requirement or a cited, verified technical prerequisite;
- no out-of-scope behavior leaked into the backlog;
- existing flows are reused rather than duplicated;
- permissions, tenant scoping, status races, transactions, external side effects, and error behavior were considered when applicable;
- API schema/client regeneration and tests are included where the repository requires them;
- blocker edges form an acyclic dependency graph and each stage is demonstrable;
- every blocker is a genuine gate rather than a preferred sequence;
- the immediately executable frontier is identified.

If the spec is too large for safe medium-sized items, create phases and split further. Mark genuinely unresolved items as blocked instead of disguising uncertainty as implementation detail.

### 7. Write the artifact

Use the template in [references/output-template.md](references/output-template.md) proportionally:

- **Detailed mode** by default when implementation-ready tickets are requested: include a compact Jira backlog table and detailed work-item cards.
- **Compact mode** when explicitly requested: return only a backlog table or title list plus blockers; do not append detailed cards.
- Omit empty or inapplicable sections rather than emitting placeholders.

A compact response is not independently implementation-ready unless it links to an existing detailed artifact. For a brief slicing example, see [references/worked-example.md](references/worked-example.md).

Titles should follow this pattern:

```text
[FULL] Let users save and reapply report filters
[BE] Expose audit-history pagination through the existing API contract
[FE] Add an accessible project-archiving confirmation flow
```

Prefer outcome-oriented verbs such as `Add`, `Enable`, `Enforce`, `Expose`, `Preserve`, `Reconcile`, `Reuse`, or `Report`. Name the domain behavior and boundary in the title.

## Quality bar for each action item

An implementation-ready item contains:

- one clear outcome;
- why the item exists;
- verified current-state evidence;
- bounded implementation scope and explicit non-goals;
- concrete acceptance criteria;
- tests/validation, including negative and partial-failure paths where relevant;
- dependencies and whether it can run in parallel;
- requirement IDs covered;
- assumptions/open questions that could change implementation;
- suggested size `S | M | L | XL` only as relative complexity, never story points unless requested.

Use `XL` as a signal to split again. Keep titles concise (ideally under 100 characters), but do not sacrifice meaning.

## Final response

Report:

- artifact path, when written;
- number of proposed items by ownership/prefix;
- key reuse findings;
- blockers or contradictions;
- slicing mode, current frontier, and recommended first implementation slice;
- validation performed and evidence gaps.

End with a non-blocking review checkpoint asking whether the granularity feels right, whether blocker edges are genuine, and whether any items should be merged or split. Do not claim the plan is implementation-ready if critical contracts or product decisions remain unresolved.

## Attribution

This skill adapts selected concepts from Matt Pocock's MIT-licensed `to-tickets` skill. See [ATTRIBUTION.md](ATTRIBUTION.md).
