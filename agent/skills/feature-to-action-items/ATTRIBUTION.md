# Attribution

This skill incorporates and adapts planning concepts from Matt Pocock's `to-tickets` skill, including tracer-bullet slicing, explicit blocking edges, a granularity review checkpoint, and expand–contract handling for wide refactors.

Source: [mattpocock/skills — engineering/to-tickets](https://github.com/mattpocock/skills/tree/main/skills/engineering/to-tickets)

Upstream revision inspected: `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76`

The upstream repository is licensed under the MIT License:

> MIT License
>
> Copyright (c) 2026 Matt Pocock
>
> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all
> copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
> SOFTWARE.

## Intentional differences

- Output remains Markdown-only; no tracker setup, Jira connection, labels, or publishing.
- Repository citations are retained for verified current-state facts.
- Vertical slices are preferred by default, but evidence-backed frontend/backend ownership slices remain supported.
- Prefactoring becomes a separate blocker only when repository evidence shows it is necessary.
- Requirement normalization, traceability, codebase evidence, contract analysis, and ambiguity handling come from this custom skill.
