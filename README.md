# Pi coding agent configuration

## Local Warden review

The repository includes a local-only [Sentry Warden](https://warden.sentry.dev/) configuration with three independent review skills:

- `change-impact-review` uses `openai-codex/gpt-5.6-luna`.
- `ui-usability-review` uses `openai-codex/gpt-5.6-terra`.
- `engineering-review` uses `openai-codex/gpt-5.6-sol`.

Warden's auxiliary work uses Luna, while cross-location synthesis uses Sol. Skills run independently; this is not the sequential handoff provided by `agent/chains/review-changes.chain.md`.

Warden 0.48.0 loads Pi's existing authentication from the configured Pi agent directory, so these models reuse the local `openai-codex` login rather than requiring an OpenRouter API key.

Review current branch and working-tree changes:

```sh
yarn review
```

Review only staged changes:

```sh
yarn review:staged
```

Run one skill when a focused review is enough:

```sh
yarn warden --skill change-impact-review
yarn warden --skill ui-usability-review
yarn warden --skill engineering-review
```
