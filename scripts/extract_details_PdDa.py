# scripts/extract_details_PdDa.py
import re

with open("scripts/transcript_PdDa0pCmsrY_hi.txt", "r", encoding="utf-8") as f:
    text = f.read()

def search_terms(term, count=3):
    matches = list(re.finditer(term, text))
    print(f"=== Term: '{term}' (Total: {len(matches)}) ===")
    for m in matches[:count]:
        start = max(0, m.start() - 100)
        end = min(len(text), m.end() + 200)
        print("...")
        print(text[start:end].replace("\n", " "))
        print("...")
    print()

search_terms(r"एनएसए|NSA")
search_terms(r"साइबर|Cyber")
search_terms(r"इमरजेंसी|Emergency|किट")
search_terms(r"स्कॉट बेसेंट|Scott Bessent|ट्रेजरी|9 दिन")
search_terms(r"बैंक|पासबुक|चेस|वेल्स")
search_terms(r"गोल्ड|सोना")
search_terms(r"कनाडा|यूके|ऑस्ट्रेलिया|फाइव आईज")
search_terms(r"असुर|धर्म|सिविलाइजेशन")
search_terms(r"धोलेरा|Dholera|मोदी")
