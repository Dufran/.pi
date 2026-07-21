# Adaptable AI configuration templates

These templates provide structure only. Replace every placeholder with repository evidence and omit irrelevant sections.

## Root `AGENTS.md`

```markdown
# Repository agent guide

> `AGENTS.md` is the source of truth for repository AI guidance. Tool-specific
> files are thin adapters only.

## Repository map

- `<path>/` — <ownership and responsibility>

## Context-aware guidance

- Changes under `<backend path>/` also follow `<backend path>/AGENTS.md`.
- Changes under `<frontend path>/` also follow `<frontend path>/AGENTS.md`.

## Toolchain and command policy

- Runtime/package-manager pins: <verified versions and files>.
- Run commands through `<canonical wrapper>` from `<working directory>`.
- Do not use alternate wrappers or global tools when a canonical command exists.

## Setup and checks

```bash
<safe setup command>
<check-only lint command>
<type-check command>
<focused/full test commands>
<build command where relevant>
```

## Architecture and contracts

- <verified dependency direction and public-contract rules>

## Database, production, and secrets

- Use disposable local/test resources only.
- Never run production, deployment, restore, release, or destructive commands
  without an explicit human request and approval.
- Never read, print, copy, or commit real environment files or credentials.

## Generated files

- `<generated path>` comes from `<source>` via `<command>`; do not hand-edit it.

## Definition of done

- Make the smallest relevant change and inspect the final diff.
- Report changed files, migrations/generated files, exact checks/results, skipped
  checks, assumptions, and residual risks.
```

## Scoped backend `AGENTS.md`

```markdown
# Backend agent guide

> Root repository rules also apply. This file contains backend-only deltas.

## Stack and ownership

- <verified runtime/framework/database/test runner>
- <apps/packages and dependency boundaries>

## Commands

```bash
<backend install/check/type/test/schema commands>
```

## Django/API safety

- Use the configured test runner; do not assume pytest.
- Model changes require a new reviewed migration through the project wrapper.
- Never edit an applied migration or access a production database.
- API changes test authentication, authorization, object/tenant isolation,
  invalid input, success, schema output, and query behavior where relevant.
- Do not weaken CSRF, CORS, hosts, TLS, cookies, validation, authentication, or
  permissions to pass tests.

## Generated outputs

- <schema/client/docs outputs and commands>
```

## Scoped frontend `AGENTS.md`

```markdown
# Frontend agent guide

> Root repository rules also apply. This file contains frontend-only deltas.

## Stack and architecture

- <verified Node/package manager, framework, router, state/data, UI, i18n>

## Commands

```bash
<immutable install/check/type/test/build/codegen commands>
```

## Frontend rules

- Keep configured TypeScript strictness and lint/accessibility rules enabled.
- Follow the existing routing, state, generated-client, UI, and i18n patterns.
- Do not use broad `any`, blanket ignores, or disabled checks to pass validation.
- State browser/E2E requirements only when the repository contains that tooling.

## Generated outputs

- <generated API/routes/models and source commands>
```

## Claude adapter

Root `CLAUDE.md`:

```markdown
@AGENTS.md
```

Nested adapter, only when needed:

```markdown
@AGENTS.md
```

## Copilot commit-message-only configuration

`.vscode/settings.json` fragment:

```json
{
  "github.copilot.chat.commitMessageGeneration.instructions": [
    {
      "file": ".github/copilot-commit-message-instructions.md"
    }
  ]
}
```

`.github/copilot-commit-message-instructions.md`:

```markdown
Generate a commit message only from the supplied/staged diff.

Output only the commit message. Follow Conventional Commits:

<type>(<optional-scope>): <imperative subject>

<optional body>

<optional footer>

- Use only types recognized by this repository's release configuration: <types>.
- Prefer scopes used by this repository: <scopes>. Omit scope when no scope fits.
- Keep the subject concise and every line within 72 characters.
- Explain why in the body when it adds useful context.
- Use `BREAKING CHANGE:` only when the diff proves a breaking change.
- Do not invent issue IDs, tickets, authors, test results, or behavior not shown
  by the diff.
```

When this mode is selected, do not add `.github/copilot-instructions.md`.

## Configuration audit report

```markdown
## Repository profile
- Root: <path>
- Stack: <verified summary>
- Supported tools: <tools and evidence/user decision>
- Canonical instructions: <path>

## Changes
### Created
- <file and purpose>
### Updated
- <file and correction>
### Removed/deactivated
- <file and reason>
### Kept
- <file and reason>

## Validation
- `<command>` — <result>
- Static checks — <result>

## Residual risks / decisions
- <unresolved item>
```
