"""scripts/fetch_doc_sources.py
Fetches the public Google Doc with research reference links and evidence for MkrfVSVO5m0.
"""
import urllib.request
import re

doc_url = "https://docs.google.com/document/d/1ZqFU7UuQuyzmERSzhtV1bL7qRgnJXf3nKj_mKzZ_zYM/export?format=txt"
req = urllib.request.Request(doc_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req) as resp:
        text = resp.read().decode('utf-8', errors='ignore')
        print("Fetched doc text length:", len(text))
        print("Doc preview:\n", text[:2000])
        with open("scripts/gaurav_thakur_research_doc.txt", "w", encoding="utf-8") as f:
            f.write(text)
except Exception as e:
    print("Error with export?format=txt:", e)
    # try normal page
    doc_url2 = "https://docs.google.com/document/d/1ZqFU7UuQuyzmERSzhtV1bL7qRgnJXf3nKj_mKzZ_zYM/edit?usp=sharing"
    try:
        req2 = urllib.request.Request(doc_url2, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req2) as resp2:
            html = resp2.read().decode('utf-8', errors='ignore')
            print("Fetched html length:", len(html))
            # look for DOCS_modelChunk
            chunks = re.findall(r'"s":"([^"]+)"', html)
            print("Found chunks:", len(chunks))
            full_text = " ".join(chunks)
            print("Snippet:", full_text[:1000])
            with open("scripts/gaurav_thakur_research_doc.txt", "w", encoding="utf-8") as f:
                f.write(full_text)
    except Exception as e2:
        print("Error fetching normal page:", e2)
