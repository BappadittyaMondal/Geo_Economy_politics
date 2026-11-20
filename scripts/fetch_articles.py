"""
scripts/fetch_articles.py
"""
import urllib.request
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
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            title_m = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
            title = title_m.group(1).strip() if title_m else "No Title"
            # Strip html tags to get text snippets
            text = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)
            text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL)
            text = re.sub(r'<.*?>', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()
            print(f"=== {tag} ===")
            print(f"Title: {title}")
            print(f"Text sample: {text[:600]}...\n")
            with open(f"scripts/{tag}.txt", "w", encoding="utf-8") as out_f:
                out_f.write(f"Title: {title}\nURL: {url}\n\n{text}")
    except Exception as e:
        print(f"=== {tag} Error: {e}")
