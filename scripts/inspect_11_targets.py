import urllib.request
import re
import json

targets = [
    "https://www.youtube.com/watch?v=ywaUhEej_oU",
    "https://www.youtube.com/watch?v=w8tg3Z6kWFk",
    "https://www.youtube.com/watch?v=hAr3WuIsB1c",
    "https://www.youtube.com/watch?v=f3eH-5DakJA",
    "https://www.youtube.com/watch?v=_F2llfGmvfQ",
    "https://www.youtube.com/@PurposeOverNoiseWorldAffairs",
    "https://www.youtube.com/watch?v=7C4xemWiBEo",
    "https://www.youtube.com/watch?v=DcgTINwxOaI",
    "https://www.youtube.com/watch?v=pIsrJfgQOWg",
    "https://www.youtube.com/watch?v=VHNt4sljhgY&pp=0gcJCTwIAYcqIYzv",
    "https://www.youtube.com/watch?v=USd5X1J4_V4"
]

results = []

for idx, url in enumerate(targets):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        
        title_m = re.search(r'<title>(.*?)</title>', html)
        title = title_m.group(1).replace(' - YouTube', '').strip() if title_m else 'Unknown'
        
        author_m = re.search(r'"author":"(.*?)"', html)
        author = author_m.group(1) if author_m else ''
        
        length_m = re.search(r'"lengthSeconds":"(.*?)"', html)
        length = length_m.group(1) if length_m else ''
        
        desc_m = re.search(r'"shortDescription":"(.*?)"', html)
        desc = desc_m.group(1) if desc_m else ''
        
        res = {
            'index': idx + 1,
            'url': url,
            'title': title,
            'author': author,
            'duration_sec': length,
            'desc_snippet': desc[:500]
        }
        results.append(res)
        print(f"[{idx+1}/11] {url} -> {author} | {title} ({length}s)")
    except Exception as e:
        print(f"[{idx+1}/11] {url} Error: {e}")
        results.append({'index': idx + 1, 'url': url, 'title': 'Error', 'author': '', 'duration_sec': '', 'desc_snippet': str(e)})

with open("scripts/targets_11_metadata.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved metadata to scripts/targets_11_metadata.json")
