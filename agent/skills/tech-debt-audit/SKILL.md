---
name: tech-debt-audit
description: Audit a codebase for evidence-backed technical debt, especially meaningful DRY violations, cognitive complexity and excessive implementation depth, Django ORM/query and query-layer duplication problems, React state-ownership and prop-drilling anti-patterns, Mantine component-override and cross-file styling duplication, outdated dependencies, deprecated or stale library usage, and viable library alternatives evaluated for developer experience and type safety. Launch parallel read-only subagents and produce a prioritized implementation handoff document. Use when asked to assess codebase health or human maintainability, find technical debt, simplify implementations, review Django, React, or Mantine architecture and patterns, review dependency currency or alternatives, or prepare actionable remediation work.
---

# Tech Debt Audit

Run a read-only, evidence-driven technical-debt audit and produce one implementation-ready handoff document. Use parallel, non-overlapping discovery lanes for codebase research, pattern finding, and analysis. Evaluate meaningful duplication, cognitive load and implementation depth, dependency/API currency, and credible alternatives to strategically important libraries, especially from developer-experience and type-safety perspectives. When detected in scope, also evaluate Django query behavior and reusable query/domain boundaries, React state ownership, server/client state separation, effect-driven synchronization, prop drilling, and avoidable render coupling, and Mantine component overrides that should become reusable variants or extensions. React findings may be reasoned assumptions from code structure, types, component contracts, and referenced usage; runtime profiling or production evidence is not required when the inference and uncertainty are explicit. The audit identifies work; it does not modify project source code or dependency files.

## Inputs

Infer these from the request and repository when possible:

- **Scope**: repository, package, service, or paths to inspect. Default: current repository.
- **Output path**: where to write the handoff. Default: `docs/tech-debt-handoff.md` when `docs/` exists; otherwise `tech-debt-handoff.md` at the repository root.
- **Focus**: optional languages, packages, frameworks, or concerns.
- **Framework signals**: detect Django from dependencies/settings/apps/models/querysets/DRF usage and React from dependencies/JSX or TSX/framework configuration. Detect Mantine reliance per frontend workspace only when a component-bearing runtime dependency such as `@mantine/core` is both declared/resolved and traced to live non-generated application imports, re-exports, rendered components, or an active `MantineProvider`/theme entry point. A transitive, lockfile-only, unused, test-only, story-only, or `@mantine/hooks`-only reference is insufficient. Apply framework-specific checks only where those signals exist.

Ask a question only when the repository/scope is unavailable, the requested scope is materially ambiguous, or writing the default output path would overwrite an existing document without clear permission. If the output already exists, choose a dated or numbered filename and report it.

## Operating rules

- Before launching subagents, call `subagent({ action: "list" })` and use only executable agents.
- Launch coordinated discovery through asynchronous `workflowScript` calls with stable keys and `runs.all`; when this run-to-completion skill requires results and no independent work remains, use `subagent_wait`, never polling or the removed `wait()` API.
- Discovery results must be returned inline or written outside the repository. Set `progress: false` for discovery children. Only the synthesis agent may write inside the repository, and only to the exact handoff path.
- Use fresh context so reviewers inspect repository evidence rather than inheriting assumptions.
- Never upgrade dependencies, refactor code, regenerate lockfiles, install packages, or apply findings during the audit.
- Snapshot Git status, staged/unstaged diffs, and untracked paths before fanout when Git is available. Compare them afterward and stop/report every unexpected change; never discard a pre-existing user change.
- Do not claim that a dependency or API is outdated from model memory alone. Verify current information using authoritative sources and record the verification date and URLs.
- Respect repository instructions and avoid expensive full test suites unless needed to validate a factual claim.
- Redact secrets, tokens, private registry credentials, and sensitive configuration from outputs.

## Workflow

### 1. Establish repository context

Inspect repository guidance and the minimum files needed to plan the audit:

- project instructions (`AGENTS.md`, `CLAUDE.md`, `README`, contribution docs)
- manifests and lockfiles
- language/runtime and package-manager configuration
- workspace/monorepo structure
- lint, test, type-check, and build commands
- existing architecture or technical-debt documents
- Django signals when present: settings, installed apps, model/queryset/manager layers, DRF/GraphQL/admin/template boundaries, database backend, and existing query-count/performance tests
- React signals when present: framework and rendering mode, component/state boundaries, routing/data-fetching layer, state libraries, form libraries, and existing profiler/render tests
- Mantine signals when present: workspace manifest and resolved version, live component import/re-export paths, active provider/theme entry points, `createTheme`, `components`, `.extend(...)`, variant resolvers, wrappers, shared design-system packages, and version-supported styling APIs such as presentational props, style props, `style`, `styles`, `classNames`, `vars`, and `sx` where applicable

