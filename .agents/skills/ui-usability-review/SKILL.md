---
name: ui-usability-review
description: Review changed React and web UI code for concrete usability, accessibility, interaction-state, and user-relevant metadata defects.
allowed-tools: Read Grep Glob
---

Review user-visible changes from an end-user UI and usability perspective using behavior established by the code and tests. This is a static review only. Do not launch the application, use browser automation, or infer visual/runtime behavior that the code does not establish.

First determine whether the change affects a user-visible interface or interaction. If it does not, return no findings.

For each affected flow, trace the user's goal, entry point, decisions, completion path, and recovery path. Follow relevant API responses, generated clients, types, props, context, selectors, hooks, state, event handlers, styles, and component branches into rendered output. Compare analogous screens and established design-system patterns.

Look for concrete defects in:

- Task completion, feedback, affordances, defaults, repeated actions, and destructive-action safeguards.
- Loading, empty, error, partial-data, stale-data, success, disabled, and permission-restricted states.
- User-relevant metadata: information required to understand status, make decisions, avoid mistakes, or complete the task that is available upstream but dropped or not meaningfully used.
- Native semantics, accessible names, keyboard operation, focus order and restoration, and announcements for dynamic changes.
- Responsive behavior established by styles, overflow, long or localized content, touch targets, reduced motion, and implementation evidence related to contrast.
- Missing interaction, state, responsive, or accessibility test coverage when the omission leaves changed behavior unprotected.

Report only evidence-backed, user-impacting issues. Do not demand that every technical field be displayed. Put concerns requiring manual runtime verification in the explanation instead of presenting them as confirmed defects.

For every finding, include the affected user/task, exact code evidence, why it matters, and a focused fix. Prefer no finding over speculation. Cite exact paths and lines wherever possible.
