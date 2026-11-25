"""scripts/dump_12_transcripts.py
Splits and formats all 12 transcripts + descriptions into clean readable chunks for forensic reading.
"""
import json

with open("scripts/targets_12_20261125_deep.json", "r", encoding="utf-8") as f:
    videos = json.load(f)

with open("scripts/targets_12_20261125_readable.txt", "w", encoding="utf-8") as out:
    for v in videos:
        out.write("=" * 90 + "\n")
        out.write(f"[{v['index']:02d}] ID: {v['video_id']} | Author: {v.get('author')} | Date: {v.get('publish_date')} | Dur: {v.get('length_seconds')}s | Views: {v.get('view_count')}\n")
        out.write(f"Title: {v.get('title')}\n")
        out.write(f"URL: {v['url']}\n")
        out.write(f"Keywords: {', '.join(v.get('keywords', []))}\n")
        out.write(f"Description:\n{v.get('short_description', '').strip()}\n")
        t = v.get("transcript_text", "")
        out.write(f"Transcript Method: {v.get('transcript_method')} | Total Chars: {len(t)}\n")
        # Write full transcript (if very long like Amit Dubey 7936s, write clean full text or inspect)
        out.write(f"Transcript:\n{t}\n\n")

print("Dumped readable file.")
import os
print("File size bytes:", os.path.getsize("scripts/targets_12_20261125_readable.txt"))
for v in videos:
    print(f"[{v['index']:02d}] {v['video_id']} ({v.get('author')}): desc={len(v.get('short_description',''))}, trans={len(v.get('transcript_text',''))}")
