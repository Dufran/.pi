---
name: review-changes
description: Review the currently checked-out branch and local changes using codebase-impact research plus a dedicated end-user UI/usability review
---

## scout
output: codebase-context.md
phase: Context
label: Research current changes and codebase patterns
as: codebaseContext
outputMode: file-only

Research the currently checked-out branch and any local uncommitted changes in this repository.

This is context gathering only. Do not edit files. Do not ask for a PR URL, branch name, issue link, or additional context. Inspect the local repository directly and analyze the current branch changes together with staged, unstaged, and untracked local changes.

Determine the comparison base from the local git repository:
- Prefer the configured upstream/base branch when available.
- Otherwise compare against `origin/main`, `origin/master`, `main`, or `master`, whichever exists.
- Use the merge base and inspect the combined change set from that base through the working tree, including commits on the current branch plus staged, unstaged, and untracked files.
- Use `git diff <merge-base>` for tracked working-tree changes and `git status --short` to discover untracked files, then inspect relevant untracked file contents directly.

Perform change-impact analysis, not only diff inspection. For every behaviorally meaningful change, identify the changed symbols, contracts, data shapes, events, configuration, and side effects, then search the repository for:
- Direct callers, consumers, imports, registrations, overrides, and implementations.
- Indirect dependents such as serializers, API/UI clients, background jobs, signals/hooks, permissions, caches, reports, fixtures, and tests.
- Similar or duplicated flows that implement the same feature elsewhere and may need the same update.
- Assumptions in unchanged code that the new behavior could invalidate.

Follow dependency paths far enough to explain concrete impact, including across module or application boundaries. Do not assume an unchanged file is unaffected merely because it is absent from the diff.

Build a compact codebase context brief for the reviewers. Use these sections, but do not produce a final change review:

### Change scope
- Current branch and detected base branch.
- Changed files and a short description of the change.
- Important diff hunks or behavior changes.

### Existing patterns
- Nearby code patterns relevant to these changes.
- Naming, architecture, typing, error handling, logging, abstractions, tests, fixtures, and configuration conventions the reviewer should compare against.

### Change-impact map
- For each meaningful behavior change, list its direct and indirect dependents, similar implementations, and relevant unchanged files.
- Explain how each location could be affected, or state why it remains compatible.
- Highlight dependent places that appear to require a corresponding code or test change but are missing from the current change set.

### Test context
- Existing tests related to the changed code and its dependent or analogous flows.
- Test style, fixtures, factories, mocks, or validation commands used in this area.
- Obvious missing test areas suggested by the diff and impact map.

### Risk areas
- Files, functions, edge cases, contracts, migrations, dependencies, or behaviors that need careful review.

Cite concrete file paths and line numbers where possible. Return context for the reviewers, not a final review.

## ui-reviewer
phase: UI review
label: Review changed UI for end-user usability and metadata completeness
reads: codebase-context.md
output: ui-review.md
as: uiReview
outputMode: file-only

Review the currently checked-out branch and local uncommitted changes from an end-user UI and usability perspective, using only behavior that can be established from the React codebase and its tests. This is a separate specialist review; do not edit files.

Use the codebase context at {outputs.codebaseContext}, then independently inspect the diff and relevant unchanged code. Apply the same locally detected base/merge-base strategy as the scout, and include staged, unstaged, and untracked changes. First determine whether the change affects any user-visible interface or interaction. If it does not, return a concise “No UI-affecting changes found” result and do not invent UI concerns.

For each affected user flow:
- Identify the user’s goal, entry point, expected sequence, decision points, and completion/recovery path.
- Trace data from API responses, generated clients, props, context, selectors, hooks, and state into rendered React components.
- Build an evidence-based metadata check: what information is available, what reaches the UI, what is displayed or behaviorally used, and what is dropped. Flag only metadata users need to understand status, make decisions, avoid mistakes, or complete the task; do not demand that every technical field be displayed.
- Verify that newly introduced or changed controls have clear labels, affordances, sensible defaults, useful feedback, and protection against accidental or repeated actions.
- Check loading, empty, error, partial-data, stale-data, success, disabled, destructive, and permission-restricted states where applicable.
- Check accessibility: native semantics, accessible names, keyboard operation, focus order and focus restoration, announcements for dynamic changes, and implementation evidence related to contrast or reduced motion.
- Check responsive layouts, overflow, long and localized content, touch targets, hierarchy, consistency with the design system, and consistency with analogous screens.
- Inspect UI tests and identify missing interaction, state, responsive, or accessibility coverage.

Perform a static React code review only. Do not launch the application or use browser automation. Base findings on component rendering, props and state, hooks, event handlers, styling code, semantic markup, and tests. Do not speculate about appearance or runtime behavior that the code does not establish. Record concerns requiring manual runtime verification separately rather than reporting them as confirmed defects.

Return Markdown with these sections:

### UI impact
Summarize the affected user flows and the React code paths that establish their behavior.

