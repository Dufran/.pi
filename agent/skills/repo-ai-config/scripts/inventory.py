#!/usr/bin/env python3
"""Create a safe, content-free inventory for repository AI configuration audits."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


GUIDANCE_NAMES = {
    "AGENTS.md",
    "AGENTS.override.md",
    "CLAUDE.md",
    "CLAUDE.local.md",
}
SKIP_DIRS = {
    ".git",
    ".mypy_cache",
    ".next",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    ".yarn",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "vendor",
}
MANIFEST_NAMES = {
    ".node-version",
    ".nvmrc",
    ".python-version",
    "Cargo.lock",
    "Cargo.toml",
    "Gemfile",
    "Gemfile.lock",
    "Makefile",
    "Pipfile",
    "Pipfile.lock",
    "Taskfile.yml",
    "Taskfile.yaml",
    "bun.lock",
    "bun.lockb",
    "deno.json",
    "deno.jsonc",
    "go.mod",
    "go.sum",
    "package-lock.json",
    "package.json",
    "pnpm-lock.yaml",
    "poetry.lock",
    "pyproject.toml",
    "requirements.txt",
    "taskfile.yml",
    "taskfile.yaml",
    "uv.lock",
    "yarn.lock",
}
SENSITIVE_NAMES = {
    ".netrc",
    ".npmrc",
    ".pypirc",
    "credentials.json",
    "secrets.json",
}
SAFE_ENV_SUFFIXES = {".example", ".sample", ".template"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root or a path inside it")
    return parser.parse_args()


def git_output(root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-c", "core.fsmonitor=false", "-C", str(root), *args],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (FileNotFoundError, subprocess.SubprocessError):
        return None
    return result.stdout.strip()


def resolve_root(candidate: Path) -> tuple[Path, bool]:
    candidate = candidate.expanduser().resolve()
    git_root = git_output(candidate, "rev-parse", "--show-toplevel")
    if git_root:
        return Path(git_root).resolve(), True
    return candidate, False


def should_skip(path: Path, root: Path) -> bool:
    try:
        relative = path.relative_to(root)
    except ValueError:
        return True
    return any(part in SKIP_DIRS for part in relative.parts)


def relative_paths(paths: list[Path], root: Path) -> list[str]:
    return sorted({path.relative_to(root).as_posix() for path in paths})


def inventory(root: Path, is_git: bool) -> dict[str, Any]:
    guidance: list[Path] = []
    manifests: list[Path] = []
    workflows: list[Path] = []
    docs: list[Path] = []
    sensitive: list[Path] = []
    symlinks: list[Path] = []

    for path in root.rglob("*"):
        if should_skip(path, root):
            continue
        if path.is_symlink():
            symlinks.append(path)
            continue
        if not path.is_file():
            continue

        relative = path.relative_to(root)
        relative_text = relative.as_posix()

        if path.name in GUIDANCE_NAMES:
            guidance.append(path)
        elif relative_text.startswith(".claude/rules/"):
            guidance.append(path)
        elif relative_text == ".claude/settings.json":
            guidance.append(path)
        elif relative_text.startswith(".cursor/rules/"):
            guidance.append(path)
        elif relative_text.startswith(".github/instructions/"):
            guidance.append(path)
        elif relative_text.startswith(".github/prompts/"):
            guidance.append(path)
        elif relative_text.startswith(".github/") and "copilot" in path.name.lower():
            guidance.append(path)
        elif relative_text in {".vscode/settings.json", ".idea/ai-instructions.xml"}:
            guidance.append(path)

        if path.name in MANIFEST_NAMES or path.name.lower().startswith("taskfile"):
            manifests.append(path)

        if relative_text.startswith(".github/workflows/"):
            workflows.append(path)

        if path.name in {"README.md", "CONTRIBUTING.md", "CODEOWNERS"}:
            docs.append(path)
        elif relative_text.startswith("docs/") and path.suffix.lower() == ".md":
            docs.append(path)

        is_non_example_env = path.name.startswith(".env") and not any(
            path.name.endswith(suffix) for suffix in SAFE_ENV_SUFFIXES
        )
        if (
            is_non_example_env
            or path.name in SENSITIVE_NAMES
            or path.suffix.lower() in {".key", ".pem", ".p12", ".pfx"}
        ):
            sensitive.append(path)

    top_level_directories = sorted(
        path.name
        for path in root.iterdir()
        if path.is_dir() and path.name not in SKIP_DIRS and not path.name.startswith(".")
    )

    result: dict[str, Any] = {
        "repository_root": str(root),
        "git_repository": is_git,
        "commit": git_output(root, "rev-parse", "HEAD") if is_git else None,
        "git_status": git_output(root, "status", "--short") if is_git else None,
        "top_level_directories": top_level_directories,
        "ai_guidance_files": relative_paths(guidance, root),
        "manifests_and_task_files": relative_paths(manifests, root),
        "ci_workflows": relative_paths(workflows, root),
        "documentation_entry_points": relative_paths(docs, root),
        "sensitive_files_present_do_not_read": relative_paths(sensitive, root),
        "symlinks_skipped_do_not_follow": relative_paths(symlinks, root),
    }
    return result


def main() -> int:
    args = parse_args()
    root, is_git = resolve_root(Path(args.root))
    if not root.is_dir():
        raise SystemExit(f"Repository path is not a directory: {root}")

    print(json.dumps(inventory(root, is_git), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
