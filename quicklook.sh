#!/usr/bin/env bash
# quicklook.sh — Quick Look images on macOS
# Usage: ./quicklook.sh [story-NN]  # or no args for all unorganized

REPO_ROOT="/Users/leoguinan/projects/white-mirror-puzzle"

if [[ $# -eq 0 ]]; then
    # Show all unorganized images
    qlmanage -p "$REPO_ROOT/images"/IMG_*.png >/dev/null 2>&1
elif [[ "$1" == "all" ]]; then
    # Show all images in all stories
    for story in "$REPO_ROOT/stories"/story-*/pages/IMG_*.png; do
        [[ -f "$story" ]] && qlmanage -p "$story" >/dev/null 2>&1
    done
else
    # Show specific story
    story_dir="$REPO_ROOT/stories/$1/pages"
    if [[ -d "$story_dir" ]]; then
        qlmanage -p "$story_dir"/IMG_*.png >/dev/null 2>&1
    else
        echo "Story not found: $1"
        echo "Available: $(ls -1 $REPO_ROOT/stories | grep story- | tr '\n' ' ')"
    fi
fi