# PlaqueCheck AI — open research preview

> **Goal:** Avoid unnecessary coronary angiography **without missing patients who genuinely need it**.
>
> **Status:** Experimental research prototype. **Not a medical device. Not for patient care or emergency triage.** No calibrated "proceed with angiography" probability has been validated.

PlaqueCheck AI is a static, browser-run research interface for exploring published coronary disease likelihood models and four separately trained experimental disease classifiers. It also shows PROMISE minimal-risk research estimates in selected stable fictional cases. The outputs refer to different endpoints; none can be interpreted as a clinical instruction to perform or avoid angiography.

### Quick start (zero accounts required)

Open `index.html` in Chrome/Edge. Use **Load stable demo**, **Load minimal-risk demo**, or **Load fictional acute demo**. Do not use actual patient information.

### What's inside

- `index.html`: self-contained prediction interface plus synthetic-case feedback form
- `config.js`: optional public Supabase project settings, initially blank
- `supabase/schema.sql`: structured anonymous feedback table with INSERT-only access
- `train*.py`, `requirements.txt`, model JSONs: reproducibility research artifacts
- `tests/check_bundle.py`: basic release-safety checks
- `SETUP.md`: non-coder deployment instructions
- `CONTRIBUTING.md`, `DATASETS.md`, `PRIVACY.md`, `SECURITY.md`: contribution and governance policies

### Configure Supabase

1. Create a new [Supabase](https://supabase.com/) project **for non-sensitive public feedback only**.
2. In **SQL Editor**, run [`supabase/schema.sql`](supabase/schema.sql).
3. Under Project Settings → API Keys, copy **Project URL** and the **publishable** key into `config.js`.
4. Open `index.html`. The Submit Feedback button becomes active if the client library is available.
5. Submit a **fictional** case feedback form. Confirm a row appears in Supabase Table Editor as owner. Normal site visitors cannot query the rows through RLS.

Never put a `secret` or `service_role` key in frontend code. This public insert endpoint needs bot protection and rate limiting before broad-scale outreach.

### Publish site and code

See [SETUP.md](SETUP.md). The repository should be **public** to enable issues and pull requests. Hosting and database resources must be connected under your own accounts; this ZIP does not publish any website or create any Supabase tables on your behalf.

### Verified limitations

- Six research calculations/models are not six independent clinical decision systems.
- No individual angiography necessity score is supplied.
- The PROMISE model has an unresolved published coefficient discrepancy; the interface displays a range when relevant. It is not a validated confidence interval.
- Predictive performance varies across clinical populations; current data cannot validate safe deferral of angiography.
- No patient document upload, OCR, real clinical data intake, telemetry or production access control.

### References

- [CardioLab/cadptp](https://github.com/CardioLab/cadptp) — GPL-3.0
- [UCI Heart Disease](https://archive.ics.uci.edu/dataset/45/heart+disease)
- [UCI Z-Alizadeh Sani](https://archive.ics.uci.edu/dataset/412/z+alizadeh+sani)
- [PROMISE data dictionary and study](https://biolincc.nhlbi.nih.gov/studies/promise/)
- [PRECISE statistical analysis plan](https://cdn.clinicaltrials.gov/large-docs/44/NCT03702244/SAP_001.pdf)

### Licensing

Code is distributed under [GPL-3.0](LICENSE) in recognition of the existing GPL-3.0 CardioLab model implementation. Third-party model methodologies and datasets retain their own rights and attribution requirements. This project does not redistribute restricted raw clinical records.
