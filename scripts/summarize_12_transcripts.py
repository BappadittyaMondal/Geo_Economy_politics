"""scripts/summarize_12_transcripts.py
Prints structured inspection of all 12 videos from targets_12_20261125_deep.json.
"""
import json

with open("scripts/targets_12_20261125_deep.json", "r", encoding="utf-8") as f:
    videos = json.load(f)

for v in videos:
    vid = v["video_id"]
    t = v.get("transcript_text", "")
    d = v.get("short_description", "")
    # For shorter transcripts (< 25000 chars), write into individual files for fast clean reading, or print key slices
    with open(f"scripts/v_{v['index']:02d}_{vid}.txt", "w", encoding="utf-8") as out:
        out.write(f"INDEX: {v['index']:02d}\n")
        out.write(f"ID: {vid}\n")
        out.write(f"AUTHOR: {v.get('author')}\n")
        out.write(f"DATE: {v.get('publish_date')}\n")
        out.write(f"DURATION_S: {v.get('length_seconds')}\n")
        out.write(f"VIEWS: {v.get('view_count')}\n")
        out.write(f"TITLE: {v.get('title')}\n")
        out.write(f"KEYWORDS: {v.get('keywords')}\n")
        out.write(f"DESCRIPTION:\n{d}\n\n")
        out.write(f"TRANSCRIPT ({len(t)} chars):\n{t}\n")
    print(f"[{v['index']:02d}] {vid} -> scripts/v_{v['index']:02d}_{vid}.txt ({len(t)} trans chars)")
