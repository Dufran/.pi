# Repository AI configuration assessment checklist

Use this checklist to assess evidence. Do not turn every unchecked item into a required file; apply only what fits the repository and supported tools.

## Discovery and scope

- Root instruction source of truth is explicit.
- Nested instructions exist only where subtree behavior differs.
- Instruction precedence and working directories are understandable.
- Tool-specific adapters are present only for intentionally supported tools.
- Stale legacy files such as `.cursorrules` are identified.
- Tool files do not contain several independent copies of the same policy.

## Factual accuracy

- Repository map matches current directories and applications/packages.
- Runtime and framework versions match pins/manifests/locks.
- Package managers and immutable install behavior are correct.
- Test runners match actual configuration; pytest is not assumed for Django and E2E is not claimed without a runner/tests.
- Architecture and routing descriptions match current code.
- Referenced paths and documentation exist.

## Commands and CI parity

- One canonical command interface is named.
- Commands are literal, valid, and specify the working directory.
- Setup, format check, lint, type check, focused tests, full tests, build, and code generation are covered when present.
- Check-only and auto-fix commands are distinguished.
- Duplicate task namespaces or wrappers do not silently disagree.
- Completion checks align with CI or differences are explained.
- Agents must report exact commands/results and skipped checks.

## Backend and database safety

- Local/test database scope is explicit.
- Production management, deployment, restore, destructive SQL, and `flush` are prohibited without explicit approval.
- Model changes require new reviewed migrations and appropriate checks.
- Applied migrations are not edited casually.
- Data migrations use project/framework-safe patterns.
- Production database engine differences are acknowledged.
- API changes cover authentication, authorization, object/tenant isolation, invalid input, schema compatibility, and query behavior.

## Frontend safety and quality

- Pinned Node/package-manager versions and lockfile are named.
- Strict type checking and configured lint/format tools remain enabled.
- Actual router/state/data-fetching/UI/i18n conventions are correct.
- Generated clients/routes/models are marked non-editable.
- Tests and browser/E2E availability are described accurately.
- Accessibility requirements reflect the tooling actually present.

## Generated files and dependencies

- Every committed generated artifact has a source and regeneration command.
- Build/cache/runtime artifacts are excluded from source edits.
- Lockfiles are changed only through the pinned package manager.
- New dependencies require justification and review.
- Agents do not hand-edit generated output.

## Secrets, permissions, and autonomous tools

- Instructions prohibit reading/printing/committing real environment and credential files.
- Agent worktrees use sanitized test configuration rather than symlinked real secrets.
- Shell permissions are least privilege; broad `task:*`, package-manager, or interpreter access is reviewed.
- Production/deployment/restore commands are denied externally, not only discouraged in prose.
- Network and MCP servers are disabled or narrowly enabled by need.
- Editor/agent tool auto-approval is disabled unless explicitly justified.
- Hooks do not run writing/fixing commands after every edit.
- Commands that print effective environments or task metadata are prohibited.
- Protected branches, independent CI, and human approval remain outside agent control.

## Maintainability

- Root guidance is concise enough to load reliably.
- Scoped files contain deltas rather than repeated root material.
- Generic framework tutorials are linked, not copied.
- Stale snapshots have an owner/review mechanism or are derived from stable facts.
- An audit can verify task names, versions, app/package lists, generated paths, and adapter imports.

## Definition of done

- The smallest relevant diff is required.
- Behavior changes require focused regression tests where practical.
- Public contracts and generated outputs are updated together.
- Final diff inspection is required.
- Final report includes changed files, migrations/generated files, command outcomes, omissions, assumptions, and residual risks.
