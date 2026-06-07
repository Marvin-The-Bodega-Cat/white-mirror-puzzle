#!/usr/bin/env python3
"""
organize_pages.py — CLI tool to organize White Mirror Puzzle pages into stories.

Usage:
  python organize_pages.py list              # Show current organization
  python organize_pages.py move 01 7243 7244 # Move pages to story-01
  python organize_pages.py move 01 all       # Move all remaining to story-01
  python organize_pages.py status            # Show master index status
"""

import sys
import shutil
from pathlib import Path

REPO_ROOT = Path("/Users/leoguinan/projects/white-mirror-puzzle")
IMAGES_DIR = REPO_ROOT / "images"
STORIES_DIR = REPO_ROOT / "stories"
MASTER_INDEX = REPO_ROOT / "analysis" / "master-index.md"


def list_stories():
    print("=== Stories ===")
    for story_dir in sorted(STORIES_DIR.glob("story-*")):
        pages = sorted(story_dir.glob("pages/*.png"))
        print(f"  {story_dir.name}: {len(pages)} pages")
        for p in pages:
            print(f"    {p.name}")


def list_unorganized():
    pages = sorted(IMAGES_DIR.glob("IMG_*.png"))
    print(f"=== Unorganized ({len(pages)} pages) ===")
    for p in pages:
        print(f"  {p.name}")


def move_pages(story_num: str, page_nums: list[str]):
    story_dir = STORIES_DIR / f"story-{story_num}"
    pages_dir = story_dir / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)

    if page_nums == ["all"]:
        sources = sorted(IMAGES_DIR.glob("IMG_*.png"))
    else:
        sources = []
        for num in page_nums:
            src = IMAGES_DIR / f"IMG_{num}.png"
            if src.exists():
                sources.append(src)
            else:
                print(f"NOT FOUND: IMG_{num}.png")

    for src in sources:
        dst = pages_dir / src.name
        shutil.move(str(src), str(dst))
        print(f"  Moved {src.name} → story-{story_num}/pages/")

    # Update master index placeholder
    print(f"\n>>> Update {MASTER_INDEX} with page range for story-{story_num}")


def show_status():
    print("=== Master Index Status ===")
    if MASTER_INDEX.exists():
        print(MASTER_INDEX.read_text())
    else:
        print("Master index not found")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]

    if cmd == "list":
        list_stories()
        print()
        list_unorganized()
    elif cmd == "move" and len(sys.argv) >= 3:
        story_num = sys.argv[2]
        page_nums = sys.argv[3:] if len(sys.argv) > 3 else []
        if not page_nums:
            print("Provide page numbers or 'all'")
            return
        move_pages(story_num, page_nums)
    elif cmd == "status":
        show_status()
    else:
        print(__doc__)


if __name__ == "__main__":
    main()