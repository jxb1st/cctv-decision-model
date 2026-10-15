# Architecture figures

Run `python3 scripts/build_architecture_figures.py` from the repository root to regenerate the three SVG diagrams and their mobile variants. No third-party packages are required. The diagrams use schematic frames and illustrative scores, not private CCTV footage or additional experimental predictions.

The architecture corresponds to `thaitea/laya-vision` at revision `f2fe3c12cb6d04c59d8a190250bf3fb40fc828dc`. Sources are linked next to the figures in `index.html`; the training settings come from this page's reported experiment. The diagrams distinguish parameter reduction from avoiding answer generation and do not claim that output probabilities are automatically calibrated.

`index.html` selects mobile diagrams at widths up to 640 px. The native dialog supports expanding a figure, closing it with Escape, and returning focus to its button. Each figure also links to a standalone desktop SVG for presentation use.

This repository publishes static files from `main` through GitHub Pages. If the upstream experiment's `build_page.py` regenerates the page, preserve or port the architecture sections, dialog script, CSS rules, and source links added here.
