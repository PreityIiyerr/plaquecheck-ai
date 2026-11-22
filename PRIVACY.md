# Privacy and data handling

## Research preview
The application is static and calculates its results locally in the browser. The public ZIP and Git repository must not contain patient reports or the prior case study. The form is restricted to fictional/synthetic data.

## Optional feedback
If the owner configures Supabase, a submission sends only:
`app_version, scenario, reviewer_role, helpfulness, assessment_alignment, suggested_pathway, improvement_area`.
No patient fields, results, PDFs, email addresses or free-text notes are transmitted by the app. Infrastructure providers may retain network logs such as IP address; consult their privacy policies.

No analytics or tracking pixels are included. A public website host may keep normal access logs. The feedback database denies public reads by design, but its public insert endpoint remains vulnerable to spam. Add rate limiting/Turnstile and a server-side endpoint before wider release.

## Future clinical data
Do not extend this public feedback table to real cases. Actual patient-level datasets must require institutional ethics approval, legal consent/lawful basis, authenticated staff, access controls, encryption, retention limits, breach response and applicable Indian DPDP Act/medical-device compliance review.
