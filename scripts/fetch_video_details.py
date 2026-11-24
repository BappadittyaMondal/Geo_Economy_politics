"""scripts/fetch_video_details.py
Fetches captions/subtitles or transcript segments for MkrfVSVO5m0.
"""
import urllib.request
import json
import re

url = "https://www.youtube.com/watch?v=MkrfVSVO5m0"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')

    # Look for captionTracks
    m = re.search(r'"captionTracks":\s*(\[.*?\])', html)
    if m:
        captions = json.loads(m.group(1))
        print("Captions available:", len(captions))
        for c in captions:
            print("Language:", c.get('languageCode'), c.get('name', {}).get('simpleText'))
            # fetch first caption
            base_url = c.get('baseUrl')
            if base_url:
                req_cap = urllib.request.Request(base_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req_cap) as cap_resp:
                    cap_xml = cap_resp.read().decode('utf-8', errors='ignore')
                    # extract text
                    texts = re.findall(r'<text start="([\d\.]+)" dur="([\d\.]+)"[^>]*>(.*?)</text>', cap_xml)
                    print(f"Extracted {len(texts)} text segments.")
                    with open("scripts/transcript_MkrfVSVO5m0.txt", "w", encoding="utf-8") as tf:
                        for start, dur, txt in texts:
                            clean_txt = txt.replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'").replace('&lt;', '<').replace('&gt;', '>')
                            tf.write(f"[{float(start):.1f}s] {clean_txt}\n")
                    print("Saved transcript to scripts/transcript_MkrfVSVO5m0.txt")
                    break
    else:
        print("No direct captionTracks found in initial html.")
        
    # Also check if description has full text or chapters
    chapters = re.findall(r'(\d+:\d+)\s+([^\n\r]+)', html)
    if chapters:
        print("Possible chapters found:", len(chapters))
        for ch in chapters[:15]:
            print(ch)

except Exception as e:
    print("Error:", e)
