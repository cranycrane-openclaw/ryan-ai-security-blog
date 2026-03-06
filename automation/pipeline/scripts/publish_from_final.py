#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[3]
PIPELINE = ROOT / "automation" / "pipeline"
STATE_PATH = PIPELINE / "state.json"
POSTS_DIR = ROOT / "_posts"
TZ = ZoneInfo("Europe/Prague")

PUBLISH_DAYS = {"monday", "wednesday", "friday"}


def iso_now() -> str:
    return datetime.now(TZ).isoformat(timespec="seconds")


def main() -> None:
    now = datetime.now(TZ)
    today = now.date().isoformat()
    weekday = now.strftime("%A").lower()

    if weekday not in PUBLISH_DAYS:
        print(f"today is {weekday}; not a publish day")
        return

    with STATE_PATH.open("r", encoding="utf-8") as f:
        state = json.load(f)

    topics = state.get("topics", [])
    target = None
    for t in topics:
        if t.get("status") == "edited":
            target = t
            break

    if not target:
        print("no edited topic to publish")
        return

    final_file = target.get("finalFile", "")
    if not final_file:
        print("edited topic has no finalFile path")
        return

    src = ROOT / final_file
    if not src.exists():
        print(f"final file not found: {src}")
        return

    slug = target.get("slug", "untitled")
    out = POSTS_DIR / f"{today}-{slug}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, out)

    target["status"] = "published"
    target["publishedPost"] = str(out.relative_to(ROOT))
    target["updatedAt"] = iso_now()

    with STATE_PATH.open("w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"published {out}")


if __name__ == "__main__":
    main()