Record the exact audit scope, exclusions, repository root, current commit when Git is available, date, detected frameworks, and the pre-audit working-tree snapshot.

### 2. Launch parallel discovery

Launch a small fresh-context, read-only discovery fanout with distinct lanes for codebase structure/patterns, human maintainability, and third-party integration usage. Add separate Django, React, and Mantine specialist lanes only when each framework is detected; the Mantine lane is an extra criteria run, not part of the generic React review. Run authoritative dependency research from the exact manifests and API candidates established locally, then evaluate alternatives only after usage and currency results identify a strategic shortlist. Adapt agent names to those available. Enforce at most three concurrent discovery agents by awaiting `runs.all` slices of three; `runs.all` has no `concurrency` option. In a monorepo with more than eight packages or an obviously broad scope, first launch one scout; require it to return explicit, non-overlapping package/path scopes, then create at most eight total local scope-review children rather than a role-by-scope Cartesian product. Never launch an unbounded repository-wide discovery prompt.

1. **Code structure / DRY reviewer** (`reviewer` or `scout`)
   - Find repeated business rules, near-duplicate control flow, duplicated transformations/queries/validation, copy-pasted tests or fixtures that create maintenance risk, and inconsistent parallel implementations.
   - Distinguish harmful duplication from intentional locality, simple repetition, generated code, framework boilerplate, and test clarity.
   - For each candidate, provide file and line references, at least two concrete occurrences, the likely change-coupling risk, a bounded consolidation direction, confidence, and reasons not to consolidate when applicable.
   - Also note dead abstractions, premature generic helpers, or existing utilities that should be reused.

2. **Cognitive complexity / human maintainability reviewer** (`reviewer`)
   - Identify code that is difficult for a maintainer to understand, change, or debug: deeply nested branching, long functions, high decision density, excessive boolean flags, non-local state mutation, temporal coupling, implicit side effects, exception-driven flow, mixed abstraction levels, unclear domain naming, and too many responsibilities in one unit.
   - Trace implementation depth across call chains, wrappers, factories, callbacks, decorators/middleware, inheritance, event flows, and configuration indirection. Flag behavior that requires jumping through many files or abstraction layers to answer “what happens here?”
   - Find accidental complexity: custom machinery already provided by the language/framework, speculative extension points, pass-through wrappers, abstraction chains with one implementation, premature generalization, and clever code whose maintenance cost exceeds its value.
   - Also find missing abstractions where stable domain concepts or change boundaries are repeatedly expressed through low-level details. Do not recommend extraction merely to shorten a function or eliminate a small amount of repetition.
   - Prefer the smallest human-centered simplification: clarify names and control flow, remove dead branches or indirection, use guard clauses, make state transitions explicit, separate orchestration from domain logic, group cohesive behavior, or introduce one stable domain abstraction.
   - For every hotspot, provide the entry point and relevant call path, concrete cognitive-load signals, who/what changes together, a before/after responsibility sketch, the smallest viable simplification, tests needed to preserve behavior, confidence, and reasons the current design might be intentional.
   - Treat numeric cognitive-complexity/lint scores only as discovery signals. Never create an action item from a score without repository-specific evidence of comprehension, change-coupling, defect, or debugging risk.
   - Explicitly reject abstractions that add more concepts, indirection, generic parameters, inheritance, configuration, or files than the complexity they remove.

3. **Dependency and library currency researcher** (`researcher`)
   - Receive the exact direct-dependency inventory, runtime/toolchain versions, manifest/lockfile paths, resolved versions, and API candidates established by the parent and local discovery lanes. Read only those named files when needed; do not perform an unbounded local inventory.
   - Determine latest relevant stable releases from official registries, vendor release notes, official documentation, or maintained repositories. Record installed/declared/resolved version when determinable, latest relevant version, release date when useful, source URL, and verification date.
   - Account for version constraints, runtime compatibility, support/LTS policy, peer dependencies, framework compatibility, pre-release status, and monorepo overrides before recommending an upgrade.
   - Flag unsupported runtimes, unmaintained libraries, stale lockfiles, duplicate dependency versions, missing automated update tooling, and major-version migration risk.
   - Do not equate “not latest” with actionable debt. Classify dependencies as current, behind but acceptable, actionable update, blocked, or unknown.

