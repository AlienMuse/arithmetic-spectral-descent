# Numerical scripts and data — Arithmetic Spectral Descent

These are the scripts and data files that accompany *Arithmetic Spectral Descent* (Research Architecture Edition 1, version 1.0.0), by Vincent Liu.
They are licensed under the Apache License 2.0 (`LICENSE`); the monograph itself is licensed under CC BY-NC-ND 4.0.

The book reports every computation here as **finite evidence** (status label [E]); none of it is used as a premise
of a theorem. The Riemann Hypothesis remains open.

## Files

| file | what it is | book |
|---|---|---|
| `lorentzian_weil_inertia.py` | Guinand–Weil Gram matrices on cubic-spline test spaces (9 supports × 7 dimensions = 63 configurations): inertia of the full form, the pole plane and the pole-removed form; firewall table | Ch. 46, App. D |
| `weil_spline_inertia.csv`, `weil_component_signatures.csv`, `lorentzian_weil_summary.json`, `firewall_local_signatures.csv` | its output | Tables D.1–D.4 |
| `generate_part_ix_datasets.py` | ψ(X) − X, the first 200 zeta ordinates (mpmath, 25 digits), gap histogram, support-doubling envelope, zero-free boundary shapes, GL(n) exponents | Part IX, App. D |
| `square_root_psi_data.csv`, `zeta_first_200_zeros.csv`, `zero_gap_histogram.csv`, `support_doubling_envelope.csv`, `zero_free_boundary_shapes.csv`, `GLn_exponents.csv`, `part_ix_dataset_summary.json` | its output | Table D.7, figures of Part IX |
| `A2_gap_numerics.py` | k-fold Goldbach sums, level-1 explicit-formula term, normalised residuals, archimedean constants, abscissa ledger | App. J, Tables D.5–D.6 |
| `A2_zeta_zeros_2000.csv`, `A2_level_residuals.csv`, `A2_abscissa_ledger.csv`, `A2_archimedean_constants.json` | its output | |
| `li_logconcavity.py`, `li_coefficients_logconcavity.csv` | Li coefficients and their log-concavity | Ch. 47, 52 |
| `square_root_barrier_numerics.py` | the square-root barrier example (with `square_root_psi_data.csv`) | Ch. 8, 11 |
| `fig_13_30_data.py`, `fig_curve_builders.py` | data and curve plates of the figures (they write into a `figures/` folder next to `numerics/`) | figures |

## Reproduce

Python 3.11 with numpy, scipy and mpmath (tested: Python 3.11.9, numpy 2.0.0, scipy 1.17.1, mpmath 1.4.1). In this folder:

```sh
python generate_part_ix_datasets.py     # first: writes zeta_first_200_zeros.csv, used by the next script
python lorentzian_weil_inertia.py
python li_logconcavity.py
python A2_gap_numerics.py               # reuses A2_zeta_zeros_2000.csv when present
```

Every data file is then reproduced; `REPRODUCIBILITY.md` is the record of that check on the final edition (one
generalized eigenvalue ratio agrees to six significant digits, the LAPACK rounding of an ill-conditioned pencil;
every other value is identical).
