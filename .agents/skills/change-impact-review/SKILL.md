---
name: change-impact-review
description: Find concrete breakage caused by changed contracts, symbols, data flows, side effects, or duplicated implementations that were not updated consistently.
allowed-tools: Read Grep Glob
---

Review the changed code for cross-codebase impact. This is an inexpensive, focused impact review—not a general style review and not a request to summarize the diff.

For each behaviorally meaningful change, identify affected symbols, contracts, data shapes, events, configuration, side effects, and persistence behavior. Search the repository for:

- Direct callers, consumers, imports, registrations, overrides, and implementations.
- Indirect dependents such as serializers, API or UI clients, background jobs, signals and hooks, permissions, caches, reports, fixtures, migrations, and tests.
- Similar or duplicated flows implementing the same behavior elsewhere.
- Assumptions in unchanged code that the new behavior invalidates.

Follow dependency paths across module and application boundaries far enough to establish concrete impact. Inspect nearby conventions and tests where they help prove compatibility or breakage.

Report a finding only when repository evidence shows that an unchanged dependent, analogous flow, fixture, migration, configuration entry, or test now requires a corresponding update. Do not report a location merely because it references changed code. Do not produce speculative hardening advice, generic summaries, or standalone context notes.

For every finding, provide:

- The changed contract or behavior and the affected dependent location.
- The concrete incompatibility or missing propagation.
- The user, runtime, data, or maintenance consequence.
- A focused correction, including the other locations that must change together.

Prefer no finding over an unproven dependency concern. Cite exact paths and lines wherever possible.
