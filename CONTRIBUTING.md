# Contributing to PlaqueCheck AI

All code improvements, evidence reviews, tests and accessibility fixes are welcome.

1. Fork the public GitHub repository.
2. Make a branch (`git checkout -b fix/clinical-gate`).
3. Run `python3 tests/check_bundle.py` and `node --check` on JS extracted from index.html.
4. Open a pull request. State exactly which published equation, dataset or issue your change addresses.
5. Use **only fictional or synthetic data** in bug reports and PRs. Never upload medical documents or raw patient datasets.
6. For a prediction change, include endpoint definition, dataset lineage, split strategy, calibration, sensitivity/specificity, confidence intervals and clinical review.
7. High-risk/suspected acute presentations must continue to be gated from stable-case probability estimates.

## Suggested work
- Verify PROMISE equation against original calculator, resolve coefficient discrepancy.
- Test calibration and transportability across centres.
- Add independent, consented, de-identified outcome cohorts under approved study governance.
- Add accessibility and localisation tests.
- Design investigator-only data entry with ethics approval, authentication, audit logs and governance.

Not accepted: patient-identifying data, unvalidated clinical claims, arbitrary "angiography needed" percentages, or removing the research-use gate.
