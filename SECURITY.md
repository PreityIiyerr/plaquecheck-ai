# Security

- **Never commit** Supabase secret/service-role keys, medical records, real case export JSON or raw study datasets.
- A Supabase **publishable** key is public by design; RLS and database privileges are the protection. Do not use secret keys in `config.js`.
- The feedback table is INSERT-only for the public role and has no free-text columns.
- Add an authenticated Edge Function with rate limiting + bot mitigation before public-scale collection.
- Researchers must use a separate protected project for patient-level data.
- Report security bugs via a private GitHub security advisory; do not post exploit details to public issues.
