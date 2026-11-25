"""scripts/inspect_7_targets_20261125.py
Fetches metadata, descriptions, keywords, and full transcripts for 7 YouTube targets.
"""
import concurrent.futures
import json
import re
import urllib.parse
import urllib.request
from youtube_transcript_api import YouTubeTranscriptApi

VIDEOS = [
    "https://www.youtube.com/watch?v=-g3ceK_V1as",
    "https://www.youtube.com/watch?v=Iy-KO051RPY",
    "https://www.youtube.com/watch?v=K-2gxaXJAKM",
    "https://www.youtube.com/watch?v=dab--v8_oW8&pp=0gcJCTcIAYcqIYzv",
    "https://www.youtube.com/watch?v=yHqupzOBCFM",
    "https://www.youtube.com/watch?v=TGVGjDixXZ0",
    "https://www.youtube.com/watch?v=ZNVShd2Qy4Y",
]

def extract_vid(url):
    return urllib.parse.parse_qs(urllib.parse.urlparse(url).query).get("v", [""])[0]

def fetch_one(idx_url):
    idx, url = idx_url
    vid = extract_vid(url)
    clean_url = f"https://www.youtube.com/watch?v={vid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    res = {"index": idx, "video_id": vid, "url": url}
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

    # Fetch transcript
    try:
        api = YouTubeTranscriptApi()
        t_list = api.fetch(vid, languages=["hi", "en", "en-US", "en-IN", "bn"])
        res["transcript_text"] = " ".join([x.text for x in t_list])
    except Exception as e:
        res["transcript_text"] = ""
        res["transcript_error"] = str(e)
    return res

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as ex:
        results = list(ex.map(fetch_one, enumerate(VIDEOS, 1)))
    results.sort(key=lambda x: x["index"])
    with open("scripts/targets_7_20261125_meta.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    for r in results:
        vid = r["video_id"]
        txt = r.get("transcript_text", "")
        with open(f"scripts/v7_{r['index']:02d}_{vid}.txt", "w", encoding="utf-8") as out:
            out.write(f"INDEX: {r['index']:02d}\nID: {vid}\nAUTHOR: {r.get('author')}\n")
            out.write(f"DATE: {r.get('publish_date')} | DUR: {r.get('length_seconds')}s | VIEWS: {r.get('view_count')}\n")
            out.write(f"TITLE: {r.get('title')}\nKEYWORDS: {r.get('keywords')}\n")
            out.write(f"DESCRIPTION:\n{r.get('short_description','')}\n\nTRANSCRIPT ({len(txt)} chars):\n{txt}\n")
        print(f"[{r['index']:02d}] {vid} | {r.get('publish_date')} | {r.get('author')} | {r.get('length_seconds')}s | trans={len(txt)}c | {r.get('title')}")
        if r.get("transcript_error"):
            print(f"     T_ERR: {r['transcript_error'][:120]}")
