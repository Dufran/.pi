---
name: pr-review
description: Review the currently checked-out PR using scout codebase research first
---

## scout
phase: Context
label: Research current PR and codebase patterns
as: codebaseContext
output: codebase-context.md
outputMode: file-only

Research the currently checked-out pull request in this repository.

This is context gathering only. Do not edit files. Do not ask for a PR URL, branch name, issue link, or additional context. Inspect the local repository directly and analyze only the current checked-out PR changes.

Determine the comparison base from the local git repository:
- Prefer the configured upstream/base branch when available.
- Otherwise compare against `origin/main`, `origin/master`, `main`, or `master`, whichever exists.
- Use the merge base and inspect the diff from base to the current `HEAD`.

Perform change-impact analysis, not only diff inspection. For every behaviorally meaningful change, identify the changed symbols, contracts, data shapes, events, configuration, and side effects, then search the repository for:
- Direct callers, consumers, imports, registrations, overrides, and implementations.
- Indirect dependents such as serializers, API/UI clients, background jobs, signals/hooks, permissions, caches, reports, fixtures, and tests.
- Similar or duplicated flows that implement the same feature elsewhere and may need the same update.
- Assumptions in unchanged code that the new behavior could invalidate.

Follow dependency paths far enough to explain concrete impact, including across module or application boundaries. Do not assume an unchanged file is unaffected merely because it is absent from the diff.

Build a compact codebase context brief for the reviewer. Use these sections, but do not produce a final PR review:

### PR scope
- Current branch and detected base branch.
- Changed files and a short description of the change.
- Important diff hunks or behavior changes.

### Existing patterns
- Nearby code patterns relevant to this PR.
- Naming, architecture, typing, error handling, logging, abstractions, tests, fixtures, and configuration conventions the reviewer should compare against.

### Change-impact map
- For each meaningful behavior change, list its direct and indirect dependents, similar implementations, and relevant unchanged files.
- Explain how each location could be affected, or state why it remains compatible.
- Highlight dependent places that appear to require a corresponding code or test change but are missing from the PR.

### Test context
- Existing tests related to the changed code and its dependent or analogous flows.
- Test style, fixtures, factories, mocks, or validation commands used in this area.
- Obvious missing test areas suggested by the diff and impact map.

### Risk areas
- Files, functions, edge cases, contracts, migrations, dependencies, or behaviors that need careful review.

Cite concrete file paths and line numbers where possible. Return context for the reviewer, not a final review.

## reviewer
phase: Review
label: Final PR review
reads: codebase-context.md

You are reviewing the currently checked-out pull request in this repository as a senior engineer familiar with this codebase.

Use the scout/codebase context saved at {outputs.codebaseContext}, but verify important claims yourself from the repository. Do not return only a list or summary of changed files. Your final answer must be a PR review with findings and recommendation.

Do not ask for a PR URL, branch name, issue link, or additional context. Inspect the local repository directly and review only the current checked-out PR changes. Do not edit files; this is review-only.

Confirm the comparison base from the local git repository:
- Prefer the configured upstream/base branch when available.
- Otherwise compare against `origin/main`, `origin/master`, `main`, or `master`, whichever exists.
- Use the merge base and inspect the diff from base to the current `HEAD`.
- Also inspect relevant nearby code, tests, configuration, and project instructions needed to judge consistency.

For every behaviorally meaningful change, independently trace its impact beyond the changed files. Search references to changed symbols and contracts, inspect callers and consumers, and follow data/control flow through APIs, serializers, UI clients, jobs, signals/hooks, permissions, caches, configuration, fixtures, and tests as applicable. Search for analogous or duplicated implementations of the same feature elsewhere. Explicitly verify whether unchanged dependent locations remain compatible; if a corresponding update is missing, report the resulting behavior as a finding. Do not treat absence from the diff as evidence that a location is unaffected.

Review the PR against the existing codebase, not in isolation. Focus on:

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

Return the review using Markdown third-level headings with exactly these section names:

### Summary
Briefly describe what the current checked-out PR changes and your overall risk assessment.

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
