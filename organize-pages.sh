#!/usr/bin/env bash
# organize-pages.sh — Interactive helper to move pages into story folders
# Usage: ./organize-pages.sh

set -euo pipefail

REPO_ROOT="/Users/leoguinan/projects/white-mirror-puzzle"
IMAGES_DIR="$REPO_ROOT/images"
STORIES_DIR="$REPO_ROOT/stories"

echo "=== White Mirror Puzzle — Page Organizer ==="
echo "Source: $IMAGES_DIR"
echo "Target: $STORIES_DIR/story-XX/pages/"
echo ""

# List available story folders
echo "Available stories:"
ls -1 "$STORIES_DIR" | grep "^story-" | sed 's/^/  /'
echo ""

# Show unorganized pages
echo "Unorganized pages (in images/):"
ls -1 "$IMAGES_DIR"/IMG_*.png | xargs -n1 basename | sed 's/^/  /'
echo ""

read -p "Enter story number (e.g., 01) or 'list' to see story contents: " STORY_NUM

if [[ "$STORY_NUM" == "list" ]]; then
    for s in "$STORIES_DIR"/story-*/pages; do
        echo ""
        echo "=== $(basename $(dirname $s)) ==="
        ls -1 "$s" 2>/dev/null | sed 's/^/  /' || echo "  (empty)"
    done
    exit 0
fi

STORY_DIR="$STORIES_DIR/story-${STORY_NUM}"
if [[ ! -d "$STORY_DIR" ]]; then
    mkdir -p "$STORY_DIR/pages"
    echo "Created $STORY_DIR/pages"
fi

echo ""
echo "Pages will be moved to: $STORY_DIR/pages/"
echo "Enter page numbers (e.g., 7243 7244 7245) or 'all' for remaining:"
read -p "> " PAGE_NUMS

if [[ "$PAGE_NUMS" == "all" ]]; then
    # Move all unorganized pages
    for f in "$IMAGES_DIR"/IMG_*.png; do
        mv "$f" "$STORY_DIR/pages/"
    done
    echo "Moved all pages to story-${STORY_NUM}"
else
    for num in $PAGE_NUMS; do
        src="$IMAGES_DIR/IMG_${num}.png"
        if [[ -f "$src" ]]; then
            mv "$src" "$STORY_DIR/pages/"
            echo "  Moved IMG_${num}.png"
        else
            echo "  NOT FOUND: IMG_${num}.png"
        fi
    done
fi

echo ""
echo "Story-${STORY_NUM} pages now:"
ls -1 "$STORY_DIR/pages" | sed 's/^/  /'

# Update master index reminder
echo ""
echo ">>> Remember to update analysis/master-index.md with the page range!"