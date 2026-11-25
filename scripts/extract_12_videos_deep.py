"""scripts/extract_12_videos_deep.py
Extracts full descriptions, links, chapters, and attempts caption retrieval via YouTube timedtext formats (json3/srv3/vtt) or installed packages for the 12 videos.
"""
import json
import re
import urllib.request
import xml.etree.ElementTree as ET

with open("scripts/targets_12_20261125_metadata.json", "r", encoding="utf-8") as f:
    videos = json.load(f)

def fetch_caption_text(cap_url):
    for suffix in ["&fmt=json3", "&fmt=srv3", "&fmt=vtt", ""]:
        try:
            url = cap_url + suffix
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
            })
            with urllib.request.urlopen(req, timeout=15) as r:
                raw = r.read().decode("utf-8", errors="ignore")
            if not raw.strip():
                continue
            if suffix == "&fmt=json3" and raw.strip().startswith("{"):
                data = json.loads(raw)
                segs = []
                for ev in data.get("events", []):
                    for s in ev.get("segs", []):
                        txt = s.get("utf8", "").strip()
                        if txt and txt != "\n":
                            segs.append(txt)
                if segs:
                    return " ".join(segs), f"json3 ({len(segs)} segs)"
            elif "<text" in raw or "<p " in raw:
                root = ET.fromstring(raw)
                texts = ["".join(el.itertext()).strip() for el in root.iter() if el.tag in ("text", "p")]
                texts = [t for t in texts if t]
                if texts:
                    return " ".join(texts), f"xml ({len(texts)} segs)"
            elif "WEBVTT" in raw:
                lines = [l.strip() for l in raw.splitlines() if l.strip() and "-->" not in l and l.strip() != "WEBVTT" and not l.strip().isdigit()]
                # strip tags like <00:00:01.000><c>
                clean = [re.sub(r"<[^>]+>", "", l) for l in lines]
                if clean:
                    return " ".join(clean), f"vtt ({len(clean)} lines)"
        except Exception as e:
            continue
    return "", "none"

# Check if youtube_transcript_api or yt_dlp exists
has_yta = False
has_ytdlp = False
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    has_yta = True
except ImportError:
    pass
try:
    import yt_dlp
    has_ytdlp = True
except ImportError:
    pass

print(f"youtube_transcript_api: {has_yta}, yt_dlp: {has_ytdlp}")

deep_results = []
for v in videos:
    vid = v["video_id"]
    print(f"\n=== [{v['index']:02d}] {vid} | {v.get('author')} | {v.get('title')} ===")
    print(f"Length: {v.get('length_seconds')}s | Views: {v.get('view_count')} | Published: {v.get('publish_date')}")
    print("Keywords:", v.get("keywords", [])[:15])
    print("Description:\n", v.get("short_description", "")[:1500])
    
    transcript = ""
    method = "none"
    if has_yta:
        try:
            api = YouTubeTranscriptApi()
            t_list = api.fetch(vid, languages=['hi', 'en', 'en-US', 'en-IN'])
            transcript = " ".join([x.text for x in t_list])
            method = "youtube_transcript_api"
        except Exception as e:
            pass
    if not transcript and v.get("captions_available"):
        # Prefer hi or en
        sorted_caps = sorted(v["captions_available"], key=lambda c: 0 if c["lang"].startswith("en") else (1 if c["lang"].startswith("hi") else 2))
        for c in sorted_caps:
            transcript, m_str = fetch_caption_text(c["baseUrl"])
            if transcript:
                method = f"timedtext/{c['lang']}/{m_str}"
                break
    print(f"Transcript ({method}, len={len(transcript)}):", transcript[:600] if transcript else "[No direct captions retrieved]")
    v["transcript_method"] = method
    v["transcript_text"] = transcript
    deep_results.append(v)

with open("scripts/targets_12_20261125_deep.json", "w", encoding="utf-8") as f:
    json.dump(deep_results, f, indent=2, ensure_ascii=False)
