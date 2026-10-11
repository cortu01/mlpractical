# Machine Learning Practical 2026/27 — Coursework 1

Coursework materials for the University of Edinburgh Machine Learning Practical course, on branch `mlp2026-27/coursework1`. The coursework uses PyTorch and the EMNIST Balanced dataset.

Coursework 1 is formative: complete the five experiments for Table 3, Figure 4, and draft answers to Questions 1, 2 and 4. Released Monday 12 October 2026; submission due 12:00 Friday 23 October 2026. See `MLP2026_27_CW1_Spec.pdf` on Learn for the full specification and submission instructions.

## Getting started

Use the Conda environment set up for the labs, with PyTorch, NumPy, Matplotlib and Jupyter installed. From the repository root, open the coursework notebook:

```bash
jupyter notebook notebooks/Coursework_1.ipynb
```

Edit your student number and answers in `report/mlp-cw1-questions.tex`, and add references to `report/ref.bib`. Build the report with:

```bash
cd report
latexmk -pdf mlp-cw1-template.tex
```

If `latexmk` is unavailable, run `pdflatex mlp-cw1-template`, `bibtex mlp-cw1-template`, then `pdflatex mlp-cw1-template` twice.

## Repository map

- `notebooks/` — PyTorch data loading, model building and training; start with `Coursework_1.ipynb`. Keep coursework experiment code alongside the notebook.
- `data/` — supplied EMNIST training, validation and test splits, plus diagnostic data.
- `report/` — LaTeX report template, question placeholders, bibliography and style files; start with `mlp-cw1-questions.tex`. `figures/` contains supplied and placeholder plots; `additional-latex-files/` contains fallback LaTeX packages.
- `notes/` — environment, lab and remote access guidance; start with `environment-set-up.md`.

This coursework branch uses the PyTorch notebook directly. The report styles retain their original `mlp2022` and ICML 2017 filenames.
