import json

data = json.load(open('scripts/videos_11_metadata.json', encoding='utf-8'))
for d in data:
    print(f"[{d['index']}] ID: {d['id']} | Channel: {d['author']} | Duration: {d['duration_sec']}s")
    print(f"Title: {d['title']}")
    print(f"Snippet: {d['desc_snippet']}")
    print("-" * 60)
