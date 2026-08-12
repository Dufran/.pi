---
description: Proofread text or a file with the low-cost proofreader subagent
argument-hint: <text, file path, or note reference>
subagent: proofreader
fresh: true
---

Proofread the following text or target conservatively. Correct spelling, grammar, punctuation, capitalization, agreement, and obvious typographical errors while preserving meaning, voice, terminology, Markdown, YAML, wiki-links, URLs, citations, code, and quoted text.

If given a file path, edit that file in place. If given text directly, return the corrected text. If this template is running in the parent session, delegate the task to the `proofreader` subagent. If it is already running inside that subagent, perform the proofreading directly. Do not fact-check, summarize, reorganize, or broadly rewrite unless explicitly requested.

Text or target:

$@
