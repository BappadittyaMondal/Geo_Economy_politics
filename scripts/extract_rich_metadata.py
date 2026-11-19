"""
scripts/extract_rich_metadata.py
"""
import urllib.request
import re
import json

urls = [
    ('o88M4Jgi-Ws', 'https://www.youtube.com/watch?v=o88M4Jgi-Ws'),
    ('0DuyyXS8OUg', 'https://www.youtube.com/watch?v=0DuyyXS8OUg'),
    ('FZfH0cl4T60', 'https://www.youtube.com/watch?v=FZfH0cl4T60'),
    ('oBf8d_iyun4', 'https://www.youtube.com/watch?v=oBf8d_iyun4'),
    ('xgrJ4OjjUVA', 'https://www.youtube.com/watch?v=xgrJ4OjjUVA'),
    ('ECYARxJ4k9I', 'https://www.youtube.com/watch?v=ECYARxJ4k9I')
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

results = {}

for vid, url in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            
            # Extract player response
            pr_match = re.search(r'ytInitialPlayerResponse\s*=\s*({.+?});', html)
            if pr_match:
                try:
                    pr = json.loads(pr_match.group(1))
                    video_details = pr.get('videoDetails', {})
                    title = video_details.get('title', '')
                    author = video_details.get('author', '')
                    desc = video_details.get('shortDescription', '')
                    keywords = video_details.get('keywords', [])
                    length_seconds = video_details.get('lengthSeconds', '')
                    
                    results[vid] = {
                        'title': title,
                        'author': author,
                        'desc': desc,
                        'keywords': keywords,
                        'length_seconds': length_seconds
                    }
                    print(f"=== {vid} ===")
                    print(f"Title: {title}")
                    print(f"Author: {author}")
                    print(f"Duration: {int(length_seconds)//60}m {int(length_seconds)%60}s")
                    print(f"Keywords: {', '.join(keywords[:10])}")
                    print("Description:\n", desc[:600])
                    print("-" * 50)
                except Exception as e:
                    print(f"{vid} json parse error: {e}")
            else:
                print(f"{vid} ytInitialPlayerResponse not found")
    except Exception as e:
        print(f"{vid} fetch error: {e}")

with open("scripts/videos_rich_metadata.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
