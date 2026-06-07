# White Mirror Puzzle — Analysis Repository

## Structure

```
white-mirror-puzzle/
├── source-heic/          # Original HEIC files (186 files, IMG_7243–IMG_7506)
├── images/               # All PNG conversions (flat, sequential)
├── stories/              # Per-story/chapter organization (populate this)
│   ├── story-01/
│   │   ├── pages/        # PNG files for this story
│   │   └── analysis.md   # Claude analysis for this chapter
│   ├── story-02/
│   │   ├── pages/
│   │   └── analysis.md
│   └── ...
├── analysis/             # Cross-story synthesis & puzzle solution
│   ├── master-index.md   # Master tracking document
│   ├── patterns.md       # Observed patterns across stories
│   ├── hypotheses.md     # Working hypotheses for the puzzle solution
│   └── solution.md       # Final solution (when reached)
└── output/               # Generated artifacts (timelines, diagrams, etc.)
```

## Quick Start

1. **Organize pages into stories**: Move/copy PNGs from `images/` into `stories/story-XX/pages/` in reading order
2. **Add chapter analysis**: Drop your Claude analysis into each `stories/story-XX/analysis.md`
3. **Synthesize**: Use `analysis/` to track cross-story patterns and hypotheses
4. **Solve**: Document the final solution in `analysis/solution.md`

## Page Inventory

186 pages total (IMG_7243.png – IMG_7506.png). Notable smaller files (likely title/chapter pages):
- IMG_7243.png (8.9 MB) — first page
- IMG_7244.png (8.4 MB)
- IMG_7246.png (6.9 MB)
- IMG_7254.png (6.9 MB)
- IMG_7258.png (8.3 MB)
- IMG_7266.png (8.9 MB)
- IMG_7278.png (7.4 MB)
- IMG_7469.png (9.0 MB)
- IMG_7480.png (8.8 MB)
- IMG_7482.png (8.1 MB)
- IMG_7485.png (8.8 MB)
- IMG_7489.png (8.0 MB)
- IMG_7504.png (8.2 MB)
- IMG_7505.png (8.6 MB)
- IMG_7506.png (7.8 MB)

## Converting More HEIC

```bash
cd source-heic
for f in *.HEIC; do sips -s format png "$f" --out "../images/${f%.HEIC}.png"; done
```

## Analysis Template (per story)

```markdown
# Story XX: [Title]

## Pages
- [ ] IMG_XXXX.png — [description]
- [ ] IMG_XXXX.png — [description]

## Key Observations
- 

## Symbols / Motifs
- 

## Text / Cipher Elements
- 

## Cross-References
- Links to other stories:
- Recurring elements:

## Hypothesis
- 
```

---

*Repo created: $(date). Ready for your chapter analysis.*