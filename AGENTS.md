# AGENTS.md

## Portfolio architecture
- Keep `index.html` as a thin shell. Do not move section copy back into it.
- Homepage sections live in `components/*.html` and are loaded by `js/includes.js`.
- Preserve IDs such as `#work`, `#experience`, and `#about`; deep-link scrolling depends on them.
- Keep homepage copy concise, factual, and engineering-focused. Avoid slogan-like or generic AI/marketing language.
- After homepage CSS, component, JS, or index changes, use the `Portfolio visual capture` workflow and inspect desktop/mobile screenshots.
- The screenshot workflow must fail if modular includes do not finish loading.
