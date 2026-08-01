# Surgical Digital Twins — Living Review Repository

Companion repository for the review:

> Fang H, Wang Q. *Digital Twins and Virtual Iteration in Precision Surgery: A Computational
> Framework for Patient-Specific Image-Guided Modeling, Simulation, and Closed-Loop Optimization.*
> Submitted to Medical Image Analysis (2026).

## Contents

| Path | Description |
|---|---|
| `references.bib` | BibTeX library of all 162 included studies (citation order as in the manuscript) |
| `extraction/Supplementary_Table_S1.csv` | Structured extraction sheet: stage, specialty, method category, validation type, CEBM evidence level for every included study |
| `tables/` | Machine-readable CSVs of the 15 tables in the review (taxonomy, notation, quantitative performance, VVUQ template, benchmark proposal) |
| `figures/make_figures.py` | Python/matplotlib source code for Figures 1–10 (300 dpi, colorblind-safe palette) |

## The framework in one paragraph

A surgical digital twin is a patient-specific, dynamic, computational surrogate of a patient's
anatomy, physiology, and pathology, continuously updated by medical images and biosignals, and
capable of predicting responses to surgical interventions through **virtual iteration** — a
constrained bilevel optimization loop over a patient-specific forward model:

```
a*   = argmin_{a in A} E_{p(s,theta|y)}[ L(f_theta(s, a), a) ] + lambda * Risk(a),  s.t. g_i(a) <= 0
theta_{t+1} = argmin_theta d( f_theta(s_t, a_t), s_{t+1}^{obs} )
```

## Twin maturity scale (proposed)

| Level | Name | Definition |
|---|---|---|
| L1 | Static model | One-off patient-specific reconstruction; no updating |
| L2 | Dynamic visualization | Model refreshed by intraoperative imaging/tracking; no forward simulation |
| L3 | Predictive simulation | Forward simulation of candidate interventions on the patient model |
| L4 | Closed-loop optimization | Iterative plan optimization with feedback (virtual iteration) |
| L5 | Autonomously updating twin | Continuous assimilation keeping model and patient synchronized |

## Contributing

This is a living review. To propose additions or corrections, open an issue or pull request with:
(1) the full reference, (2) the extraction-sheet fields as in `Supplementary_Table_S1.csv`, and
(3) a one-sentence justification of relevance to image-guided surgical digital twins.
Updates are merged into the reference library and extraction sheet on a rolling basis.

## License

CC-BY 4.0. Please cite the review when reusing the taxonomy, maturity scale, or tables.
