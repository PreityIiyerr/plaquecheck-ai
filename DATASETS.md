# Dataset provenance and limitations

The public source contains **model coefficients**, not raw clinical datasets or real case reports.

- UCI Heart Disease (920 original patient records across centres): https://archive.ics.uci.edu/dataset/45/heart+disease
- Z-Alizadeh Sani (303, angiography-selected): https://archive.ics.uci.edu/dataset/412/z+alizadeh+sani
- PROMISE trial: published mathematical equations only; patient-level PROMISE records were **not** obtained: https://biolincc.nhlbi.nih.gov/studies/promise/
- RF-CL based on published Winther model and CardioLab/cadptp repository: https://github.com/CardioLab/cadptp (GPL-3.0).

The different models have different definitions and denominators. They cannot be averaged to produce a meaningful angiography decision percentage. Test metrics reported in README refer to internal held-out studies, not clinical qualification. Many training cohorts were selected for angiography, creating selection bias. The model has no trial demonstrating safe avoidance of invasive coronary angiography.

Do not publish any user-provided medical images or case data. Check dataset licences and permissions separately before reuse.
