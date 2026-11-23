import urllib.request
import re
import json

video_urls = [
    "https://www.youtube.com/watch?v=Q24ThmXdqN8",
    "https://www.youtube.com/watch?v=lCVEEujlPrA",
    "https://www.youtube.com/watch?v=LvNSkHFFriE",
    "https://www.youtube.com/watch?v=hi5r6LMyT2M",
    "https://www.youtube.com/watch?v=y_gDbpmgEak",
    "https://www.youtube.com/watch?v=3gULDSUQxtM&t=16s",
    "https://www.youtube.com/watch?v=z8-jotD16oI&pp=ugUEEgJoaQ%3D%3D",
    "https://www.youtube.com/watch?v=lRdNonWrnF8",
    "https://www.youtube.com/watch?v=iWpk7O2ZFLs",
    "https://www.youtube.com/watch?v=h4jpCCkurzo&pp=0gcJCRAIAYcqIYzv",
    "https://www.youtube.com/watch?v=ltwNzwy5Ghk"
]

seen = set()
unique_urls = []
for u in video_urls:
    v_id = re.search(r'v=([a-zA-Z0-9_-]+)', u).group(1)
    if v_id not in seen:
        seen.add(v_id)
        unique_urls.append((v_id, u))

print(f"Total unique videos: {len(unique_urls)}")

results = []

for idx, (vid, url) in enumerate(unique_urls):
    req = urllib.request.Request(f"https://www.youtube.com/watch?v={vid}", headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
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
            'id': vid,
            'url': url,
            'title': title,
            'author': author,
            'duration_sec': length,
            'desc_snippet': desc[:500]
        }
        results.append(res)
        print(f"[{idx+1}/11] {vid}: {author} | {title} ({length}s)")
    except Exception as e:
        print(f"[{idx+1}/11] {vid} Error: {e}")
        results.append({'index': idx + 1, 'id': vid, 'url': url, 'title': 'Error', 'author': '', 'duration_sec': '', 'desc_snippet': str(e)})

with open("scripts/videos_11_metadata.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved metadata to scripts/videos_11_metadata.json")
