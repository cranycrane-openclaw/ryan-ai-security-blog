# Agents Playbook

This is the operational contract so everyone knows what to do without ad-hoc coordination.

## Roles

- **Marvin** = research owner
- **Marvin** = drafting owner
- **Marvin** = editing owner

## Daily source of truth

1. `automation/pipeline/daily/YYYY-MM-DD.md`
2. `automation/pipeline/state.json`

If these conflict, update `state.json` first and regenerate daily task.

Daily generation is automated by GitHub Actions (`editorial-daily.yml`).

## Handoff contract

- Marvin outputs: `research/*.research.md`
- Marvin outputs: `drafts/*.draft.md`
- Marvin outputs: `final/*.final.md`
- Publish output: `_posts/YYYY-MM-DD-slug.md`

Each stage must update `state.json` in the same commit.

## Minimum quality bar by role

### Marvin
- At least 3 credible sources
- Specific angle, not generic summary
- Practical security implications

### Marvin
- Full article draft from research handoff
- Concrete examples/checklists
- No invented references

### Marvin
- Clarity, flow, consistency
- Tighten title + intro
- Final readiness checklist complete

## Status transitions

`queued -> researched -> drafted -> edited -> published`

Allowed exception:
- Any stage can set `blocked` with a short reason in commit message.