4. **API usage and maintainability reviewer** (`reviewer`)
   - Trace actual usage of important third-party libraries in source code.
   - Find local candidates for deprecated/removed APIs, legacy configuration, old integration patterns, compatibility shims, ignored warnings, risky wrappers, and library capabilities duplicated locally.
   - Return exact symbols, versions when locally determinable, call sites, wrappers, and test boundaries to the dependency researcher for authoritative external verification. Do not assert deprecation or currency from memory; local compiler/linter output or repository evidence may verify a claim directly.
   - Identify missing or weak tests around proposed migration boundaries and likely regression areas.

5. **Django / React framework specialists, only when detected** (`reviewer`)
   - Run Django and React as separate lanes when both are present unless the in-scope application is demonstrably small.
   - **Django query performance:** trace request/task/serializer/template/admin/GraphQL paths into ORM evaluation. Look for evidenced N+1 queries; repeated queryset evaluation; queries hidden in loops, properties, `__str__`, serializer method fields, or templates; wasteful `count()`/`exists()`/`len()` patterns; unbounded loads; per-row writes; missing bulk operations; and transaction/locking patterns that create concrete contention or correctness risk.
   - Evaluate `select_related`, `prefetch_related`, `Prefetch`, annotations, subqueries, pagination, field projection, indexes, caching, and bulk APIs against the actual access pattern. Do not recommend eager loading, `only()`/`defer()`, caching, or an index by reflex: state cardinality, memory, invalidation, write cost, and database-backend tradeoffs. Index recommendations require a concrete filter/order/join shape and should use an existing representative `EXPLAIN` path when safely available; never use or mutate production data.
   - **Django DRY boundary check:** the code structure / DRY lane owns discovery of duplicated filters, permission/tenant scoping, annotations, ordering, lifecycle rules, validation, and business rules. The Django specialist verifies whether apparently similar cases have distinct authorization, locking, eager-loading, transaction, or consistency semantics before consolidation. Prefer a cohesive custom `QuerySet`/manager, domain service, model constraint, or shared validator only when it represents one stable rule and preserves composability; reject fat-model/fat-view/service-layer indirection that merely moves logic.
   - Require path-and-line evidence plus the query trigger and evaluation point. Prefer existing query-count tests or bounded test-client reproductions. Report measured query counts/timings/plans separately from static suspicions; never invent performance gains from source inspection.
   - **React state architecture:** map each hotspot's state owner, writers, readers, source of truth, and lifecycle. Find duplicated or mirrored state, derived state stored unnecessarily, effect chains used for synchronization, stale-closure risks, state split across competing stores, overly broad global/context state, server data copied into client state, unstable provider values, broad subscriptions/selectors, and state colocated too high or too low.
   - **Props and component boundaries:** flag prop drilling when data or callbacks pass through multiple components that neither interpret nor own them and the code, types, or usage references indicate likely change coupling. Record the chain and depth. Compare the smallest options first: composition/children, colocating state, a feature hook, splitting a component, or an existing context/store. Do not prescribe Context or a new state library merely to avoid two or three explicit props; explicit component APIs and intentional container/presenter boundaries may be clearer.
   - **React effects and rendering:** distinguish server state, URL state, form state, local UI state, and cross-feature client state before recommending ownership. Identify avoidable `useEffect` synchronization, render-phase derivation expressed as effects, incorrect dependency workarounds, remount/reset hacks, and likely rerender fan-out. Static reasoning from component structure, types, hooks, provider values, selectors, and call-site references is sufficient; profiling is optional. Recommendations for `memo`, `useMemo`, `useCallback`, selector rewrites, or state-library changes must explain the inferred render path and tradeoffs rather than asserting a measured speedup. Account for the repository's React/framework version and server/client component model.
   - For Django findings return verified evidence and distinguish measurements from static suspicions. For React findings return cited code/type/reference observations, the resulting assumption, confidence, smallest bounded change, validation ideas, and reasons the current pattern may be intentional; do not block a useful React finding solely because runtime evidence is unavailable. Separate correctness, query-count/render-frequency, latency, memory, and code-organization claims.

