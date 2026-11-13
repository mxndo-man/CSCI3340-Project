# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

**Primary:** undergraduate students, CS and engineering first, starting at UTRGV, who are applying to internships, often alongside a group of friends applying to the same programs. They come to find postings they're actually eligible for, keep track of deadlines, and share what they know with their group.

**Secondary:** the course instructor and classmates who judge the CSCI 3340 demo (final demo Mon Dec 7, 2026). They look at the product to see whether it works and solves a real problem.

## Product Purpose

Internship postings are scattered across dozens of employer sites, and the facts that decide whether a student can apply (deadline, U.S. citizenship, security clearance, degree level, pay) are buried in long descriptions. Deadlines get missed, and friends applying to the same programs don't share what they know.

Shortlist pulls postings from employers' public job boards, uses AI to read each one for those facts, and lets groups of students track and share applications together. Success means a student sees only internships they can apply to, never misses a deadline, and knows what their friends know.

## Positioning

Every eligibility fact shows where it came from (the job board, the AI with the sentence it read, or a person), and facts the AI isn't sure about go to a review queue where people confirm or fix them. On top of that sourced catalog, friends collect postings together on shared boards with private comments. A generic job board neither shows its sources nor lets a friend group work the same postings together.

## Operating Context

- **Discover:** a shared catalog synced from Greenhouse and Lever job boards every 6 hours, filtered by citizenship, clearance, degree level, work mode, deadline, pay, and keyword; sorted by deadline; closed postings badged.
- **Add by hand:** paste a posting's text or upload a PDF for employers without a supported job board.
- **Review queue:** uncertain fields shown with their evidence; accept or edit. A person's correction is never overwritten.
- **Boards:** create a board, invite friends with a join code, save postings, comment privately. Owner and member roles.
- **Tracker:** one application per posting moving through saved → applying → applied → interview → offer, or ending as rejected or withdrawn; tasks with due dates, optionally tied to an application.
- **Reminders:** a daily digest in the app and by email (tasks due soon, approaching deadlines, new matches for saved searches).
- **Home:** this week at a glance; must work for a brand-new user with nothing yet.
- Students use it on laptops and phones; every page is checked at 1440 and 390 px wide, logged in and logged out.

## Capabilities and Constraints

- Django server-rendered templates with Tailwind (`django-tailwind-cli`), Alpine.js, and htmx. PostgreSQL, Celery + Redis for background work, and a separate FastAPI extraction service reached only through `apps/extraction_client`.
- **Status as of Deliverable 2 (Nov 14, 2026):** accounts and boards work for real; every other page is a clickable prototype on sample data at `/preview/`. The current state per feature is in `docs/user_stories.md`.
- Templates in `templates/` are the real pages; data shapes follow `docs/contracts.md`, and `docs/frontend-handoff.md` explains how views plug in. Links use `get_absolute_url()`, forms use `{% form_url %}`.
- Each owner builds inside their own apps. Shared files (`base.html`, `config/settings.py`, `pyproject.toml`, `uv.lock`, CI) change only through a PR all three teammates approve.
- The repo and its `docs/` GitHub Pages site are public. Nothing private goes in code, docs, issues, PRs, or commits.
- "Shortlist" is a working name.
- Hard deadline: feature freeze Dec 3, final demo Dec 7, 2026.

## Evidence on Hand

- User stories with acceptance criteria: `docs/user_stories.md`.
- Wireframes: `docs/wireframes/` and the Figma wireframe and prototype files linked in `README.md`.
- Sample data for every prototype page: `apps/ui_preview/fake_data.py`.
- **Absent, so never fabricate:** user interview findings (dropped), testimonials, usage numbers, partner employers, accuracy figures for the AI reading, and deployment or production claims.

## Product Principles

1. **Eligibility first.** The facts that decide whether a student can apply come before everything else about a posting.
2. **Show the source.** No fact appears without where it came from; uncertainty is shown openly and routed to people, never hidden.
3. **People outrank the model.** A human correction is final and is never overwritten by a later AI pass.
4. **Built for the group.** Boards, comments, and shared knowledge are core, not an add-on to a solo tracker.
5. **Deadlines drive the day.** Home, sorting, and reminders put what's due soonest in front of the student.

## Accessibility & Inclusion

WCAG 2.1 AA on every page, checked at 1440 and 390 px wide.
