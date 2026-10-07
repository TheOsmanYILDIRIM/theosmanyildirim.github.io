# AGENTS.md

## Portfolio architecture
- Keep `index.html` as a thin shell. Homepage section copy lives in `components/*.html` and is loaded by `js/includes.js`.
- Homepage IDs such as `#work`, `#experience`, and `#about` must remain stable.
- Inner pages use the shared shell: `components/inner-header.html`, `components/inner-footer.html`, `css/site-shell.css`, and `js/site-shell.js`.
- Do not duplicate inner-page header/footer markup in individual pages.
- Copy must be concise, factual, and engineering-focused. Avoid slogans, generic marketing language, and unsupported claims.
- Preserve technical detail in thesis/stage content; simplify framing, not evidence.
- The thesis page opens as a short case study. Full report content remains inside the `#makale` disclosure.
- After any homepage or inner-page visual/content change, run `Portfolio visual capture` and inspect desktop/mobile fold + full-page screenshots.
- Visual capture must wait for modular includes/shared shell and retry while GitHub Pages is deploying.