6. **Mantine override specialist, only when Mantine reliance is verified** (`reviewer`)
   - Resolve aliases and local re-exports to Mantine components and inspect the active provider/theme/component-extension boundary for the detected Mantine version. Confirm proposed APIs against installed types/source or official version-matched documentation; do not assume current Mantine APIs apply to older majors.
   - Return findings under exactly two categories:
     1. `mantine-component-extension`: existing Mantine elements with a heavy, coordinated bundle of presentational props, style props, `style`, `styles`, `classNames`, `vars`, or version-supported `sx` overrides that repeats within one file or cohesive module and should become an opt-in semantic theme variant or equivalent component extension.
     2. `mantine-cross-file-override-duplication`: the same or semantically equivalent Mantine style/prop override pattern independently appears in at least two non-generated source files and should have one centralized source of truth.
   - For Category 1 require exact occurrence evidence and a normalized heavy override signature with multiple coordinated props, slots, declarations, or state rules plus a concrete stable semantic role and maintainability benefit. Repetition within one module strengthens the case but is not mandatory; a single element may qualify when its override surface is substantial and clearly belongs at the active theme/component-extension boundary rather than being a one-off treatment. When the same pattern crosses files, report the aggregate only in Category 2, not both.
   - For Category 2 require at least two exact file-and-line occurrences from distinct files, verified total occurrence/file counts, a normalized common signature, meaningful differences, Mantine provenance, and the stable semantic role/change boundary. Compare resolved values rather than raw text alone, including referenced constants, spreads, CSS-module declarations, slot mappings, aliases, and property ordering.
   - For both categories inspect existing variants, theme extensions, wrappers, tokens, and design-system primitives before proposing a new abstraction. Explain why an opt-in variant/extension is safer than locality, a plain constant, an existing primitive, a wrapper, or a global default.
   - Reject one-off or art-directed treatments, routine one- or two-prop usage without change-coupling evidence, layout-specific or data-dependent values, unrelated semantic roles, generated/test/story/example code, already-centralized usage, unresolved spreads/classes, accessibility or state differences, and abstractions that merely hide props. Preserve loading, disabled, error, selected, hover/focus, responsive, color-scheme, polymorphic, event, layout, and accessibility behavior.
   - Do not claim bundle-size, render-performance, accessibility, or defect improvements without independent evidence. Treat this primarily as maintainability and design-consistency debt. If Mantine is active but neither category has verified findings, return both category headings with `No verified findings`.

7. **Library alternatives researcher, launched after local usage and currency research** (`researcher`)
   - Receive a named strategic shortlist and repository-specific use cases from validated local usage and currency results. Select only core framework/infrastructure dependencies, libraries with significant application coupling, weak typing or poor ergonomics, maintenance concerns, or an actionable update/migration finding. Do not inventory alternatives for every transitive or trivial utility dependency.
   - Identify at most three credible alternatives per selected library, including “keep the current library” as the baseline. Consider replacement, supplement, or native platform/framework capabilities rather than assuming migration is desirable.
   - Evaluate developer experience using concrete evidence: API ergonomics, documentation quality, diagnostics/error messages, tooling and IDE support, testability, configuration burden, ecosystem/integration fit, learning curve, and operational/debugging experience.
   - Evaluate typing/type safety using ecosystem-appropriate evidence: first-party type support, strict-mode compatibility, generic precision and inference, nullability/error modeling, typed configuration and plugins, runtime validation where relevant, generated/stub type quality, static-analyzer compatibility, and the prevalence of casts, ignores, `Any`, or untyped boundaries.
   - Compare maintenance health, license, adoption/ecosystem risk, runtime compatibility, performance or bundle impact when relevant, migration surface, codemod availability, and likely lock-in.
   - Support claims with official documentation, source/type declarations, release history, issue trackers, static-analysis output, or a clearly labeled minimal read-only evaluation. Separate observed facts from judgment; do not use popularity alone as a recommendation.
   - Conclude with `keep`, `adopt`, `pilot`, `watch`, or `reject`, confidence, and the conditions that could change the conclusion. Recommend migration only when benefits outweigh migration and ecosystem costs.

For small repositories, combine roles only when their evidence boundaries remain explicit. Every launch must set `cwd` to the repository root, `context: "fresh"`, `async: true`, a timeout, explicit bounded paths, a read-only/no-project-write constraint, and the required result sections. Before using this skeleton, replace the framework booleans and exact manifest/source paths from repository context. Canonical shape:

