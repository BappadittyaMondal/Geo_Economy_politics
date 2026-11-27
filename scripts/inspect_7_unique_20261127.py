"""scripts/inspect_7_unique_20261127.py
Fetches metadata, descriptions, keywords, and full transcripts for the 8 submitted links
(7 unique video IDs; slot 8 duplicates slot 1 RuBSdqXCqiw) on 2026-11-27.
"""
import concurrent.futures
import json
import re
import urllib.parse
import urllib.request
from youtube_transcript_api import YouTubeTranscriptApi

URLS = [
    ("01", "https://www.youtube.com/watch?v=RuBSdqXCqiw"),
    ("02", "https://www.youtube.com/watch?v=9TjSNSdiPnA"),
    ("03", "https://www.youtube.com/watch?v=qa31tANX0tU&pp=ugUEEgJoadIHCQk3CAGHKiGM7w%3D%3D"),
    ("04", "https://www.youtube.com/watch?v=GnYmmUkO4qQ"),
    ("05", "https://www.youtube.com/watch?v=qPpC9eNvUvI"),
    ("06", "https://www.youtube.com/watch?v=dZt16wkcGXc&pp=ugUEEgJoaQ%3D%3D"),
    ("07", "https://www.youtube.com/watch?v=HyAkTlFHNtw"),
    ("08_dup1", "https://www.youtube.com/watch?v=RuBSdqXCqiw"),
]

def extract_vid(url):
    return urllib.parse.parse_qs(urllib.parse.urlparse(url).query).get("v", [""])[0]

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
        t_list = api.fetch(vid, languages=["en", "hi", "en-US", "en-IN", "bn", "mr"])
        res["transcript_text"] = " ".join([x.text for x in t_list])
    except Exception as e:
        res["transcript_text"] = ""
        res["transcript_error"] = str(e)
    return res

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as ex:
        results = list(ex.map(fetch_one, UNIQUE))
    with open("scripts/targets_7_20261127_meta.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    for r in results:
        vid = r["video_id"]
        txt = r.get("transcript_text", "")
        with open(f"scripts/v27_{r['slot']}_{vid}.txt", "w", encoding="utf-8") as out:
            out.write(f"SLOT: {r['slot']} | ID: {vid} | AUTHOR: {r.get('author')}\n")
            out.write(f"DATE: {r.get('publish_date')} | DUR: {r.get('length_seconds')}s | VIEWS: {r.get('view_count')}\n")
            out.write(f"TITLE: {r.get('title')}\nKEYWORDS: {r.get('keywords')}\n")
            out.write(f"DESCRIPTION:\n{r.get('short_description','')}\n\nTRANSCRIPT ({len(txt)} chars):\n{txt}\n")
        print(f"[{r['slot']}] {vid} | {r.get('publish_date')} | {r.get('author')} | {r.get('length_seconds')}s | {r.get('view_count')} views | trans={len(txt)}c | {r.get('title')}")
        if r.get("transcript_error"):
            print(f"    T_ERR: {r['transcript_error'][:120]}")
