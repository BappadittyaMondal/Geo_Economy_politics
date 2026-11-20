# scripts/read_segments.py
with open("scripts/transcript_PdDa0pCmsrY_hi.txt", "r", encoding="utf-8") as f:
    text = f.read()

sentences = text.split("।")

def print_range(start, end):
    print(f"=== Sentences {start} to {end} ===")
    for i in range(start, min(end, len(sentences))):
        print(f"[{i}] {sentences[i].strip().replace(chr(10), ' ')}")
    print()

print_range(0, 45)
print_range(120, 160)
