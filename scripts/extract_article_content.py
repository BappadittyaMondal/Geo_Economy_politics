"""
scripts/extract_article_content.py
"""
import urllib.request
from bs4 import BeautifulSoup
import re

urls = [
    ("moneycontrol", "https://www.moneycontrol.com/news/opinion/the-rupee-may-have-fallen-too-far-what-does-this-mean-for-stock-markets-14085354.html"),
    ("et_cea", "https://economictimes.indiatimes.com/news/economy/finance/should-india-really-wish-for-a-stronger-rupee-as-it-turns-a-corner-problems-and-advantages-stronger-and-weaker-rupee-trade-it-sector-exports-cea-anantha-nageswaran/articleshow/135983023.cms"),
    ("et_bfsi", "https://bfsi.economictimes.indiatimes.com/articles/india-rupee-global-risk-jitters-bolster-rupee-as-investors-turn-to-indian-assets/136010923"),
    ("thehindu", "https://www.thehindu.com/business/Industry/rupee-settles-above-93-level-after-seven-months-on-fii-flows/article71724100.ece")
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

for tag, url in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            soup = BeautifulSoup(html, 'html.parser')
            
            # Title
            h1 = soup.find('h1')
            title = h1.get_text().strip() if h1 else (soup.title.get_text().strip() if soup.title else tag)
            
            # Extract paragraphs
            article_body = soup.find(['article', 'div'], class_=re.compile(r'(article|content|story|body)', re.I)) or soup
            paras = [p.get_text().strip() for p in article_body.find_all('p') if len(p.get_text().strip()) > 40]
            
            print(f"==================== {tag.upper()} ====================")
            print(f"Title: {title}")
            print(f"Paragraphs found: {len(paras)}")
            full_body = "\n\n".join(paras)
            print(f"Body preview:\n{full_body[:1000]}\n")
            
            with open(f"scripts/{tag}_clean.txt", "w", encoding="utf-8") as f:
                f.write(f"TITLE: {title}\nURL: {url}\n\n{full_body}")
    except Exception as e:
        print(f"Error {tag}: {e}")
