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

Build a compact codebase context brief for the reviewer. Use these sections, but do not produce a final PR review:

### PR scope
- Current branch and detected base branch.
- Changed files and a short description of the change.
- Important diff hunks or behavior changes.

### Existing patterns
- Nearby code patterns relevant to this PR.
- Naming, architecture, typing, error handling, logging, abstractions, tests, fixtures, and configuration conventions the reviewer should compare against.

### Test context
- Existing tests related to the changed code.
- Test style, fixtures, factories, mocks, or validation commands used in this area.
- Obvious missing test areas suggested by the diff.

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

Review the PR against the existing codebase, not in isolation. Focus on:

1. Consistency with existing patterns
   - Does the implementation match nearby code, architecture, naming, error handling, logging, typing, and abstractions?
   - Does it duplicate existing functionality or introduce a parallel pattern without justification?

2. Correctness and edge cases
   - Are there logic errors, race conditions, security issues, performance regressions, or backwards-incompatible changes?
   - Are edge cases, failure paths, and boundary conditions handled?

3. Test coverage
   - Are there missing or weak tests for the changed behavior?
   - Are both success and failure paths covered?
   - Do tests follow the repository’s existing test style and fixture patterns?

4. Repository standards
   - Does the code follow the repo’s formatting, linting, typing, naming, dependency, and documentation conventions?
   - Are migrations, configuration changes, changelog entries, or docs needed?

5. Maintainability
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
