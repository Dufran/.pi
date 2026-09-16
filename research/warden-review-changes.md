# Research: Migrating Pi `review-changes` to Sentry Warden

## Summary
Warden is a skill-based, diff/hunk-oriented reviewer, not a general multi-agent chain runner. It can run separate repository-aware skills with **explicit main-agent models per skill or trigger**, so a cheaper scout-like *independent* skill and a stronger UI/final-review skill are supported. It cannot, from the verified `warden.toml` schema and docs, express Pi's ordered `scout -> ui-reviewer -> reviewer` workflow, write a named intermediate artifact, or inject one skill's output into the next; therefore a literal migration is not supported.

**Recommendation:** retain the Pi chain when the evidence handoff and one consolidated prose review are essential. Add Warden as a complementary local/PR diff-review layer: implement independent `change-context`, `ui-usability-review`, and engineering/final-review skills; use cheap/strong models at the **skill** level; keep `[runner].concurrency = 1` only to reduce concurrent hunk work, not to create stages. Treat Warden's combined structured findings as the closest final output, or perform a separate external consolidation step outside Warden.

## Findings

1. **Claim: Warden's configuration supports a model override for each skill and each trigger. This is the supported way to put the scout-like and UI/final reviewers on different main-agent models.** **Sources:** [Models and Runtimes](https://warden.sentry.dev/config/models/), [config schema](https://raw.githubusercontent.com/getsentry/warden/main/packages/warden/src/config/schema.ts). **Support:** direct evidence. **Confidence:** high.
   - Exact Pi syntax is `provider/<provider-specific-model-id>`, e.g. `model = "openai/gpt-5.5"`; Warden splits at the first `/`, so the model ID may itself contain slashes. Credentials conventionally use `WARDEN_{PROVIDER}_API_KEY` (native provider key variables also work). The runtime is global: `[defaults] runtime = "pi"`; it cannot be selected per skill/trigger.
   - Main-agent precedence is: `[[skills.triggers]].model` > `[[skills]].model` > `[defaults.agent].model` > legacy `[defaults].model` > CLI `--model` > `WARDEN_MODEL` > runtime default. Thus a skill/trigger override is explicit and wins over a workflow environment model.
   - For `runtime = "claude"`, model IDs are Claude Code model IDs without the Pi provider prefix. `runtime` is a config-layer-global choice.

