#!/usr/bin/env python3
"""
Compare CHANGELOG.md between two Git branches and produce:
1. Exact changelog text present in the base branch but missing in the target branch.
2. A client-facing changelog from conventional commit-style entries in that difference,
   supplemented by conventional git commit subjects in target..base.

Usage:
    changelog_diff.py <branch-where-to-merge> <base-branch>
"""
from __future__ import annotations

import argparse
import difflib
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

CONVENTIONAL_RE = re.compile(
    r"^(?:[a-f0-9]{7,40}\s+)?"
    r"(?P<type>feat|fix|perf|refactor|docs|style|test|build|ci|chore|revert|security)"
    r"(?P<scope>\([^)]+\))?"
    r"(?P<breaking>!)?:\s+"
    r"(?P<description>.+)$",
    re.IGNORECASE,
)

CLIENT_FACING_TYPES = {
    "feat": "Added",
    "fix": "Fixed",
    "perf": "Improved",
    "security": "Security",
    "docs": "Documentation",
}

INTERNAL_TYPES = {"chore", "build", "ci", "test", "style", "refactor", "revert"}


@dataclass(frozen=True)
class MissingBlock:
    start_line: int
    end_line: int
    lines: tuple[str, ...]


@dataclass(frozen=True)
class ConventionalEntry:
    type: str
    scope: str
    breaking: bool
    description: str
    source: str


def run_git(args: list[str], *, cwd: Path | None = None, check: bool = True) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout


def repo_root() -> Path:
    try:
        return Path(run_git(["rev-parse", "--show-toplevel"]).strip())
    except RuntimeError as exc:
        raise SystemExit(f"Error: current directory is not inside a Git repository.\n{exc}")


def ensure_branch(branch: str, root: Path) -> None:
    try:
        run_git(["rev-parse", "--verify", f"{branch}^{{commit}}"], cwd=root)
    except RuntimeError as exc:
        raise SystemExit(f"Error: branch or revision not found: {branch!r}\n{exc}")


def find_changelog_path(branch: str, root: Path) -> str:
    files = run_git(["ls-tree", "-r", "--name-only", branch], cwd=root).splitlines()
    if "CHANGELOG.md" in files:
        return "CHANGELOG.md"
    for candidate in files:
        if candidate == "changelog.md":
            return candidate
    for candidate in files:
        if Path(candidate).name.lower() == "changelog.md":
            return candidate
    raise SystemExit(f"Error: no CHANGELOG.md/changelog.md found in {branch!r}.")


def read_file_at(branch: str, path: str, root: Path) -> str:
    try:
        return run_git(["show", f"{branch}:{path}"], cwd=root)
    except RuntimeError as exc:
        raise SystemExit(f"Error: could not read {path!r} from {branch!r}.\n{exc}")


def missing_blocks(target_text: str, base_text: str) -> list[MissingBlock]:
    """Return base-branch line chunks that do not appear in the target text."""
    target_lines = target_text.splitlines()
    base_lines = base_text.splitlines()
    matcher = difflib.SequenceMatcher(a=target_lines, b=base_lines, autojunk=False)
    blocks: list[MissingBlock] = []

    for tag, _a1, _a2, b1, b2 in matcher.get_opcodes():
        if tag not in {"insert", "replace"}:
            continue
        lines = tuple(base_lines[b1:b2])
        if not any(line.strip() for line in lines):
            continue
        blocks.append(MissingBlock(start_line=b1 + 1, end_line=b2, lines=lines))
    return blocks


def clean_possible_commit_line(line: str) -> str:
    line = line.strip()
    # Remove common markdown list/checklist/quote decorations.
    line = re.sub(r"^[>\s]*", "", line)
    line = re.sub(r"^(?:[-*+]\s+|\d+[.)]\s+)", "", line)
    line = re.sub(r"^\[[ xX]\]\s+", "", line)
    line = line.strip(" `*_\t")
    return line


def extract_conventional(lines: Iterable[str], source: str) -> list[ConventionalEntry]:
    entries: list[ConventionalEntry] = []
    for raw_line in lines:
        line = clean_possible_commit_line(raw_line)
        match = CONVENTIONAL_RE.match(line)
        if not match:
            continue
        entries.append(
            ConventionalEntry(
                type=match.group("type").lower(),
                scope=(match.group("scope") or "").strip("()"),
                breaking=bool(match.group("breaking")),
                description=match.group("description").strip(),
                source=source,
            )
        )
    return entries


def git_conventional_commits(target_branch: str, base_branch: str, root: Path) -> list[ConventionalEntry]:
    output = run_git(["log", "--format=%s", f"{target_branch}..{base_branch}"], cwd=root, check=False)
    return extract_conventional(output.splitlines(), f"git log {target_branch}..{base_branch}")


def dedupe_entries(entries: Iterable[ConventionalEntry]) -> list[ConventionalEntry]:
    seen: set[tuple[str, str, str, bool]] = set()
    result: list[ConventionalEntry] = []
    for entry in entries:
        key = (entry.type, entry.scope.lower(), normalize_description(entry.description), entry.breaking)
        if key in seen:
            continue
        seen.add(key)
        result.append(entry)
    return result


def normalize_description(description: str) -> str:
    description = re.sub(r"\s+", " ", description).strip()
    description = re.sub(r"\s*\(#\d+\)\s*$", "", description)
    return description.lower().rstrip(".")


