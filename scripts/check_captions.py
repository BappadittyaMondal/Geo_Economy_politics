"""
scripts/check_captions.py
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

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for vid, url in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            
            # Find captionTracks
            caption_m = re.search(r'"captionTracks":\s*(\[.*?\])', html)
            if caption_m:
                tracks = json.loads(caption_m.group(1))
                print(f"=== {vid} Captions available ===")
                for t in tracks:
                    print(f"  Lang: {t.get('languageCode')} - {t.get('name', {}).get('simpleText')} URL: {t.get('baseUrl')[:60]}...")
            else:
                print(f"=== {vid} No captions in initial HTML ===")
    except Exception as e:
        print(f"=== {vid} Error: {e}")
