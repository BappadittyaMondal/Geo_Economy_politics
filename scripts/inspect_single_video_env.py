import urllib.request
import re
import json

vid = "ENvsxdIB8TA"
url = f"https://www.youtube.com/watch?v={vid}"

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req, timeout=12) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
    
    title_m = re.search(r'<title>(.*?)</title>', html)
    title = title_m.group(1).replace(' - YouTube', '').strip() if title_m else 'Unknown'
    
    author_m = re.search(r'"author":"(.*?)"', html)
    author = author_m.group(1) if author_m else ''
    
    length_m = re.search(r'"lengthSeconds":"(.*?)"', html)
    length = length_m.group(1) if length_m else ''
    
    desc_m = re.search(r'"shortDescription":"(.*?)"', html)
    desc = desc_m.group(1) if desc_m else ''
    
    res = {
        'id': vid,
        'url': url,
        'title': title,
        'author': author,
        'duration_sec': length,
        'desc_snippet': desc[:1000]
    }
    print("Metadata fetched:")
    print(json.dumps(res, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Error fetching metadata: {e}")