```javascript
subagent({
  cwd: "<repository-root>",
  context: "fresh",
  async: true,
  maxRuntimeMs: 3600000,
  workflowScript: `
    const djangoDetected = false;
    const reactDetected = true;
    const mantineDetected = false;
    const lanes = [
      { key: "code-patterns", agent: "reviewer", task: "Audit harmful duplication and stable domain-rule change coupling only within <exact paths>. Do not modify files. Return verified findings, candidates, intentional locality, and gaps with path:line evidence.", output: false, progress: false, timeoutMs: 900000 },
      { key: "maintainability", agent: "reviewer", task: "Audit cognitive complexity and implementation depth only within <exact paths>. Exclude standalone duplication and dependency currency. Do not modify files. Return hotspots, call paths, responsibility sketches, smallest simplifications, non-issues, and gaps.", output: false, progress: false, timeoutMs: 900000 },
      { key: "integration-map", agent: "reviewer", task: "Trace actual third-party integration seams within <exact paths>. Return local deprecated-API candidates, wrappers, migration boundaries, tests, and gaps; do not make external currency claims or modify files.", output: false, progress: false, timeoutMs: 900000 }
    ];
    if (djangoDetected) lanes.push({ key: "django", agent: "reviewer", task: "Audit Django ORM evaluation and query performance within <exact Django paths>; exclude query-layer DRY owned by code-patterns. Do not modify files or access production data. Return traces, measured evidence versus static candidates, smallest fixes, validation, non-issues, and gaps.", output: false, progress: false, timeoutMs: 900000 });
    if (reactDetected) lanes.push({ key: "react", agent: "reviewer", task: "Audit React state ownership, effects, prop chains, and inferred render coupling within <exact frontend paths>. Do not modify files. Return code/type/reference evidence, assumptions, state-flow traces, smallest fixes, intentional patterns, validation ideas, and gaps.", output: false, progress: false, timeoutMs: 900000 });
    if (mantineDetected) lanes.push({ key: "mantine", agent: "reviewer", task: "Run the Mantine override criterion within <exact frontend paths>. Resolve Mantine provenance, version, active theme/extensions, props, style objects, classes, spreads, and CSS. Return exactly mantine-component-extension and mantine-cross-file-override-duplication findings, or No verified findings under each. Require normalized signatures and the occurrence thresholds from this skill. Do not modify files.", output: false, progress: false, timeoutMs: 900000 });

    const discovery = [];
    for (let i = 0; i < lanes.length; i += 3) {
      discovery.push(...await runs.all(lanes.slice(i, i + 3)));
    }

    const currency = await runs.run("currency", {
      agent: "researcher",
      task: "Using these exact manifests, declared/resolved versions, runtime constraints, and API candidates: <exact inventory>, verify dependency currency and deprecations from authoritative sources. Do not inspect or modify project files and do not install packages. Return exact URLs, UTC verification times, compatibility constraints, coverage, and unknowns. Local discovery context:\n" + discovery.map(r => r.key + ": " + r.output).join("\n"),
      output: false,
      progress: false,
      timeoutMs: 900000
    });

    const alternatives = await runs.run("alternatives", {
      agent: "researcher",
      task: "Evaluate only the strategic direct-library shortlist supported by the discovery and currency results below. Compare keep-current plus at most two credible alternatives per library for repository-specific DX, type safety, maintenance, compatibility, and migration cost. Do not modify files or install packages. Conclude keep/adopt/pilot/watch/reject with confidence and authoritative evidence.\n\nCurrency:\n" + currency.output + "\n\nLocal discovery:\n" + discovery.map(r => r.key + ": " + r.output).join("\n"),
      output: false,
      progress: false,
      timeoutMs: 900000
    });

    return {
      discovery: discovery.map(r => ({ key: r.key, output: r.output })),
      currency: currency.output,
      alternatives: alternatives.output
    };
  `
})
```

When this skill must finish in the current turn, retain the returned workflow id and call `subagent_wait({ id: "<workflow-id>", timeoutMs: 3600000 })` only after independent parent work is exhausted.

Each discovery result must separate:

- verified findings; for React, code/type/reference-based observations and reasoned assumptions are sufficient
- candidates needing validation
- non-issues / intentional patterns
- evidence gaps or inference limits

### 3. Validate high-value findings

