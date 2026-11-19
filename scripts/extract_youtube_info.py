"""
scripts/extract_youtube_info.py
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

for vid, url in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            
            title_m = re.search(r'<title>(.*?)</title>', html)
            title = title_m.group(1).replace(' - YouTube', '').strip() if title_m else 'Unknown'
            
            channel_m = re.search(r'"ownerChannelName":"([^"]+)"', html) or re.search(r'"author":"([^"]+)"', html)
            channel = channel_m.group(1) if channel_m else 'Unknown'
            
            desc_m = re.search(r'"shortDescription":"([^"]+)"', html)
            desc = desc_m.group(1).encode('utf-8').decode('unicode_escape', errors='ignore') if desc_m else 'No desc'
            
            date_m = re.search(r'"publishDate":"([^"]+)"', html) or re.search(r'"uploadDate":"([^"]+)"', html)
            date = date_m.group(1) if date_m else 'Unknown'
            
            print(f"=== {vid} ===")
            print(f"Title: {title}")
            print(f"Channel: {channel}")
            print(f"Date: {date}")
            print(f"Desc: {desc[:400]}")
            print()
    except Exception as e:
        print(f"=== {vid} === Error: {e}")
