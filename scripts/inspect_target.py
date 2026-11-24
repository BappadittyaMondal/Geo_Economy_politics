"""scripts/inspect_target.py
Inspects YouTube video MkrfVSVO5m0.
"""
import urllib.request
import re
import json

url = "https://www.youtube.com/watch?v=MkrfVSVO5m0"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        
    title_match = re.search(r'<title>(.*?)</title>', html)
    print("PAGE TITLE:", title_match.group(1) if title_match else "None")
    
    # Try finding ytInitialPlayerResponse
    m = re.search(r'ytInitialPlayerResponse\s*=\s*({.*?});', html)
    if m:
        data = json.loads(m.group(1))
        videoDetails = data.get('videoDetails', {})
        print("VIDEO TITLE:", videoDetails.get('title'))
        print("AUTHOR:", videoDetails.get('author'))
        print("LENGTH SECONDS:", videoDetails.get('lengthSeconds'))
        print("VIEW COUNT:", videoDetails.get('viewCount'))
        print("KEYWORDS:", videoDetails.get('keywords', [])[:10])
        print("SHORT DESCRIPTION:\n", videoDetails.get('shortDescription', '')[:1000])
    else:
        # Fallback search
        desc_match = re.search(r'"shortDescription":"(.*?)"', html)
        if desc_match:
            print("DESC SNIPPET:", desc_match.group(1)[:500])
        author_match = re.search(r'"author":"(.*?)"', html)
        if author_match:
            print("AUTHOR:", author_match.group(1))

except Exception as e:
    print("ERROR:", e)
