import urllib.request
import re
import json

video_urls = [
    "https://www.youtube.com/watch?v=yTRo8pd-FME",
    "https://www.youtube.com/watch?v=O_ixC270uPU",
    "https://www.youtube.com/watch?v=2MuR2t0uimQ",
    "https://www.youtube.com/watch?v=96hG5Jy9Qfo",
    "https://www.youtube.com/watch?v=iJ8FjhrVo6Q",
    "https://www.youtube.com/watch?v=NYwoEGBaIUo",
    "https://www.youtube.com/watch?v=RCNyhpGRYnU",
    "https://www.youtube.com/watch?v=l94obFmMaIM",
    "https://www.youtube.com/watch?v=coIqdVPHZnE",
    "https://www.youtube.com/watch?v=iBb2hEPOwRY",
    "https://www.youtube.com/watch?v=wsGO_PXUMTE",
    "https://www.youtube.com/watch?v=Vh2KFICpnVo",
    "https://www.youtube.com/watch?v=t-8RCK5JfbI",
    "https://www.youtube.com/watch?v=QO8NTA4HCJo",
    "https://www.youtube.com/watch?v=yRVgNB3Ieys",
    "https://www.youtube.com/watch?v=30Xlo1Pcl2c",
    "https://www.youtube.com/watch?v=_bnVDasqsr4",
    "https://www.youtube.com/watch?v=eIFif_aIL6k",
    "https://www.youtube.com/watch?v=w8tg3Z6kWFk",
    "https://www.youtube.com/watch?v=nRj65O5RTnc",
    "https://www.youtube.com/watch?v=Vw5-PngxXnE",
    "https://www.youtube.com/watch?v=3fCeZ0Jk4DQ"
]

# Deduplicate preserving order
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
        with urllib.request.urlopen(req, timeout=10) as resp:
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
            'desc_snippet': desc[:200]
        }
        results.append(res)
        print(f"[{idx+1}/22] {vid}: {author} | {title} ({length}s)")
    except Exception as e:
        print(f"[{idx+1}/22] {vid} Error: {e}")
        results.append({'index': idx + 1, 'id': vid, 'url': url, 'title': 'Error', 'author': '', 'duration_sec': '', 'desc_snippet': str(e)})

with open("scripts/videos_22_metadata.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved metadata to scripts/videos_22_metadata.json")
