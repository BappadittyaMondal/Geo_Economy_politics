"""
scripts/test_timedtext.py
"""
import urllib.request
import re
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
req = urllib.request.Request('https://www.youtube.com/watch?v=0DuyyXS8OUg', headers=headers)
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')
    caption_m = re.search(r'"captionTracks":\s*(\[.*?\])', html)
    if caption_m:
        tracks = json.loads(caption_m.group(1))
        url = tracks[0]['baseUrl']
        print("Track URL:", url)
        req2 = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req2) as resp2:
                content = resp2.read()
                print("Status:", resp2.status)
                print("Content len:", len(content))
                print("Content sample:", content[:200])
        except Exception as e:
            print("Fetch error:", e)
