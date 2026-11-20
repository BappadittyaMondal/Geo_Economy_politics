# scripts/analyze_transcript_PdDa.py
with open("scripts/transcript_PdDa0pCmsrY_hi.txt", "r", encoding="utf-8") as f:
    text = f.read()

print("Total characters:", len(text))
print("Total words:", len(text.split()))

import re

# Let's inspect sections
step = len(text) // 12
for i in range(12):
    start = i * step
    print(f"=== SEGMENT {i+1} (approx {i*6} min) ===")
    print(text[start:start+450])
    print()
