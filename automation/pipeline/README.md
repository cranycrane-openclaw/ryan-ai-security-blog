# Editorial Pipeline (Marvin workflow)

This pipeline is designed for the weekly cadence:

- Monday: Publish
- Tuesday: Research
- Wednesday: Publish
- Thursday: Research
- Friday: Publish
- Saturday: Research
- Sunday: Research

## Directories

- `research/` — handoff files prepared by **Marvin**
- `drafts/` — article drafts prepared by **Marvin**
- `final/` — final edited articles prepared by **Marvin**
- `templates/` — markdown templates for each stage
- `daily/` — auto-generated daily task cards
- `state.json` — queue + status tracking
- `agents-playbook.md` — role contract for Marvin

## File naming

Use consistent slug-based naming:

- Research: `YYYY-MM-DD-<slug>.research.md`
- Draft: `YYYY-MM-DD-<slug>.draft.md`
- Final: `YYYY-MM-DD-<slug>.final.md`

Example: `2026-03-10-zero-trust-for-ai-agents.research.md`

## Workflow

1. **Research day (Tue/Thu/Sat/Sun)**
   - Marvin picks the next queued topic from `state.json`.
   - Marvin writes research note using `templates/research-template.md`.
   - Marvin sets topic status to `researched` and writes `researchFile` path.

2. **Drafting**
   - Marvin picks a `researched` topic.
   - Marvin writes full draft using `templates/draft-template.md`.
   - Marvin sets status to `drafted` and writes `draftFile` path.

3. **Editing**
   - Marvin picks a `drafted` topic.
   - Marvin edits and finalizes with `templates/final-checklist.md`.
   - Marvin sets status to `edited` and writes `finalFile` path.

4. **Publish day (Mon/Wed/Fri)**
   - Publish next `edited` topic into `_posts/YYYY-MM-DD-<slug>.md`.
   - Move/copy from `final/` to `_posts/`.
   - Set status to `published`.

## Status values

- `queued`
- `researched`
- `drafted`
- `edited`
- `published`
- `blocked`

## Automation

- OpenClaw cron jobs trigger agents daily:
  - `marvin-research-days` (Tue/Thu/Sat/Sun 08:15 Europe/Prague)
  - `marvin-publish-days-builder` (Mon/Wed/Fri 08:20 Europe/Prague)
  - `marvin-publish-days-editor` (Mon/Wed/Fri 08:30 Europe/Prague)
- GitHub Action: `.github/workflows/editorial-daily.yml` (09:05 UTC daily)
- Runs daily and does three steps:
  1. `sync_state.py` — syncs `state.json` from files in `research/`, `drafts/`, `final/`
  2. `publish_from_final.py` — on Mon/Wed/Fri auto-publishes next `edited` topic to `_posts/`
  3. `generate_daily_task.py` — creates `daily/YYYY-MM-DD.md` with role instructions
- Can also be triggered manually via **workflow_dispatch**

## Coordination rule

Every stage must update `state.json` in the same commit as its content file.
This ensures Marvin can always pick up Marvin's latest research without ambiguity.