Before synthesis, independently verify findings that are high priority, broad in scope, or based on uncertain heuristics:

- inspect cited files and call sites
- confirm dependency versions from manifests/lockfiles
- run focused repository-provided diagnostics only in documented read-only/no-fix/no-install modes, with timeouts and lifecycle scripts disabled where supported; skip a command if its write/network/credential behavior cannot be established
- prohibit package installs, update commands, auto-fix modes, generated-file rewrites, and commands that require exposing private registry credentials
- distinguish command failure from an actual finding
- verify high-impact alternative recommendations against actual repository usage and type-checking configuration; treat claims requiring a hands-on spike as `pilot`, not `adopt`
- verify cognitive-complexity findings by tracing the cited entry point and change path; ensure the proposed simplification reduces concepts or navigation without hiding behavior or creating a speculative abstraction
- for Django, confirm the ORM evaluation point and request/task path; use focused query-count tests or safe local/test-database plans when available, and label source-only N+1/index/performance claims as candidates rather than measured findings
- for React, trace enough of the state/prop flow to support the conclusion, then allow assumptions from code structure, types, hooks, component contracts, selectors, and usage references; runtime profiler/render-count evidence is optional, but inferred performance effects must be labeled as assumptions rather than measured gains
- reject Django abstractions that erase meaningful authorization/transaction/query semantics and React Context/store proposals that merely hide explicit dependencies or introduce a second source of truth
- for Mantine, confirm every counted occurrence resolves to Mantine, compare normalized props/styles/classes rather than raw text, inspect the active theme/extension boundary, and verify the proposed variant or extension API against the detected version; route cross-file patterns only to `mantine-cross-file-override-duplication`
- record every skipped diagnostic with the command or check and the safety, environment, access, or scope reason
- note ecosystems or private dependencies that could not be checked

Never present “all libraries are up to date” unless every in-scope direct dependency and relevant runtime was checked successfully. State coverage numerically where practical, such as `24/27 direct dependencies verified; 3 private packages unknown`.

### 4. Synthesize the handoff

After discovery and parent verification, choose exactly one write-capable executable agent returned by `subagent({ action: "list" })`, normally `worker`, as the sole writer of the configured handoff document. Launch it with repository `cwd`, `context: "fresh"`, `progress: false`, and `output: false`; pass it the discovery artifacts, validated corrections, output path, and required structure below. Instruct it to edit only the exact handoff path and return a concise summary. Do not set runtime `output` to the handoff path because response capture could overwrite the document.

The handoff must be useful to an implementation agent without repeating the audit. Prefer fewer high-confidence items over a long speculative backlog. Merge overlapping findings and explicitly discard weak or false-positive candidates. Only high- or medium-confidence items with bounded scope, no unresolved decision blocker, and effort `S`, `M`, or `L` belong in the implementation action plan. Put low-confidence, blocked, unresolved, and unsplit `XL` candidates in deferred/open questions.

## Required handoff structure

