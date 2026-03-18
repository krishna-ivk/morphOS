# JobOps Setup Guide For Your Search

This guide is based on `DaKheera47/job-ops` release `0.2.0` from March 17, 2026.

## What JobOps can automate

- scrape jobs from LinkedIn, Indeed, Glassdoor, Adzuna, Hiring Cafe, Gradcracker, and UK Visa Jobs
- score jobs against your profile
- tailor resume PDFs for strong matches
- track recruiter emails in Gmail after you apply

## What it does not automate

- submitting applications for you
- optimizing your public LinkedIn profile directly
- replacing the need for a strong base resume

## Best setup path

### 1. Build your base resume first

JobOps works best when your resume is already structured and up to date.

Recommended source of truth:

1. Fill `profile-source-of-truth.md`
2. Create or refresh a base resume in RxResume
3. Make sure the resume includes:
   - clear headline
   - strong summary
   - updated experience bullets
   - projects section with relevant projects, even if some are hidden by default
   - LinkedIn and GitHub profile links

### 2. Launch JobOps

```bash
git clone https://github.com/DaKheera47/job-ops.git
cd job-ops
docker compose up -d
```

Then open:

- Dashboard: `http://localhost:3005`

## Onboarding choices that matter most

### LLM provider

Use whichever model provider you trust for resume and scoring quality.

Strong default choice:

- OpenAI or OpenRouter with a reliable fast model for scoring and tailoring

### Reactive Resume

JobOps uses RxResume as the base resume source.

Recommended:

- use RxResume v5 with an API key if possible

You will need to configure:

- `rxresumeMode`
- `rxresumeUrl` if self-hosting RxResume
- `rxresumeApiKey` for v5, or email and password for v4

### Gmail tracking

If you want automatic status tracking after applying, configure Google OAuth and connect Gmail from the Tracking Inbox page.

Required environment variables:

- `GMAIL_OAUTH_CLIENT_ID`
- `GMAIL_OAUTH_CLIENT_SECRET`
- `GMAIL_OAUTH_REDIRECT_URI`

Local callback:

- `http://localhost:3005/oauth/gmail/callback`

## Suggested first-run settings

Start conservative while tuning.

- sources:
  - `linkedin`
  - `indeed`
- discovery size:
  - 30 to 50 jobs
- tailoring threshold:
  - start around the score where roles feel obviously relevant
- tailored jobs count:
  - 5 to 10

## Suggested search logic

Use your target titles and filters from `profile-source-of-truth.md`.

Example search inputs:

- target titles:
  - `Backend Engineer`
  - `Software Engineer`
  - `Full Stack Engineer`
- must-have keywords:
  - `TypeScript`
  - `Node.js`
  - `React`
- exclude keywords:
  - `senior manager`
  - `principal`
  - `security clearance`

## LinkedIn-specific advice

JobOps can scrape LinkedIn jobs, but LinkedIn profile quality still matters for the human part of your search.

Make sure your LinkedIn:

- headline matches the titles you are searching
- About section contains measurable wins
- featured links point to proof of work
- top skills align with target roles

## Weekly operating rhythm

### Daily

- run a small pipeline
- review discovered jobs
- advance only strong matches to ready
- apply manually
- mark applied jobs in JobOps

### Weekly

- refresh LinkedIn headline or About if your targeting changes
- add new projects or wins to your base resume
- tune JobOps scoring filters based on false positives

## Most important quality rule

The automation is only as good as the profile it scores against. Spend the first hour on profile clarity, and the following weeks get much easier.
