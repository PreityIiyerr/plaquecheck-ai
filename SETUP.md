# PlaqueCheck AI — 15-minute setup tutorial

## Part 1. Test it locally
1. Download the `PlaqueCheck_GitHub_Ready.zip` package and unzip it.
2. Double-click `index.html` in Chrome/Edge.
3. Click **Load stable demo** → **Run assessment**. Only fictional data is supplied.
4. Review PROMISE / RF-CL / ML results. They are **different research endpoints**, not angiography recommendations.

## Part 2. Create Supabase feedback storage
1. Sign up at https://supabase.com and choose **New project**.
2. Name it `plaquecheck-feedback` and keep it separate from any clinical patient database.
3. Choose **SQL Editor** → **New query**. Paste the entire contents of `supabase/schema.sql`, then select **Run**.
4. Verify `preview_feedback` appears in Table Editor.
5. In Project Settings → API Keys copy **Project URL** and **publishable** API key. Do not use a secret/service-role key.
6. Open `config.js` in a text editor and put them between the quote marks. Save.
7. Reopen `index.html`. The Submit anonymous feedback button should become enabled.
8. Complete a fictional case feedback form; click Submit. In Supabase Table Editor, check the new row. **No patient parameters are uploaded.**
9. For broad public traffic, replace the public insert with an Edge Function protected by CAPTCHA and rate limits, then revoke anon INSERT.

## Part 3. Put source code on GitHub (no terminal)
1. Create a GitHub account or log in.
2. Download and unzip this repository package.
3. Go to https://github.com/new and enter repository name `plaquecheck-ai`, visibility **Public**, and choose **Create repository**. Leave README and license unchecked because they already exist in the package.
4. On the empty repo page, click **uploading an existing file**. Drag all unpacked project files and directories; confirm you see `index.html`, `README.md`, `config.js`, `supabase/schema.sql`, and `.github/workflows/checks.yml`. GitHub web upload may not preserve hidden folders on some systems; for a complete upload, use GitHub Desktop or the command-line instructions below.
5. Commit changes. Open **Settings → General** and enable Issues; collaborators can now fork, open issues and submit Pull Requests.
6. Before publishing, check that no `.env`, report PDFs, patient images or raw clinical Excel/CSV files were uploaded.

### More reliable GitHub upload — terminal
From the extracted project folder:
```bash
git init
git branch -M main
git add .
git commit -m "Open research preview and structured feedback"
gh auth login
gh repo create plaquecheck-ai --public --source . --remote origin --push
```
This requires Git and the GitHub CLI, installed and logged in. `gh repo create` creates a repository only after you authorise it in your own account.

## Part 4. Host the app free on Netlify
**Recommended:** Connect the newly created public GitHub repository to Netlify for automatic updates.
1. Sign in to https://app.netlify.com.
2. Choose **Add new project → Import from Git** → GitHub → `plaquecheck-ai`.
3. For a plain HTML app, set **Publish directory** to `.` (repository root); no build command is needed.
4. Click Deploy and open the URL shown in Netlify. This is the public preview URL.
5. Alternatively, go to https://app.netlify.com/drop and drop the extracted **`index.html` and `config.js` files in the same folder**. Connected feedback requires both files.
6. Test using fictional inputs; submit feedback and confirm it is stored in Supabase.
7. Add your URL to your GitHub repository About section and README.

## Part 5. Invite responsible collaborators
- Invite clinicians to critique the **methodology and mock scenarios**, not to use it for care.
- Invite engineers to test code, verify equations, improve UI and add automated tests.
- Ask reviewers to use Issues or structured feedback only, with no actual medical reports.

## Public-release checklist
- [ ] `index.html` opens and demos work in browser
- [ ] No preloaded real case, raw patient data or identifiers
- [ ] Visible "research-only / not a clinical decision tool" warning
- [ ] PROMISE coefficient caveat still visible
- [ ] Supabase project uses publishable key only and INSERT-only table
- [ ] No public SQL SELECT/UPDATE/DELETE on feedback
- [ ] New issue templates and contribution guidelines visible
- [ ] Test submission received in Supabase and no patient data sent
- [ ] Decide on a spam/rate-limit plan before broad public launch

**Not a clinical use authorisation:** Further clinical claims require prospective evaluation, regulatory review, security, consent, and a properly labelled clinical dataset.