2. **Claim: “Every workflow stage/agent can select a model” is only partly true.** **Sources:** [Models and Runtimes](https://warden.sentry.dev/config/models/), [config schema](https://raw.githubusercontent.com/getsentry/warden/main/packages/warden/src/config/schema.ts). **Support:** direct evidence. **Confidence:** high.
   - Warden distinguishes model *lanes*, not named workflow agents: `defaults.agent.model` (repo-aware skill analysis), `defaults.auxiliary.model` (structured extraction/repair/merge/dedupe/fix-evaluation helpers), and `defaults.synthesis.model` (post-analysis synthesis/consolidation). `synthesis` falls back to `auxiliary` if unset.
   - Only the **main agent** has skill- and trigger-level model overrides. The docs explicitly say auxiliary/synthesis lanes only come from their global defaults and do **not** inherit skill/trigger model overrides. Consequently a stronger `final-review` *skill* can be selected with `[[skills]].model`, but a separate stronger per-skill “synthesis/finalizer lane” cannot.
   - `effort` is independent of model. Agent effort accepts `off|low|medium|high|xhigh|max`; `--effort` overrides only the local main-agent lane. Auxiliary effort applies to Pi helper calls; Claude structured helpers currently ignore it.

3. **Claim: The closest Warden primitive to a Pi agent prompt is a custom Skill, not a chain stage.** **Sources:** [Writing Skills](https://warden.sentry.dev/skills/writing/), [Skills configuration](https://warden.sentry.dev/config/skills/), [prompt construction reference](https://github.com/getsentry/warden/blob/main/.agents/skills/agent-prompt/references/system-prompts.md). **Support:** direct evidence. **Confidence:** high.
   - A custom skill is `.agents/skills/<name>/SKILL.md` (also `.warden/skills` or `.claude/skills`) with YAML `name`, `description`, and `allowed-tools`, followed by the reviewer instructions. This is where the current three prompt bodies should be translated.
   - Warden builds a system prompt with the skill prompt and gives each analysis a per-hunk user prompt with code context/diff. It permits `Read`, `Grep`, and `Glob` for review exploration; analysis is forcibly read-only even if a skill declares edit/write tools. This supports local codebase/diff investigation but not edits from the review skills.
   - A UI specialist is supported as a **custom static-code-review skill** (e.g., React data flow, states, accessible names, keyboard/focus, responsive overflow, and test coverage). No first-party source establishes browser automation or visual-rendered UI review as a Warden feature; do not claim those capabilities. Use Sentry Snapshots separately if image-diff review is desired.

4. **Claim: Warden has local repository/diff access and a GitHub PR mode.** **Sources:** [README](https://github.com/getsentry/warden), [CLI run docs](https://warden.sentry.dev/cli/run/), [Triggers](https://warden.sentry.dev/config/triggers/). **Support:** direct evidence. **Confidence:** high.
   - `npx @sentry/warden` is documented as a pre-review of current-branch changes; `--base HEAD~3` and `--base origin/main` are documented ways to select historical/branch comparison. The local trigger type is `local`; PR trigger type is `pull_request`; scheduled scans are `schedule` and require `paths`.
   - This is not a proof that Warden exactly reproduces Pi's merge-base/upstream fallback and explicit inclusion/reporting of every untracked file. The migration should test that behavior on a fixture before retiring Pi's local-change review.

5. **Claim: Warden parallelism is concurrency of hunk analyses/trigger dispatch, not a directed workflow dependency mechanism.** **Sources:** [Runner configuration](https://warden.sentry.dev/config/runner/), [Action inputs](https://github.com/getsentry/warden/blob/main/action.yml), [config schema](https://raw.githubusercontent.com/getsentry/warden/main/packages/warden/src/config/schema.ts). **Support:** direct evidence. **Confidence:** high.
   - `[runner] concurrency = N` caps concurrent hunk analyses in CLI runs and matched trigger dispatch in GitHub Actions. CLI `--parallel` overrides it; Action `parallel` is used when the runner setting is absent.
   - **Researcher inference:** Set `concurrency = 1` if rate/cost predictability matters, but this does not make skill B wait for, read, or summarize skill A. The published schema contains skills, triggers, defaults, runner, logs, and service—not `phase`, `reads`, `output`, `as`, `outputMode`, dependency, or handoff fields.

6. **Claim: Findings artifacts exist for reporting, but they are not chain handoff artifacts.** **Sources:** [GitHub Action definition](https://github.com/getsentry/warden/blob/main/action.yml), [split analyze/report artifact fix](https://github.com/getsentry/warden/pull/409). **Support:** direct evidence. **Confidence:** medium.
   - The Action exposes `findings-file`, a structured JSON findings path, and supports analyze/report uses in Sentry's own workflow. The cited change says split reporting replays settings and trigger rows from the analyze artifact.
   - No first-party documentation/schema found for a configuration-level “write `codebase-context.md`, then provide it to another Warden skill” primitive. An external GitHub Actions job could upload/download a separately generated markdown artifact, but that orchestration would be GitHub Actions/custom scripting—not Warden configuration.

7. **Claim: Invocation/migration surface is straightforward for independent skills, with important limitations.** **Sources:** [README](https://github.com/getsentry/warden), [Action definition](https://github.com/getsentry/warden/blob/main/action.yml), [Triggers](https://warden.sentry.dev/config/triggers/). **Support:** direct evidence. **Confidence:** high.
   - Local: `npx @sentry/warden` (or `warden` after installation); use `--skill <name>` for a targeted skill. Initialize with `npx @sentry/warden init`; add baseline skills with `npx @sentry/warden add code-review` / `security-review`.
   - PR: check out the repository and run `getsentry/warden@v0` with model-provider credentials. The Action accepts reporting/failure thresholds and `parallel`; it publishes inline eligible findings/checks. Configure matching `pull_request` actions in both workflow YAML and `warden.toml`.
   - Warden is not a drop-in parser for `agent/chains/*.chain.md` or `agent/prompts/*.md`; rewrite prompts as discrete skills and rewrite policy/configuration as `warden.toml` plus optional GitHub workflow.

## Closest viable configuration

The following is a **supported independent-skill design**, not a sequential chain. It demonstrates per-skill main-agent model selection and deliberately sets auxiliary/synthesis lanes globally. Replace IDs with models available to the configured providers/account; Warden requires the Pi provider prefix and the matching credential.

```toml
# warden.toml
version = 1

[defaults]
runtime = "pi"
# This is a global fallback, not a workflow-stage setting.

[defaults.agent]
model = "openai/gpt-5.5"
maxTurns = 30
effort = "medium"

# Helper/verification/merge work is global for the whole run.
[defaults.auxiliary]
model = "openai/gpt-5.5"
effort = "medium"
maxRetries = 3

# Global consolidation lane; it is not a custom final-review agent nor per-skill.
[defaults.synthesis]
model = "anthropic/claude-opus-4-5"

[runner]
# Limits hunk/trigger concurrency; it does not impose scout -> UI -> final order.
concurrency = 1

[[skills]]
name = "change-context"
model = "openai/gpt-5.5" # cheap scout-like independent analysis

[[skills.triggers]]
type = "local"

[[skills.triggers]]
type = "pull_request"
actions = ["opened", "synchronize", "reopened"]
draft = false

[[skills]]
name = "ui-usability-review"
model = "anthropic/claude-sonnet-4-6" # stronger UI specialist
paths = ["**/*.{tsx,jsx,css,scss}"]

[[skills.triggers]]
type = "local"

[[skills.triggers]]
type = "pull_request"
actions = ["opened", "synchronize", "reopened"]
draft = false

[[skills]]
name = "final-engineering-review"
model = "anthropic/claude-opus-4-5" # stronger independent final-like review

[[skills.triggers]]
type = "local"

[[skills.triggers]]
type = "pull_request"
actions = ["opened", "synchronize", "reopened"]
draft = false
```

Create `.agents/skills/change-context/SKILL.md`, `.agents/skills/ui-usability-review/SKILL.md`, and `.agents/skills/final-engineering-review/SKILL.md`, moving the appropriate Pi instructions into each. Do **not** include `{outputs.codebaseContext}` or `{outputs.uiReview}`: Warden has no verified substitution/handoff syntax. The final skill must independently inspect code/diff; it cannot receive the first two outputs.

Example CI invocation:

```yaml
- uses: actions/checkout@v4
- uses: getsentry/warden@v0
  with:
    parallel: "1"
  env:
    WARDEN_OPENAI_API_KEY: ${{ secrets.WARDEN_OPENAI_API_KEY }}
    WARDEN_ANTHROPIC_API_KEY: ${{ secrets.WARDEN_ANTHROPIC_API_KEY }}
```

## Contradictions
- **Apparent contradiction resolved:** the docs say Warden can use different models for “different stages,” but these are internal agent/auxiliary/synthesis lanes, not arbitrary named chain stages. The same docs simultaneously limit skill/trigger overrides to the main agent and say auxiliary/synthesis do not inherit them. A literal three-agent sequential model plan is therefore unsupported.
- **Documentation drift risk:** the README/search snippets have varied between Claude-centric and Pi-centric wording over releases. Use a version-pinned Action/CLI and validate the installed version's schema; the current first-party model docs and `main` schema are the basis for the exact syntax above.

## Missing evidence
- No verified first-party evidence that Warden includes untracked files with the exact Pi workflow semantics, or that it implements Pi's full merge-base/upstream fallback. Test this before migration.
- No verified Warden configuration primitive for named markdown outputs, `reads`, output aliases, sequential dependencies, or one model seeing a previous skill's raw output.
- No verified Warden browser/visual UI-test runner. Static UI specialist prompts are supported; rendered usability assertions need another tool/process.
- The `source_check` validation attempt returned **unclear** despite direct official docs/source supporting model-lane facts; this brief relies on the fetched first-party documentation and schema rather than treating the automated verdict as corroboration.

## Sources
- **Kept:** [Warden Models and Runtimes](https://warden.sentry.dev/config/models/) — exact model syntax, lane constraints, precedence, runtime/auth rules.
- **Kept:** [Warden configuration schema](https://raw.githubusercontent.com/getsentry/warden/main/packages/warden/src/config/schema.ts) — authoritative accepted-field inventory and constraints.
- **Kept:** [Warden Skills configuration](https://warden.sentry.dev/config/skills/) and [Triggers](https://warden.sentry.dev/config/triggers/) — skill/trigger primitives and overrides.
- **Kept:** [Warden Runner configuration](https://warden.sentry.dev/config/runner/) — concurrency semantics.
- **Kept:** [Writing Skills](https://warden.sentry.dev/skills/writing/) and [prompt construction reference](https://github.com/getsentry/warden/blob/main/.agents/skills/agent-prompt/references/system-prompts.md) — custom prompt/tool model.
- **Kept:** [Warden README](https://github.com/getsentry/warden), [CLI run docs](https://warden.sentry.dev/cli/run/), and [Action definition](https://github.com/getsentry/warden/blob/main/action.yml) — invocation, local/PR, Action artifact surface.
- **Kept:** [PR #409](https://github.com/getsentry/warden/pull/409) — limited evidence for analyze/report artifact behavior.
- **Rejected/deprioritized:** Sentry Seer Code Review documentation — first-party but a different product from open-source Warden; not evidence for Warden configuration.

## Next steps
1. Create the three skills in a throwaway branch and run `npx @sentry/warden --skill ... --base <base>` against fixtures containing committed, staged, unstaged, and untracked changes; compare with the Pi chain's context output.
2. Decide whether independent Warden findings are sufficient. If consolidated final prose and scout/UI evidence handoff are mandatory, keep the Pi chain (or build an explicit external orchestrator) rather than attempting unsupported TOML fields.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Concrete Warden migration findings, exact configuration syntax, limitations, and severity-style risks are recorded in research/warden-review-changes.md."
    }
  ],
  "changedFiles": [
    "/Users/oleksandr.korol/.pi/agent/sessions/--Users-oleksandr.korol-.pi--/subagent-artifacts/outputs/3a56513b-7099-42b5-8687-b8c59dcdfea2/research/warden-review-changes.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "Focused first-party Warden web/source research and schema inspection",
      "result": "passed",
      "summary": "Fetched official Warden docs, GitHub source schema, action definition, and repository workflow references."
    },
    {
      "command": "source_check for per-skill/per-trigger versus lane model selection",
      "result": "not-run",
      "summary": "Tool was invoked but returned unclear rather than a pass/fail validation; limitation disclosed in the brief."
    }
  ],
  "validationOutput": [
    "Brief written to the authoritative output path.",
    "No repository configuration was modified."
  ],
  "residualRisks": [
    "Warden local untracked-file and merge-base semantics are not verified as exact equivalents of the Pi chain.",
    "No native sequential artifact handoff/final consolidation workflow is verified."
  ],
  "noStagedFiles": true,
  "diffSummary": "Added one cited research brief only; existing configuration untouched.",
  "reviewFindings": [
    "high: Literal scout -> UI -> final migration is unsupported because verified Warden configuration lacks staged dependencies and skill-output handoffs.",
    "medium: Validate local diff/untracked behavior before retiring the existing Pi review chain."
  ],
  "manualNotes": "The source_check automated validation returned unclear; direct fetched first-party docs/schema provide the cited evidence."
}
```