```markdown
---
title: Technical debt implementation handoff
date: YYYY-MM-DD
repository: <name>
commit: <sha or unknown>
scope: <audited scope>
status: implementation-ready | needs-decision
---

# Technical debt implementation handoff

## Executive summary
- Audit scope and exclusions
- Overall themes
- Finding counts by priority and confidence
- Dependency verification and alternatives-evaluation coverage
- Detected Django, React, and Mantine scopes; for Mantine, state whether the activation gate ran or why it was skipped

## Audit method and limitations
- Evidence inspected and commands run
- Authoritative external sources and verification date
- Areas not checked or results that remain unknown

## Prioritized action plan

### TD-001: <outcome-oriented title>
- **Priority:** P0 | P1 | P2 | P3
- **Category:** duplication | cognitive-complexity | excessive-indirection | django-query-performance | django-query-dry | react-state-ownership | react-prop-drilling | react-render-performance | mantine-component-extension | mantine-cross-file-override-duplication | dependency | deprecated-api | library-alternative | maintainability | testing | tooling
- **Confidence:** high | medium | low
- **Effort:** S | M | L | XL
- **Why now:** <maintenance cost, defect risk, support deadline, or blocker>
- **Evidence:** `<path:line-range>` plus commands, versions, and source URLs as applicable
- **Affected surface:** <files, modules, consumers, tests>
- **Recommended change:** <bounded implementation direction, not vague “refactor”>
- **Implementation steps:** <ordered checklist>
- **Acceptance criteria:** <observable completion conditions>
- **Validation:** <specific tests/checks/commands>
- **Risks / rollback:** <migration hazards and safe fallback>
- **Dependencies / blockers:** <other items, compatibility, approvals>

## Dependency currency matrix
| Package/runtime | Declared/resolved | Latest relevant | Status | Compatibility/migration note | Authoritative source | Verified at (UTC) |
|---|---:|---:|---|---|---|---|

## Human maintainability hotspots
| Hotspot / entry point | Cognitive-load signals | Implementation depth / call path | Change-coupling risk | Smallest simplification | Abstraction tradeoff | Confidence |
|---|---|---|---|---|---|---|

For each proposed simplification, explain which concepts, branches, state transitions, navigation steps, or responsibilities are removed. If introducing an abstraction, name the stable domain concept or change boundary it represents and explain why it lowers total cognitive load. Record “keep current design” when simplification would merely move complexity or add indirection.

## Django findings (include only when Django is in scope)
| Entry path and ORM evaluation point | Query/DRY issue | Evidence or measurement | Correctness/performance impact | Smallest change | Validation | Confidence |
|---|---|---|---|---|---|---|

Keep measured query counts, timings, and plans distinct from static candidates. Include relevant database/backend and data-shape caveats. For shared-query recommendations, state the stable rule being centralized and semantics that must remain caller-specific.

## React findings (include only when React is in scope)
| State/prop flow | State kind and source of truth | Issue | Observed or inferred coupling/render impact | Smallest change | Optional validation | Confidence |
|---|---|---|---|---|---|---|

For prop drilling, show the owner-to-consumer chain and identify pass-through components. For state changes, name the writers/readers visible from in-scope code and avoid introducing competing sources of truth. State whether impact is observed or inferred from code, types, component contracts, or usage references. Profiling may be suggested but is not required for inclusion or prioritization.

## Mantine findings (include only when Mantine reliance is verified)
- **Activation evidence:** <manifest plus live runtime import/re-export/provider path:line>
- **Mantine package/version:** <declared and resolved, or unknown>
- **Scope searched:** <workspace and source paths>
- **Theme/extension entry points:** <path:line or none found>

### 1. Heavy element overrides suitable for a variant (`mantine-component-extension`)
| Mantine element and semantic role | Occurrences | Normalized props/style override signature | Existing extension search | Why a variant/extension is the right boundary | Material exceptions | Confidence |
|---|---|---|---|---|---|---|

### 2. Repeated style/prop overrides across files (`mantine-cross-file-override-duplication`)
| Mantine element and semantic role | Files / occurrence count | Normalized shared signature | Meaningful differences | Change-coupling or drift evidence | Centralization direction | Confidence |
|---|---:|---|---|---|---|---|

Keep the two categories visibly separate and write `No verified findings` under either empty category. A cross-file pattern appears only in Category 2 and maps to one aggregate action item. Every row must resolve Mantine provenance, cite exact `path:line-range` evidence, name the detected package/version, preserve caller-specific behavior, and explain why locality, an existing primitive, a constant, a wrapper, or a global default is not safer.

For accepted Mantine work, validation must cover all cited call sites and the active provider/theme boundary using repository-supported type-check, lint, build, tests, Storybook, or visual-regression checks where available. Check relevant default, hover, focus-visible, active, disabled, loading, error, selected, responsive, color-scheme, and polymorphic states actually used; preserve event handlers, accessibility attributes, layout ownership, CSS-module slot mappings, and caller-specific behavior. Verify unrelated consumers do not acquire defaults. Document intentional exceptions and do not require new screenshot infrastructure solely for the finding.

## Library alternatives assessment
| Current library / use case | Candidate | Disposition | Developer experience | Type safety | Maintenance/ecosystem | Migration cost/risk | Confidence | Evidence |
|---|---|---|---|---|---|---|---|---|

For every `adopt` or `pilot` conclusion, include the repository use cases affected, decisive tradeoffs, migration prerequisites, a bounded proof-of-concept plan, measurable success criteria, and rollback conditions. Record “keep current” explicitly when replacement value does not justify churn.

## Suggested execution sequence
- Group items into safe implementation batches.
- Identify prerequisites, parallelizable work, and review boundaries.

## Deferred or rejected candidates
- Record intentional duplication, acceptable version lag, rejected library alternatives, false positives, and low-confidence ideas with brief rationale.

## Open questions
- Include only decisions that require project-owner input.
```

