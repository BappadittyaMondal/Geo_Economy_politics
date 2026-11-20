"""
scripts/inspect_articles.py
"""
import re

files = [
    ("moneycontrol", "scripts/moneycontrol.txt"),
    ("et_cea", "scripts/et_cea.txt"),
    ("et_bfsi", "scripts/et_bfsi.txt"),
    ("thehindu", "scripts/thehindu.txt")
]

for tag, fpath in files:
    with open(fpath, "r", encoding="utf-8") as f:
        text = f.read()
    print(f"==================== {tag.upper()} ====================")
    # Print lines that look like article content
    paragraphs = [p.strip() for p in text.split("  ") if len(p.strip()) > 80]
    print(f"Total long chunks: {len(paragraphs)}")
    for i, p in enumerate(paragraphs[:15]):
        # filter out nav/cookie stuff
        if any(w in p.lower() for w in ['rupee', 'currency', 'depreciation', 'appreciation', 'rbi', 'nageswaran', 'stock', 'fii', 'market', 'trade', 'export', 'import', 'dollar']):
            print(f"[{i}] {p[:300]}...\n")
