#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[3]
PIPELINE = ROOT / "automation" / "pipeline"
STATE_PATH = PIPELINE / "state.json"
TZ = ZoneInfo("Europe/Prague")


def iso_now() -> str:
    return datetime.now(TZ).isoformat(timespec="seconds")


def latest_match(directory: Path, suffix: str, slug: str) -> Path | None:
    matches = sorted(directory.glob(f"*{slug}{suffix}"))
    return matches[-1] if matches else None


def main() -> None:
    with STATE_PATH.open("r", encoding="utf-8") as f:
        state = json.load(f)

    changed = False
    for topic in state.get("topics", []):
        slug = topic.get("slug", "").strip()
        if not slug:
            continue

        research = latest_match(PIPELINE / "research", ".research.md", slug)
        draft = latest_match(PIPELINE / "drafts", ".draft.md", slug)
        final = latest_match(PIPELINE / "final", ".final.md", slug)

        if research:
            rel = str(research.relative_to(ROOT))
            if topic.get("researchFile") != rel:
                topic["researchFile"] = rel
                changed = True
            if topic.get("status") in {"queued", "blocked"}:
                topic["status"] = "researched"
                topic["updatedAt"] = iso_now()
                changed = True

        if draft:
            rel = str(draft.relative_to(ROOT))
            if topic.get("draftFile") != rel:
                topic["draftFile"] = rel
                changed = True
            if topic.get("status") in {"researched", "blocked"}:
                topic["status"] = "drafted"
                topic["updatedAt"] = iso_now()
                changed = True

        if final:
            rel = str(final.relative_to(ROOT))
            if topic.get("finalFile") != rel:
                topic["finalFile"] = rel
                changed = True
            if topic.get("status") in {"drafted", "blocked"}:
                topic["status"] = "edited"
                topic["updatedAt"] = iso_now()
                changed = True

    if changed:
        with STATE_PATH.open("w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("state.json updated")
    else:
        print("no changes")


if __name__ == "__main__":
    main()
