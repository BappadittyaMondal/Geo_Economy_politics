"""scripts/inspect_12_videos_20261125.py
Inspects metadata, descriptions, keywords, chapters, and caption tracks for 12 YouTube videos.
"""
import concurrent.futures
import json
import re
import urllib.request
import urllib.parse

VIDEOS = [
    "https://www.youtube.com/watch?v=MwqeH0mCD88",
    "https://www.youtube.com/watch?v=hYvCrXGgZGk",
    "https://www.youtube.com/watch?v=rvvotSU4Tg0",
    "https://www.youtube.com/watch?v=-g3ceK_V1as",
    "https://www.youtube.com/watch?v=rspjKG4QerM",
    "https://www.youtube.com/watch?v=vs7O8EjQaYA&pp=0gcJCTcIAYcqIYzv",
    "https://www.youtube.com/watch?v=OZqDq8u2FjY&t=121s&pp=ugUEEgJoaQ%3D%3D",
    "https://www.youtube.com/watch?v=_96cG8aY1nY&pp=ugUEEgJoaQ%3D%3D",
    "https://www.youtube.com/watch?v=TvcSRq7mMFU",
    "https://www.youtube.com/watch?v=9eA-tbQbhFk&pp=ugUEEgJoaQ%3D%3D",
    "https://www.youtube.com/watch?v=-MF7OqLxnyw&pp=0gcJCTcIAYcqIYzv",
    "https://www.youtube.com/watch?v=h4tu41A3BH8&pp=ugUEEgJlbg%3D%3D",
]

def extract_video_id(url):
    parsed = urllib.parse.urlparse(url)
    qs = urllib.parse.parse_qs(parsed.query)
    return qs.get("v", [""])[0]

def fetch_video(idx_url):
    idx, url = idx_url
    vid = extract_video_id(url)
    clean_url = f"https://www.youtube.com/watch?v={vid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    req = urllib.request.Request(clean_url, headers=headers)
    result = {"index": idx, "video_id": vid, "url": url}
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        m = re.search(r"ytInitialPlayerResponse\s*=\s*(\{.*?\});", html)
        if m:
            data = json.loads(m.group(1))
            vd = data.get("videoDetails", {})
            mf = data.get("microformat", {}).get("playerMicroformatRenderer", {})
            result["title"] = vd.get("title")
            result["author"] = vd.get("author")
            result["channel_id"] = vd.get("channelId")
            result["length_seconds"] = vd.get("lengthSeconds")
            result["view_count"] = vd.get("viewCount")
            result["publish_date"] = mf.get("publishDate")
            result["upload_date"] = mf.get("uploadDate")
            result["category"] = mf.get("category")
            result["keywords"] = vd.get("keywords", [])
            result["short_description"] = vd.get("shortDescription", "")
            
            # Extract caption track metadata
            captions = data.get("captions", {}).get("playerCaptionsTracklistRenderer", {}).get("captionTracks", [])
            result["captions_available"] = [
                {"lang": c.get("languageCode"), "name": c.get("name", {}).get("simpleText"), "baseUrl": c.get("baseUrl")}
                for c in captions
            ]
        else:
            title_m = re.search(r"<title>(.*?)</title>", html)
            result["title"] = title_m.group(1) if title_m else None
            result["error"] = "ytInitialPlayerResponse not found"
    except Exception as e:
        result["error"] = str(e)
    return result

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        results = list(ex.map(fetch_video, enumerate(VIDEOS, 1)))
    results.sort(key=lambda x: x["index"])
    with open("scripts/targets_12_20261125_metadata.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    for r in results:
        print(f"[{r['index']:02d}] {r['video_id']} | {r.get('publish_date')} | {r.get('author')} | {r.get('length_seconds')}s | {r.get('title')}")
        if r.get("error"):
            print(f"    ERROR: {r['error']}")
