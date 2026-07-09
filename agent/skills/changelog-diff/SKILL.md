---
name: changelog-diff
description: Compare CHANGELOG.md across two Git branches. Use when asked to find changelog text present in a base/source branch but missing from the branch where changes will be merged, and to produce a client-facing changelog from conventional commit entries.
---

# Changelog Diff

Use this skill when the user asks for a changelog comparison between two Git branches, especially with wording like:

- “branch where to merge” / “target branch” / “destination branch”
- “base branch” / “source branch”
- “missing CHANGELOG.md text”
- “client-facing changelog”
- “conventional commits”

## Arguments

This skill expects exactly two arguments:

1. `branch_where_to_merge` — the target/destination branch that should receive changelog entries.
2. `base_branch` — the branch that already contains the changelog entries to compare against.

Interpretation:

- Return text that is present in `base_branch:CHANGELOG.md` but missing from `branch_where_to_merge:CHANGELOG.md`.
- Also return a client-facing changelog for the same branch difference, using conventional commit-style entries.

If either argument is missing or ambiguous, ask the user for the missing branch name before running commands.

## Safety rules

- Do **not** check out or switch branches.
- Do **not** edit files.
- Use `git show`, `git ls-tree`, and `git log` so the working tree stays untouched.
- Work from the current repository root. If the current directory is not inside a Git repository, explain that the skill must be run from the repository that contains `CHANGELOG.md`.
- Prefer root-level `CHANGELOG.md`; also accept `changelog.md` or another path whose basename is `CHANGELOG.md` if that is what the branch contains.

## Primary command

Run the bundled helper script with the two branch arguments:

```bash
python3 /Users/oleksandr.korol/.pi/agent/skills/changelog-diff/scripts/changelog_diff.py <branch_where_to_merge> <base_branch>
```

Example:

```bash
python3 /Users/oleksandr.korol/.pi/agent/skills/changelog-diff/scripts/changelog_diff.py main release/2026-07-06
```

The script prints:

1. Compared changelog files.
2. Exact missing Markdown text from the base branch.
3. A client-facing changelog grouped by change type.
4. Counts for conventional entries found in missing changelog text and in `git log branch_where_to_merge..base_branch`.

## Conventional commit handling

A conventional entry has this shape:

```text
<type>(optional-scope)!: description
```

Supported types:

- Client-facing by default: `feat`, `fix`, `perf`, `security`, `docs`
- Internal by default: `chore`, `build`, `ci`, `test`, `style`, `refactor`, `revert`

Breaking changes marked with `!` are always included under “Breaking changes”.

When generating the client-facing changelog:

- Rewrite commit-style descriptions into user-facing sentences.
- Group entries under clear headings such as `Added`, `Fixed`, `Improved`, `Security`, and `Documentation`.
- Deduplicate entries found both in the changelog diff and in git commit subjects.
- Mention if no client-facing conventional entries were found.

## Manual fallback

If the helper script cannot run, use this safe manual flow:

```bash
git rev-parse --show-toplevel
git rev-parse --verify '<branch_where_to_merge>^{commit}'
git rev-parse --verify '<base_branch>^{commit}'
git show '<branch_where_to_merge>:CHANGELOG.md' > /tmp/changelog-target.md
git show '<base_branch>:CHANGELOG.md' > /tmp/changelog-base.md
diff -u /tmp/changelog-target.md /tmp/changelog-base.md
git log --format='%s' '<branch_where_to_merge>..<base_branch>'
```

Then report:

1. Lines/blocks added on the base side of the diff as “missing changelog text”.
2. Conventional commit entries from those missing blocks and from the git log range.
3. A concise client-facing changelog from user-visible conventional commit types.
