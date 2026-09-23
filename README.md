# Pi coding agent configuration

## Local Warden review

The repository includes a local-only [Sentry Warden](https://warden.sentry.dev/) configuration with three independent review skills:

- `engineering-review` uses `openai-codex/gpt-6-sol` and runs by default.
- `ui-usability-review` uses `openai-codex/gpt-5.6-terra` and runs by default for changed TSX, JSX, CSS, and SCSS files.
- `change-impact-review` uses `openai-codex/gpt-6-luna` and runs only when explicitly requested because its repository-wide analysis is expensive when repeated per diff hunk.

Warden's auxiliary and cross-location synthesis work use Luna. Main-analysis turn limits are capped at 8–10 turns, and up to four hunks run concurrently. Skills run independently; this is not the sequential handoff provided by `agent/chains/review-changes.chain.md`.

Warden 0.48.0 loads Pi's existing authentication from the configured Pi agent directory, so these models reuse the local `openai-codex` login rather than requiring an OpenRouter API key.

Review current branch changes:

```sh
yarn review
```

Review only staged changes:

```sh
yarn review:staged
```

Run one skill when a focused review is enough:

```sh
yarn review:impact
yarn review:ui
yarn review:engineering
```
