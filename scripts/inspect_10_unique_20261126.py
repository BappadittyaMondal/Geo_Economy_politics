"""scripts/inspect_10_unique_20261126.py
Fetches metadata, descriptions, keywords, and full transcripts for the 11 links (10 unique video IDs).
"""
import concurrent.futures
import json
import re
import urllib.parse
import urllib.request
from youtube_transcript_api import YouTubeTranscriptApi

URLS = [
    ("01", "https://www.youtube.com/watch?v=uatz1dTTPQ0"),
    ("02", "https://www.youtube.com/watch?v=aQv0stk8QY8"),
    ("03", "https://www.youtube.com/watch?v=qwOL9dWveEM&pp=ugUEEgJlbtIHCQk3CAGHKiGM7w%3D%3D"),
    ("04", "https://www.youtube.com/watch?v=Kf-trFQRZLI"),
    ("05", "https://www.youtube.com/watch?v=WD1lizsfRC8"),
    ("06", "https://www.youtube.com/watch?v=ZNVShd2Qy4Y&t=135s&pp=ugUEEgJoaQ%3D%3D"),
    ("07_dup1", "https://www.youtube.com/watch?v=uatz1dTTPQ0"),
    ("08", "https://www.youtube.com/watch?v=VkLz1OXfV0Y"),
    ("09", "https://www.youtube.com/watch?v=e_M8Tgin-uI"),
    ("10", "https://www.youtube.com/watch?v=q5N0EZ8fEJI&pp=ugUEEgJlbg%3D%3D"),
    ("11", "https://www.youtube.com/watch?v=xrBNBZEnRJY"),
]

def extract_vid(url):
    return urllib.parse.parse_qs(urllib.parse.urlparse(url).query).get("v", [""])[0]

# Deduplicate preserving order
seen = set()
UNIQUE = []
for slot, url in URLS:
    vid = extract_vid(url)
    if vid not in seen:
        seen.add(vid)
        UNIQUE.append((slot, vid, url))

def fetch_one(item):
    slot, vid, url = item
    clean_url = f"https://www.youtube.com/watch?v={vid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    res = {"slot": slot, "video_id": vid, "url": url}
    try:
        req = urllib.request.Request(clean_url, headers=headers)
        with urllib.request.urlopen(req, timeout=20) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        m = re.search(r"ytInitialPlayerResponse\s*=\s*(\{.*?\});", html)
        if m:
            data = json.loads(m.group(1))
            vd = data.get("videoDetails", {})
            mf = data.get("microformat", {}).get("playerMicroformatRenderer", {})
            res["title"] = vd.get("title")
            res["author"] = vd.get("author")
            res["length_seconds"] = vd.get("lengthSeconds")
            res["view_count"] = vd.get("viewCount")
            res["publish_date"] = mf.get("publishDate")
            res["keywords"] = vd.get("keywords", [])
            res["short_description"] = vd.get("shortDescription", "")
    except Exception as e:
        res["meta_error"] = str(e)

    try:
        api = YouTubeTranscriptApi()
        t_list = api.fetch(vid, languages=["en", "hi", "en-US", "en-IN", "bn"])
        res["transcript_text"] = " ".join([x.text for x in t_list])
    except Exception as e:
        res["transcript_text"] = ""
        res["transcript_error"] = str(e)
    return res

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(fetch_one, UNIQUE))
    with open("scripts/targets_10_20261126_meta.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    for r in results:
        vid = r["video_id"]
        txt = r.get("transcript_text", "")
        with open(f"scripts/v26_{r['slot']}_{vid}.txt", "w", encoding="utf-8") as out:
            out.write(f"SLOT: {r['slot']} | ID: {vid} | AUTHOR: {r.get('author')}\n")
            out.write(f"DATE: {r.get('publish_date')} | DUR: {r.get('length_seconds')}s | VIEWS: {r.get('view_count')}\n")
            out.write(f"TITLE: {r.get('title')}\nKEYWORDS: {r.get('keywords')}\n")
            out.write(f"DESCRIPTION:\n{r.get('short_description','')}\n\nTRANSCRIPT ({len(txt)} chars):\n{txt}\n")
        print(f"[{r['slot']}] {vid} | {r.get('publish_date')} | {r.get('author')} | {r.get('length_seconds')}s | trans={len(txt)}c | {r.get('title')}")
        if r.get("transcript_error"):
            print(f"    T_ERR: {r['transcript_error'][:120]}")