def sentence_case(text: str) -> str:
    text = text.strip()
    if not text:
        return text
    return text[0].upper() + text[1:]


def client_sentence(entry: ConventionalEntry) -> str:
    desc = re.sub(r"\s*\(#\d+\)\s*$", "", entry.description).strip()
    desc = desc.rstrip(".")
    low = desc.lower()

    replacements = [
        (r"^(add|adds|added)\s+", "Added "),
        (r"^(implement|implements|implemented)\s+", "Added "),
        (r"^(support|supports|supported)\s+", "Added support for "),
        (r"^(fix|fixes|fixed)\s+", "Fixed "),
        (r"^(resolve|resolves|resolved)\s+", "Fixed "),
        (r"^(improve|improves|improved)\s+", "Improved "),
        (r"^(optimize|optimizes|optimized)\s+", "Improved "),
        (r"^(update|updates|updated)\s+", "Updated "),
        (r"^(remove|removes|removed)\s+", "Removed "),
    ]
    for pattern, prefix in replacements:
        if re.match(pattern, low):
            rendered = re.sub(pattern, prefix, desc, count=1, flags=re.IGNORECASE)
            break
    else:
        if entry.type == "feat":
            rendered = f"Added {desc}"
        elif entry.type == "fix":
            rendered = f"Fixed {desc}"
        elif entry.type == "perf":
            rendered = f"Improved {desc}"
        elif entry.type == "security":
            rendered = f"Improved security for {desc}"
        elif entry.type == "docs":
            rendered = f"Updated documentation for {desc}"
        else:
            rendered = sentence_case(desc)

    rendered = sentence_case(rendered)
    if entry.scope and entry.scope.lower() not in rendered.lower():
        rendered = f"{rendered} ({entry.scope})"
    if not rendered.endswith(('.', '!', '?')):
        rendered += "."
    return rendered


def grouped_client_changelog(entries: list[ConventionalEntry]) -> tuple[dict[str, list[str]], list[ConventionalEntry]]:
    groups: dict[str, list[str]] = {
        "Breaking changes": [],
        "Added": [],
        "Fixed": [],
        "Improved": [],
        "Security": [],
        "Documentation": [],
    }
    omitted: list[ConventionalEntry] = []

    for entry in entries:
        if entry.breaking:
            groups["Breaking changes"].append(client_sentence(entry))
            continue
        category = CLIENT_FACING_TYPES.get(entry.type)
        if category is None:
            omitted.append(entry)
            continue
        groups[category].append(client_sentence(entry))

    groups = {name: bullets for name, bullets in groups.items() if bullets}
    return groups, omitted


def render_missing(blocks: list[MissingBlock]) -> str:
    if not blocks:
        return "No changelog text from the base branch is missing in the target branch."

    parts: list[str] = []
    for idx, block in enumerate(blocks, start=1):
        line_label = f"base lines {block.start_line}-{block.end_line}"
        parts.append(f"--- missing block {idx} ({line_label}) ---")
        parts.extend(block.lines)
    return "\n".join(parts)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Return CHANGELOG.md text present in base branch but missing from target branch, plus client-facing notes.",
    )
    parser.add_argument("target_branch", help="Branch where changes will be merged / destination branch")
    parser.add_argument("base_branch", help="Branch that contains the changelog text to compare against")
    args = parser.parse_args(argv)

    root = repo_root()
    ensure_branch(args.target_branch, root)
    ensure_branch(args.base_branch, root)

    target_path = find_changelog_path(args.target_branch, root)
    base_path = find_changelog_path(args.base_branch, root)
    target_text = read_file_at(args.target_branch, target_path, root)
    base_text = read_file_at(args.base_branch, base_path, root)

    blocks = missing_blocks(target_text, base_text)
    missing_lines = [line for block in blocks for line in block.lines]

    changelog_entries = extract_conventional(missing_lines, f"{base_path} missing text")
    commit_entries = git_conventional_commits(args.target_branch, args.base_branch, root)
    entries = dedupe_entries([*changelog_entries, *commit_entries])
    groups, omitted = grouped_client_changelog(entries)

    print(f"# Changelog comparison: `{args.target_branch}` ← `{args.base_branch}`")
    print()
    print("## Compared files")
    print(f"- Target branch: `{args.target_branch}:{target_path}`")
    print(f"- Base branch: `{args.base_branch}:{base_path}`")
    print()
    print("## Missing changelog text")
    print()
    print("```markdown")
    print(render_missing(blocks))
    print("```")
    print()
    print("## Client-facing changelog")
    print()
    if groups:
        for category, bullets in groups.items():
            print(f"### {category}")
            for bullet in bullets:
                print(f"- {bullet}")
            print()
    else:
        print("No client-facing conventional commit entries were found in the changelog difference or git commit range.")
        print()

    print("## Conventional commit sources")
    print(f"- From missing changelog text: {len(changelog_entries)}")
    print(f"- From `git log {args.target_branch}..{args.base_branch}`: {len(commit_entries)}")
    if omitted:
        omitted_types = ", ".join(sorted({entry.type for entry in omitted}))
        print(f"- Omitted as internal/non-client-facing: {len(omitted)} ({omitted_types})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