## Prioritization rubric

- **P0**: active security/support/correctness emergency with direct evidence. Do not infer this solely from age.
- **P1**: high defect or maintenance risk, imminent end-of-support, or a blocker for important work.
- **P2**: concrete recurring cost or moderate migration/maintainability risk.
- **P3**: opportunistic cleanup with bounded value.

Effort is a relative implementation size, not a time estimate:

- **S**: localized change with focused tests
- **M**: several files or one contained migration
- **L**: cross-module change requiring coordinated validation
- **XL**: must be split into smaller discovery or implementation items

Set handoff status to `implementation-ready` only when every prioritized action has no unresolved blocker or owner decision. Otherwise use `needs-decision` and keep blocked work out of the executable action plan.

## Quality gate

Before reporting completion, verify that:

- every action item has concrete repository evidence
- DRY findings cite multiple occurrences and explain why consolidation is safer than locality; Django query-layer consolidation preserves distinct authorization, transaction, eager-loading, and consistency semantics
- Django findings identify the entry path and ORM evaluation point; measured query counts/timings/plans are distinguished from source-only candidates, and index/eager-loading/cache recommendations include backend, cardinality, memory, write-cost, or invalidation tradeoffs as relevant
- React state findings identify the inferred source of truth and visible writers/readers; prop-drilling findings show the pass-through chain and explain why composition or colocation is insufficient before proposing Context/a store
- React findings may rely on reasoned assumptions from code, types, component contracts, hooks, selectors, and usage references; assumptions are labeled with confidence, while measured gains are claimed only when measurements exist
- framework recommendations use the repository's actual Django/DRF/database, React/framework/rendering, and Mantine versions rather than generic best practices
- the Mantine criterion ran only where both a component-bearing runtime dependency and live non-generated runtime usage were verified; otherwise its documented skip reason is coverage information, not a finding
- Mantine findings are separated into exactly `mantine-component-extension` and `mantine-cross-file-override-duplication`; heavy-element findings include a normalized substantial override signature and a stable semantic role, while cross-file findings cite at least two distinct files, verified counts, common settings, and meaningful differences
- Mantine aliases, re-exports, spreads, referenced style objects, CSS declarations, slot mappings, provider scope, existing variants/extensions/wrappers/tokens, and version-supported APIs were resolved sufficiently before recommending centralization
- one-off/local treatments, unrelated semantics, generated/test/story code, already-centralized usage, and behavior/accessibility/state differences are rejected; global defaults are recommended only when evidence shows unrelated consumers should also change
- each cross-file Mantine pattern is emitted once under Category 2 rather than duplicated in both categories, and priorities reflect demonstrated maintenance impact rather than override count or visual preference
- every checked dependency/runtime row includes an exact authoritative URL and per-row UTC verification time; failed verification is `unknown`
- alternatives coverage names which strategic direct libraries were evaluated and why others were excluded
- declared, resolved, and latest relevant versions are not conflated
- compatibility blockers and private/unverifiable packages are explicit
- cognitive-complexity findings include an entry point/call path, concrete human comprehension or change-coupling evidence, a before/after responsibility sketch, and a simplification that reduces total concepts or navigation
- proposed abstractions represent stable domain concepts or change boundaries; they are rejected when they only move complexity or add indirection
- alternative comparisons include the current library baseline, repository-specific use cases, DX and type-safety evidence, migration cost, and a justified disposition
- no migration is recommended solely because an alternative is newer or more popular; uncertain hands-on claims become bounded pilots
- priorities reflect impact and urgency rather than cosmetic preference
- acceptance criteria and validation steps are executable; Django performance work includes focused correctness/query-count checks where feasible, React validation may be recommended without being a prerequisite for code/type/reference-based findings, and Mantine work covers affected states, caller-owned behavior/accessibility, intentional exceptions, and unrelated-consumer regressions
- every referenced repository path and validation command was confirmed to exist or clearly marked conditional; every skipped diagnostic records why
- duplicate findings are merged
- post-audit Git status/diffs/untracked paths match the pre-audit snapshot except for the exact handoff file; every unexpected file or lockfile change causes a stop and explicit warning
- the handoff file exists at the reported path and no other repository file was written by the audit

Report the handoff path, audit coverage, commands that failed or were skipped, and the most important unresolved risks.