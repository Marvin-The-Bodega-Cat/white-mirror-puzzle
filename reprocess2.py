#!/usr/bin/env python3
"""
Reprocess specific images with improved prompt.
"""

import json
import base64
import re
from pathlib import Path
from ollama import Client

client = Client(host='http://localhost:11434')

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

def extract_num(name):
    m = re.search(r'IMG_(\d+)', name)
    return int(m.group(1)) if m else 999999

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
            options={'temperature': 0.0}
        )
        content = response['message']['content']
        start = content.find('{')
        end = content.rfind('}') + 1
        if start >= 0 and end > start:
            return json.loads(content[start:end])
        return {"error": "Failed to parse JSON", "raw": content[:200]}
    except Exception as e:
        return {"error": str(e)}

def main():
    # Load list of images to reprocess
    with open('/Users/leoguinan/projects/white-mirror-puzzle/analysis/to_reprocess2.json') as f:
        to_reprocess = json.load(f)
    
    # Load existing results
    output_path = Path('/Users/leoguinan/projects/white-mirror-puzzle/analysis/page_metadata.json')
    with open(output_path) as f:
        results = json.load(f)
    
    print(f"Reprocessing {len(to_reprocess)} images...")
    
    for i, img_name in enumerate(to_reprocess):
        img_path = Path('/Users/leoguinan/projects/white-mirror-puzzle/images') / img_name
        if not img_path.exists():
            print(f"[{i+1}/{len(to_reprocess)}] {img_name}... NOT FOUND")
            continue
        
        print(f"[{i+1}/{len(to_reprocess)}] {img_name}...", end=" ", flush=True)
        result = analyze_image(str(img_path))
        results[img_name] = result
        print("✓" if "error" not in result else f"✗ ({result.get('error', 'unknown')})")
        
        if (i + 1) % 10 == 0:
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=2)
    
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDone. Results saved.")

if __name__ == "__main__":
    main()