import urllib.request
import json
import re

url = 'https://www.youtube.com/watch?v=PdDa0pCmsrY'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
    
    title_m = re.search(r'<title>(.*?)</title>', html)
    title = title_m.group(1) if title_m else 'Unknown'
    
    desc_m = re.search(r'"shortDescription":"(.*?)"', html)
    desc = desc_m.group(1) if desc_m else ''
    
    author_m = re.search(r'"author":"(.*?)"', html)
    author = author_m.group(1) if author_m else ''
    
    length_m = re.search(r'"lengthSeconds":"(.*?)"', html)
    length = length_m.group(1) if length_m else ''
    
    print('Title:', title)
    print('Author:', author)
    print('Length (sec):', length)
    print('Description:', desc[:300])

    with open('scripts/video_PdDa0pCmsrY.txt', 'w', encoding='utf-8') as f:
        f.write(f'Title: {title}\nAuthor: {author}\nLength: {length}\nDescription:\n{desc}\n')
except Exception as e:
    print('Error:', e)
