---
name: tech-debt-audit
description: Audit a codebase for evidence-backed technical debt, especially meaningful DRY violations, cognitive complexity and excessive implementation depth, outdated dependencies, deprecated or stale library usage, and viable library alternatives evaluated for developer experience and type safety. Launch read-only subagents and produce a prioritized implementation handoff document. Use when asked to assess codebase health or human maintainability, find technical debt, simplify implementations, review dependency currency or alternatives, or prepare actionable remediation work.
---

# Tech Debt Audit

Run a read-only, evidence-driven technical-debt audit and produce one implementation-ready handoff document. Evaluate meaningful duplication, cognitive load and implementation depth, dependency/API currency, and credible alternatives to strategically important libraries, especially from developer-experience and type-safety perspectives. The audit identifies work; it does not modify project source code or dependency files.

## Inputs

Infer these from the request and repository when possible:

- **Scope**: repository, package, service, or paths to inspect. Default: current repository.
- **Output path**: where to write the handoff. Default: `docs/tech-debt-handoff.md` when `docs/` exists; otherwise `tech-debt-handoff.md` at the repository root.
- **Focus**: optional languages, packages, or concerns.

Ask a question only when the repository/scope is unavailable, the requested scope is materially ambiguous, or writing the default output path would overwrite an existing document without clear permission. If the output already exists, choose a dated or numbered filename and report it.

## Operating rules

- Before launching subagents, call `subagent({ action: "list" })` and use only executable agents.
- Prefer asynchronous subagent orchestration and call `wait()` when results are required and no independent work remains.
- Discovery results must be returned inline or written outside the repository. Only the synthesis agent may write inside the repository, and only to the exact handoff path.
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

Record the exact audit scope, exclusions, repository root, current commit when Git is available, date, and the pre-audit working-tree snapshot.

### 2. Launch parallel discovery

Launch a small parallel fanout, normally five fresh-context read-only roles with at most three running concurrently. Adapt agent names to those available. Use at most three concurrent discovery agents by default. In a monorepo with more than eight packages or an obviously broad scope, first launch one scout; require it to return explicit, non-overlapping package/path scopes, then process at most eight scopes per batch with no more than three agents concurrently. Never launch an unbounded repository-wide discovery prompt.

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
   - Inventory direct dependencies, runtime/toolchain versions, manifests, lockfiles, and dependency-management configuration.
   - Determine latest relevant stable releases from official registries, vendor release notes, official documentation, or maintained repositories. Record installed/declared/resolved version when determinable, latest relevant version, release date when useful, source URL, and verification date.
   - Account for version constraints, runtime compatibility, support/LTS policy, peer dependencies, framework compatibility, pre-release status, and monorepo overrides before recommending an upgrade.
   - Flag unsupported runtimes, unmaintained libraries, stale lockfiles, duplicate dependency versions, missing automated update tooling, and major-version migration risk.
   - Do not equate “not latest” with actionable debt. Classify dependencies as current, behind but acceptable, actionable update, blocked, or unknown.

4. **API usage and maintainability reviewer** (`reviewer`)
   - Trace actual usage of important third-party libraries in source code.
   - Find deprecated/removed APIs, legacy configuration, old integration patterns, compatibility shims, ignored warnings, risky wrappers, and library capabilities duplicated locally.
   - Validate deprecation or migration claims against official docs, changelogs, migration guides, compiler/linter output, or repository evidence.
   - Identify missing or weak tests around proposed migration boundaries and likely regression areas.

5. **Library alternatives researcher** (`researcher`)
   - Select only strategically important direct libraries: core framework/infrastructure dependencies, libraries with significant application coupling, weak typing or poor ergonomics, maintenance concerns, or an actionable update/migration finding. Do not inventory alternatives for every transitive or trivial utility dependency.
   - Identify at most three credible alternatives per selected library, including “keep the current library” as the baseline. Consider replacement, supplement, or native platform/framework capabilities rather than assuming migration is desirable.
   - Evaluate developer experience using concrete evidence: API ergonomics, documentation quality, diagnostics/error messages, tooling and IDE support, testability, configuration burden, ecosystem/integration fit, learning curve, and operational/debugging experience.
   - Evaluate typing/type safety using ecosystem-appropriate evidence: first-party type support, strict-mode compatibility, generic precision and inference, nullability/error modeling, typed configuration and plugins, runtime validation where relevant, generated/stub type quality, static-analyzer compatibility, and the prevalence of casts, ignores, `Any`, or untyped boundaries.
   - Compare maintenance health, license, adoption/ecosystem risk, runtime compatibility, performance or bundle impact when relevant, migration surface, codemod availability, and likely lock-in.
   - Support claims with official documentation, source/type declarations, release history, issue trackers, static-analysis output, or a clearly labeled minimal read-only evaluation. Separate observed facts from judgment; do not use popularity alone as a recommendation.
   - Conclude with `keep`, `adopt`, `pilot`, `watch`, or `reject`, confidence, and the conditions that could change the conclusion. Recommend migration only when benefits outweigh migration and ecosystem costs.

