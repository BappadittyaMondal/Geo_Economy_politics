# scripts/outline_transcript.py
with open("scripts/transcript_PdDa0pCmsrY_hi.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Let's break by sentences and extract key themes
sentences = text.split("।")
print("Total sentences:", len(sentences))

for i, s in enumerate(sentences):
    s_clean = s.strip().replace("\n", " ")
    if any(k in s_clean for k in ["एनएसए", "साइबर सिक्योरिटी", "स्कॉट बेसेंट", "9 दिन", "इमरजेंसी किट", "पासबुक", "गिफ्ट सिटी", "टू फैक्टर", "जेन फुरले", "CISA"]):
        print(f"[{i}] {s_clean[:140]}...")
