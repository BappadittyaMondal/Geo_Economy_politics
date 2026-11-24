import json

data = json.load(open('scripts/targets_11_metadata.json', encoding='utf-8'))
for d in data:
    print(f"[{d['index']}] URL: {d['url']}")
    print(f"Title: {d['title']} | Author: {d['author']} | Duration: {d['duration_sec']}s")
    print(f"Snippet: {d['desc_snippet']}")
    print("=" * 60)
