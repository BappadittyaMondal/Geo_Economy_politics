"""
scripts/inspect_new_video.py
"""
import urllib.request
import re
import json

url = 'https://www.youtube.com/watch?v=1C-Mps-LwXI'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=12) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

# Title
title_m = re.search(r'<title>(.*?)</title>', html)
title = title_m.group(1).replace(' - YouTube', '').strip() if title_m else 'Unknown'

# Channel
channel_m = re.search(r'"ownerChannelName":"([^"]+)"', html) or re.search(r'"author":"([^"]+)"', html)
channel = channel_m.group(1) if channel_m else 'Unknown'

# Description
desc_m = re.search(r'"shortDescription":"([^"]+)"', html)
desc = desc_m.group(1).encode('utf-8').decode('unicode_escape', errors='ignore') if desc_m else 'No desc'

# Date
date_m = re.search(r'"publishDate":"([^"]+)"', html) or re.search(r'"uploadDate":"([^"]+)"', html)
date = date_m.group(1) if date_m else 'Unknown'

# Length
len_m = re.search(r'"lengthSeconds":"([^"]+)"', html)
length = len_m.group(1) if len_m else '0'

# Keywords
kw_m = re.search(r'"keywords":(\[.*?\])', html)
keywords = kw_m.group(1) if kw_m else '[]'

print(f"Title: {title}")
print(f"Channel: {channel}")
print(f"Date: {date}")
print(f"Duration: {int(length)//60}m {int(length)%60}s")
print(f"Keywords: {keywords[:200]}")
print(f"Description:\n{desc}\n")

with open("scripts/video_1C-Mps-LwXI.txt", "w", encoding="utf-8") as f:
    f.write(f"Title: {title}\nChannel: {channel}\nDate: {date}\nDuration: {length}\nKeywords: {keywords}\n\nDescription:\n{desc}\n")