For small repositories, combine roles. Every launch must set `cwd` to the repository root, `context: "fresh"`, `async: true`, a timeout, explicit bounded paths, a read-only/no-project-write constraint, and the required result sections. Canonical shape:

```text
subagent({
  tasks: [
    { agent: "reviewer", task: "Audit DRY debt only within <paths>. Do not modify repository files. Return verified findings, candidates, non-issues, and evidence gaps with path:line evidence.", output: false },
    { agent: "reviewer", task: "Audit cognitive complexity and implementation depth only within <paths>. Trace difficult control flow and indirection, distinguish accidental complexity from justified design, and propose the smallest human-centered simplification without speculative abstraction. Do not modify repository files. Return hotspots, call paths, cognitive-load signals, before/after responsibility sketches, tests, non-issues, and evidence gaps.", output: false },
    { agent: "researcher", task: "Verify dependency currency for manifests under <paths>. Do not modify repository files or install packages. Return versions, exact authoritative URLs, UTC verification times, compatibility constraints, and unknowns.", output: false },
    { agent: "reviewer", task: "Audit third-party API usage only within <paths>. Do not modify repository files. Return evidence-backed deprecated/stale usage, tests at risk, non-issues, and evidence gaps.", output: false },
    { agent: "researcher", task: "For strategically important direct libraries used within <paths>, compare at most three credible alternatives including keeping the current library. Do not modify repository files or install packages. Evaluate developer experience, type safety, maintenance, compatibility, and migration cost using authoritative evidence; conclude keep/adopt/pilot/watch/reject with confidence and unknowns.", output: false }
  ],
  cwd: "<repository-root>",
  context: "fresh",
  async: true,
  concurrency: 3,
  timeoutMs: 900000
})
wait({ all: true, timeoutMs: 900000 })
```

Each discovery result must separate:

- verified findings
- candidates needing validation
- non-issues / intentional patterns
- evidence gaps

### 3. Validate high-value findings

Before synthesis, independently verify findings that are high priority, broad in scope, or based on uncertain heuristics:

- inspect cited files and call sites
- confirm dependency versions from manifests/lockfiles
- run focused repository-provided diagnostics only in documented read-only/no-fix/no-install modes, with timeouts and lifecycle scripts disabled where supported; skip a command if its write/network/credential behavior cannot be established
- prohibit package installs, update commands, auto-fix modes, generated-file rewrites, and commands that require exposing private registry credentials
- distinguish command failure from an actual finding
- verify high-impact alternative recommendations against actual repository usage and type-checking configuration; treat claims requiring a hands-on spike as `pilot`, not `adopt`
- verify cognitive-complexity findings by tracing the cited entry point and change path; ensure the proposed simplification reduces concepts or navigation without hiding behavior or creating a speculative abstraction
- note ecosystems or private dependencies that could not be checked

Never present “all libraries are up to date” unless every in-scope direct dependency and relevant runtime was checked successfully. State coverage numerically where practical, such as `24/27 direct dependencies verified; 3 private packages unknown`.

### 4. Synthesize the handoff

Use one `context-builder` or `planner` as the sole writer of the configured handoff document. Pass it the discovery artifacts, validated corrections, output path, and the required structure below. The writer must not edit any other project file.

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

## Audit method and limitations
- Evidence inspected and commands run
- Authoritative external sources and verification date
- Areas not checked or results that remain unknown

## Prioritized action plan

### TD-001: <outcome-oriented title>
- **Priority:** P0 | P1 | P2 | P3
- **Category:** duplication | cognitive-complexity | excessive-indirection | dependency | deprecated-api | library-alternative | maintainability | testing | tooling
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
- DRY findings cite multiple occurrences and explain why consolidation is safer than locality
- every checked dependency/runtime row includes an exact authoritative URL and per-row UTC verification time; failed verification is `unknown`
- alternatives coverage names which strategic direct libraries were evaluated and why others were excluded
- declared, resolved, and latest relevant versions are not conflated
- compatibility blockers and private/unverifiable packages are explicit
- cognitive-complexity findings include an entry point/call path, concrete human comprehension or change-coupling evidence, a before/after responsibility sketch, and a simplification that reduces total concepts or navigation
- proposed abstractions represent stable domain concepts or change boundaries; they are rejected when they only move complexity or add indirection
- alternative comparisons include the current library baseline, repository-specific use cases, DX and type-safety evidence, migration cost, and a justified disposition
- no migration is recommended solely because an alternative is newer or more popular; uncertain hands-on claims become bounded pilots
- priorities reflect impact and urgency rather than cosmetic preference
- acceptance criteria and validation steps are executable
- duplicate findings are merged
- post-audit Git status/diffs/untracked paths match the pre-audit snapshot except for the exact handoff file; every unexpected file or lockfile change causes a stop and explicit warning
- the handoff file exists at the reported path and no other repository file was written by the audit

Report the handoff path, audit coverage, commands that failed or were skipped, and the most important unresolved risks.