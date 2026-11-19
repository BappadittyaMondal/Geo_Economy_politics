"""
scripts/fetch_transcripts_json.py
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
            
            caption_m = re.search(r'"captionTracks":\s*(\[.*?\])', html)
            if caption_m:
                tracks = json.loads(caption_m.group(1))
                # Prefer en or hi
                chosen = None
                for t in tracks:
                    if t.get('languageCode') in ['en', 'hi']:
                        chosen = t
                        break
                if not chosen and tracks:
                    chosen = tracks[0]
                
                track_url = chosen.get('baseUrl')
                if not '&fmt=' in track_url:
                    track_url += '&fmt=json3'
                    
                req_t = urllib.request.Request(track_url, headers=headers)
                with urllib.request.urlopen(req_t, timeout=10) as resp_t:
                    raw_data = resp_t.read().decode('utf-8', errors='ignore')
                    j = json.loads(raw_data)
                    events = j.get('events', [])
                    text = ' '.join(''.join(s.get('utf8', '') for s in e.get('segs', [])) for e in events)
                    text = re.sub(r'\s+', ' ', text).strip()
                    print(f"=== {vid} ({chosen.get('languageCode')}) ===")
                    print(f"Words: {len(text.split())}")
                    print(f"Preview: {text[:350]}...\n")
                    with open(f"scripts/{vid}_transcript.txt", "w", encoding="utf-8") as out_f:
                        out_f.write(text)
            else:
                print(f"=== {vid} No captions found ===")
    except Exception as e:
        print(f"=== {vid} Error: {e}")
