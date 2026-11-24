"""scripts/inspect_captions.py
"""
import urllib.request
import json
import re

url = 'https://www.youtube.com/watch?v=MkrfVSVO5m0'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

m = re.search(r'"captionTracks":\s*(\[.*?\])', html)
if m:
    tracks = json.loads(m.group(1))
    for i, t in enumerate(tracks):
        print(f"Track {i}: lang={t.get('languageCode')}, name={t.get('name')}")
        base_url = t.get('baseUrl')
        # Let's inspect content
        try:
            r = urllib.request.Request(base_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(r) as cr:
                content = cr.read().decode('utf-8', errors='ignore')
                print(f"  Length: {len(content)}, Snippet: {content[:200]}")
                # check if json3 format or xml
                if len(content) > 100:
                    with open(f"scripts/caption_track_{i}_{t.get('languageCode')}.txt", "w", encoding="utf-8") as out_f:
                        out_f.write(content)
        except Exception as e:
            print("  Error fetching:", e)
