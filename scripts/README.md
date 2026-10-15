# Architecture figures

Run `python3 scripts/build_architecture_figures.py` from the repository root to regenerate the four SVG diagrams and their mobile variants. No third-party packages are required. The diagrams use schematic frames and illustrative scores, not private CCTV footage or additional experimental predictions.

Run `python3 scripts/build_finetuning_figures.py` to regenerate the two fine-tuning diagrams and their mobile variants. They show the reported XML-to-frame target rule and partial model update loop. Sample times, frames and probability bars are illustrative, and the question labels are conceptual examples rather than exported training records. The single-frame L3 setting is kept distinct from the proposed temporal extension. The upstream loss at `r33drichards/laya-vision@9e1e241` is linked separately from the reported CCTV run: its exact loss coefficients and schedule were not audited. Temperature fitting is shown as a separate step, with the report's poor calibration outcome retained.

The introductory model map distinguishes Jev's hosted service, Laya's independent compatible implementation, and Laya-Vision's code fork. Its dashed connection denotes interface compatibility, not shared weights or an official open-source Jev release. The solid arrow denotes a code extension. The highlighted CCTV path uses only Laya-Vision. Sources are linked below the figure; Laya's 421M/322M labels refer to its English/multilingual text checkpoints.

The architecture corresponds to `thaitea/laya-vision` at revision `f2fe3c12cb6d04c59d8a190250bf3fb40fc828dc`. Sources are linked next to the figures in `index.html`; the training settings come from this page's reported experiment. The diagrams distinguish parameter reduction from avoiding answer generation and do not claim that output probabilities are automatically calibrated.

`index.html` selects mobile diagrams at widths up to 640 px. The native dialog supports expanding a figure, closing it with Escape, and returning focus to its button. Each figure also links to a standalone desktop SVG for presentation use.

This repository publishes static files from `main` through GitHub Pages. If the upstream experiment's `build_page.py` regenerates the page, preserve or port the architecture sections, dialog script, CSS rules, and source links added here.
