-- PlaqueCheck AI | research feedback only. Do not insert actual patient information.
-- Run once using Supabase Dashboard > SQL Editor (new project).
create extension if not exists pgcrypto;

create table if not exists public.preview_feedback (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  app_version text not null check (app_version = '0.4-community'),
  scenario text not null check (scenario in ('fictional_stable','fictional_minimal','fictional_acute','custom_synthetic')),
  reviewer_role text not null check (reviewer_role in ('cardiologist','physician','researcher','engineer','other')),
  helpfulness text not null check (helpfulness in ('useful','unclear','not_useful')),
  assessment_alignment text not null check (assessment_alignment in ('agree','partly','disagree','not_qualified')),
  suggested_pathway text not null check (suggested_pathway in ('need_more_info','specialist_review','consider_noninvasive','consider_invasive','not_qualified')),
  improvement_area text not null check (improvement_area in ('none','unsafe_triage','equation','missing_inputs','explanation','other'))
);

alter table public.preview_feedback enable row level security;
-- Restrict direct access: public users may submit one row, but cannot list, modify or delete feedback.
revoke all on table public.preview_feedback from public, anon, authenticated;
grant insert on table public.preview_feedback to anon, authenticated;

drop policy if exists "submit_structured_feedback" on public.preview_feedback;
create policy "submit_structured_feedback" on public.preview_feedback
  for insert to anon, authenticated
  with check (
    app_version = '0.4-community'
    and scenario in ('fictional_stable','fictional_minimal','fictional_acute','custom_synthetic')
  );

-- IMPORTANT: There are deliberately NO SELECT/UPDATE/DELETE policies.
-- Review data in the Supabase Dashboard as a project administrator.
-- Public insert endpoints can be abused. Add Turnstile + a rate-limited Edge Function
-- or authenticated reviewer access BEFORE large-scale recruitment.
-- Healthcare data must use a separate private, approved and consented research system.
