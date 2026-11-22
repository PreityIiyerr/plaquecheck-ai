"""Static sanity checks for the public, fictional-only release bundle."""
from pathlib import Path
p = Path(__file__).resolve().parents[1]
html = (p / 'index.html').read_text(encoding='utf-8')
sql = (p / 'supabase/schema.sql').read_text(encoding='utf-8')
assert 'Not a clinical decision tool.' in html
assert 'Angiography recommendation confidence' in html
assert 'Not established' in html
assert 'No real patient data' in html or 'no real patient data' in html.lower()
assert "from('preview_feedback').insert(payload)" in html
assert 'patient_data' not in html.lower()
assert 'for insert to anon, authenticated' in sql
assert 'grant insert on table public.preview_feedback' in sql
assert 'grant select' not in sql.lower()
assert all(not (p / name).exists() for name in ('heart_disease_uci.csv','Z-Alizadeh sani dataset.xlsx'))
print('Public release safety and structure checks passed')
