# Numerical reproducibility (C-3)

## 1. Generators run again

| script | seconds | file | result |
|---|---|---|---|
| generate_part_ix_datasets.py | 18 | square_root_psi_data.csv | identical |
| generate_part_ix_datasets.py | 18 | zeta_first_200_zeros.csv | identical |
| generate_part_ix_datasets.py | 18 | zero_gap_histogram.csv | identical |
| generate_part_ix_datasets.py | 18 | part_ix_dataset_summary.json | identical |
| generate_part_ix_datasets.py | 18 | support_doubling_envelope.csv | identical |
| generate_part_ix_datasets.py | 18 | zero_free_boundary_shapes.csv | identical |
| generate_part_ix_datasets.py | 18 | GLn_exponents.csv | identical |
| lorentzian_weil_inertia.py | 4 | weil_spline_inertia.csv | reproduced: row 58 generalized_gap_ratio: 3.837402530505506e-05 vs 3.837399480796375e-05 (agree to 6 digits) |
| lorentzian_weil_inertia.py | 4 | weil_component_signatures.csv | identical |
| lorentzian_weil_inertia.py | 4 | lorentzian_weil_summary.json | identical |
| lorentzian_weil_inertia.py | 4 | firewall_local_signatures.csv | identical |
| li_logconcavity.py | 1 | li_coefficients_logconcavity.csv | identical |
| A2_gap_numerics.py | 0 | A2_zeta_zeros_2000.csv | identical |
| A2_gap_numerics.py | 0 | A2_level_residuals.csv | identical |
| A2_gap_numerics.py | 0 | A2_abscissa_ledger.csv | identical |
| A2_gap_numerics.py | 0 | A2_archimedean_constants.json | identical |

## 2. Independent checks

- zeta ordinates 1–200 against mpmath.zetazero: max |difference| 4.99e-23 → PASS
- A2 ordinates (2000 stored): 41 sampled against mpmath.zetazero, max |difference| 0.00e+00 → PASS
- Guinand–Weil Gram matrices, 63 configurations (9 supports T × 7 dimensions N), as the book states them: n_-(B_N) = 1 in 63/63 and (N−1, 1, 0) in 45 (book: 45); n_-(W_N) = 0 in 63/63 and (N, 0, 0) in 39 (book: 39); pole plane P_N signature (1, 1) in 63/63 → PASS
- Table D.7 (first ten ordinates): 10/10 printed as in the file → PASS

**Result: PASS**
