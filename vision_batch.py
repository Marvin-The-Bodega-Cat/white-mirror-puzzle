#!/usr/bin/env python3
"""
Batch vision analysis for White Mirror Puzzle pages.
Uses Ollama with LLaVA for local vision processing.
"""

import json
import base64
import argparse
import re
from pathlib import Path
from ollama import Client

def extract_num(name):
    m = re.search(r'IMG_(\d+)', name)
    return int(m.group(1)) if m else 999999

# Initialize Ollama client
client = Client(host='http://localhost:11434')

# Prompt for structured extraction
EXTRACTION_PROMPT = """Analyze this book page from "White Mirror" (sci-fi anthology). Return ONLY valid JSON.

{
  "page_type": "cover|title_page|chapter_start|content|blank|other",
  "text_content": "ALL visible text, line by line. If illegible, write \"illegible\".",
  "page_number": null or integer,
  "chapter_number": null or string,
  "chapter_title": null or string,
  "story_title": null or string,
  "author_name": null or string,
  "glyphs_symbols": ["describe each symbol/icon/glyph"],
  "watermarks": ["describe faint text/watermarks"],
  "layout_notes": "brief layout description",
  "recurring_motifs": ["circuit_board", "geometric_logo", "arrow_triangle", "INFINITE_BOOKS", "TINKERED_THINKING", "WHITE_MIRROR"],
  "orientation": "portrait|landscape|rotated_90_cw|rotated_90_ccw",
  "confidence": 0.0-1.0
}

NO EXPLANATION. ONLY JSON."""

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

def analyze_image(image_path, model="llava:13b"):
    try:
        response = client.chat(
            model=model,
            messages=[{
                'role': 'user',
                'content': EXTRACTION_PROMPT,
                'images': [encode_image(image_path)]
            }],
            options={'temperature': 0.1}
        )
        content = response['message']['content']
        # Try to parse JSON from response
        start = content.find('{')
        end = content.rfind('}') + 1
        if start >= 0 and end > start:
            return json.loads(content[start:end])
        return {"error": "Failed to parse JSON", "raw": content}
    except Exception as e:
        return {"error": str(e)}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', default='/Users/leoguinan/projects/white-mirror-puzzle/images')
    parser.add_argument('--output', default='/Users/leoguinan/projects/white-mirror-puzzle/analysis/page_metadata.json')
    parser.add_argument('--model', default='llava:13b')
    parser.add_argument('--limit', type=int, default=None)
    parser.add_argument('--start', type=int, default=0)
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    image_files = sorted(input_dir.glob("IMG_*.png"), key=lambda f: extract_num(f.name))
    
    if args.limit:
        image_files = image_files[args.start:args.start + args.limit]
    
    # Load existing results
    output_path = Path(args.output)
    results = {}
    if output_path.exists():
        with open(output_path) as f:
            results = json.load(f)
        print(f"Loaded {len(results)} existing results")
    
    # Filter out already-processed images
    to_process = [f for f in image_files if f.name not in results]
    
    print(f"Processing {len(to_process)} new images with {args.model}...")
    
    for i, img_path in enumerate(to_process):
        print(f"[{i+1}/{len(to_process)}] {img_path.name}...", end=" ", flush=True)
        result = analyze_image(str(img_path), args.model)
        results[img_path.name] = result
        print("✓" if "error" not in result else f"✗ ({result.get('error', 'unknown')})")
        
        # Save progress every 10 images
        if (i + 1) % 10 == 0:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
    
    # Final save
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDone. Results saved to {args.output}")

if __name__ == "__main__":
    main()