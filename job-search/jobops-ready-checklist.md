# JobOps Ready Checklist

This checklist is tailored to your machine and the local copy at:

`/Users/shivakrishnayadav/Documents/skyforce/job-search/job-ops`

## Current status

- JobOps repo cloned locally: yes
- Node and npm available: yes
- Docker available: no
- Gmail OAuth configured: no
- RxResume configured: no
- LinkedIn / job-search targeting drafted: yes

## Step 1: Install Docker

JobOps `0.2.0` is currently documented as a Docker-first setup.

After Docker Desktop is installed, verify:

```bash
docker --version
docker compose version
```

## Step 2: Prepare environment values

Use:

- `/Users/shivakrishnayadav/Documents/skyforce/job-search/jobops.env.template`

and copy the values you want into:

- `/Users/shivakrishnayadav/Documents/skyforce/job-search/job-ops/.env`

## Step 3: Minimum viable first launch

These are the minimum pieces worth having for a useful first run:

- one LLM provider in the onboarding wizard
- one base resume in RxResume

Optional for later:

- Gmail OAuth
- Adzuna
- UK Visa Jobs
- public tracer links

## Step 4: Start JobOps

From the cloned repo:

```bash
cd /Users/shivakrishnayadav/Documents/skyforce/job-search/job-ops
docker compose up -d
```

Open:

- `http://localhost:3005`

## Step 5: Onboarding choices

Recommended defaults for your profile:

- target positioning:
  - `Senior AI Platform Engineer`
  - `Senior Data Engineer`
- first sources:
  - `linkedin`
  - `indeed`
- initial run size:
  - discovery `40`
  - threshold `70`
  - ready count `8`

## Step 6: Resume setup

Before running serious searches, make sure your RxResume base resume includes:

- your stronger LinkedIn-style summary
- measurable metrics where possible
- 2 to 4 projects or case studies
- LinkedIn and GitHub links

## Step 7: Gmail tracking

Only do this after the app is running locally.

Google Cloud callback for local setup:

- `http://localhost:3005/oauth/gmail/callback`

Required values:

- `GMAIL_OAUTH_CLIENT_ID`
- `GMAIL_OAUTH_CLIENT_SECRET`

## Step 8: First search run

Use the filters from:

- `/Users/shivakrishnayadav/Documents/skyforce/job-search/jobops-targeting-from-resume.md`

Start with just LinkedIn and Indeed, then expand later if the score quality looks right.

## Suggested next move

Once Docker is installed, the fastest path is:

1. Create `.env`
2. Start JobOps
3. Configure RxResume in the UI
4. Run a small search
5. Add Gmail tracking after that