### Blocking usability issues
For each issue include severity, file/location, affected user/task, evidence, why it matters, and a focused suggested fix. If none, write “No major issues found.”

### Non-blocking UX suggestions
Use the same evidence and impact standard. If none, write “No major issues found.”

### Metadata coverage
Explain which user-relevant metadata is surfaced and used, which is missing or dropped, and which omitted metadata is correctly irrelevant.

### Missing UI tests
List concrete tests that should be added. If none, write “No major issues found.”

Be specific, prioritize user impact, and cite file paths and line numbers where possible.

## reviewer
phase: Final review
label: Consolidate engineering and UI findings
reads: codebase-context.md, ui-review.md

You are reviewing the currently checked-out branch and any local uncommitted changes in this repository as a senior engineer familiar with this codebase.

Use the scout/codebase context saved at {outputs.codebaseContext} and the specialist UI review saved at {outputs.uiReview}, but verify important claims yourself from the repository. Treat the UI review as evidence, not authority: include its concrete user-impacting findings in the final recommendation, reconcile overlaps with engineering findings, and discard unsupported or irrelevant suggestions. Do not return only a list or summary of changed files. Your final answer must be a consolidated change review with findings and recommendation.

Do not ask for a PR URL, branch name, issue link, or additional context. Inspect the local repository directly and review the current branch changes together with staged, unstaged, and untracked local changes. Do not edit files; this is review-only.

Confirm the comparison base from the local git repository:
- Prefer the configured upstream/base branch when available.
- Otherwise compare against `origin/main`, `origin/master`, `main`, or `master`, whichever exists.
- Use the merge base and inspect the combined change set from that base through the working tree, including commits on the current branch plus staged, unstaged, and untracked files.
- Use `git diff <merge-base>` for tracked working-tree changes and `git status --short` to discover untracked files, then inspect relevant untracked file contents directly.
- Also inspect relevant nearby code, tests, configuration, and project instructions needed to judge consistency.

For every behaviorally meaningful change, independently trace its impact beyond the changed files. Search references to changed symbols and contracts, inspect callers and consumers, and follow data/control flow through APIs, serializers, UI clients, jobs, signals/hooks, permissions, caches, configuration, fixtures, and tests as applicable. Search for analogous or duplicated implementations of the same feature elsewhere. Explicitly verify whether unchanged dependent locations remain compatible; if a corresponding update is missing, report the resulting behavior as a finding. Do not treat absence from the diff as evidence that a location is unaffected.

Review the changes against the existing codebase, not in isolation. Focus on:

1. Consistency with existing patterns
   - Does the implementation match nearby code, architecture, naming, error handling, logging, typing, and abstractions?
   - Does it duplicate existing functionality or introduce a parallel pattern without justification?

2. Cross-codebase impact and dependencies
   - Which direct and indirect consumers depend on the changed behavior, contract, data shape, side effect, or configuration?
   - Do analogous flows or duplicated implementations require the same change?
   - Could unchanged callers, clients, jobs, hooks, permissions, caches, reports, fixtures, or tests now behave incorrectly?

3. Correctness and edge cases
   - Are there logic errors, race conditions, security issues, performance regressions, or backwards-incompatible changes?
   - Are edge cases, failure paths, and boundary conditions handled?

4. Test coverage
   - Are there missing or weak tests for the changed behavior?
   - Are both success and failure paths covered?
   - Do tests follow the repository’s existing test style and fixture patterns?

5. Repository standards
   - Does the code follow the repo’s formatting, linting, typing, naming, dependency, and documentation conventions?
   - Are migrations, configuration changes, changelog entries, or docs needed?

6. Maintainability
   - Is the solution simple, readable, and appropriately scoped?
   - Are there unnecessary abstractions, hidden coupling, or unclear responsibilities?

7. End-user UI and usability
   - Do changed flows help users understand state, make decisions, complete tasks, and recover from errors?
   - Are user-relevant data and metadata carried through to the UI and surfaced or used at the right time?
   - Are interaction states, accessibility, responsive behavior, and design-system consistency adequate?
   - Incorporate supported findings from the specialist UI review, including UI test gaps.

Return the review using Markdown third-level headings with exactly these section names:

### Summary
Briefly describe what the current checked-out branch and local uncommitted changes do, including user-visible impact, and give your overall risk assessment.

### Blocking issues
List issues that should be fixed before merge. For each issue include:
- File/location
- Problem
- Why it matters
- Suggested fix

If there are no blocking issues, write “No major issues found.”

### Non-blocking suggestions
List improvements that are useful but not required. If none, write “No major issues found.”

### Missing tests
List specific test cases that should be added or improved. If none, write “No major issues found.”

### Questions
List any assumptions or unclear requirements that need confirmation. Only include questions that remain after inspecting the local repo. If none, write “No major issues found.”

### Final recommendation
Choose one: approve, approve with comments, request changes.

Be specific and avoid generic feedback. Cite file paths and line numbers where possible.
