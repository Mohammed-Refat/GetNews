import json, os, requests, feedparser
from urllib.parse import quote

TOKEN, CHAT = os.environ["TG_TOKEN"], os.environ["TG_CHAT_ID"]

def gnews(q, hl="ar", gl="EG", ceid="EG:ar"):
    return f"https://news.google.com/rss/search?q={quote(q)}&hl={hl}&gl={gl}&ceid={ceid}"

FEEDS = [
    gnews("عقارات الساحل الشمالي"),
    gnews("عقارات العين السخنة"),
    gnews("رأس سدر مشروعات"),
    gnews("السوق العقاري مصر"),
    gnews("التمويل العقاري البنك المركزي"),
    gnews("Egypt real estate", "en", "EG", "EG:en"),
]

seen = set(json.load(open("seen.json"))) if os.path.exists("seen.json") else set()
new = []
for url in FEEDS:
    for e in feedparser.parse(url).entries[:15]:
        key = e.get("id") or e.link
        if key not in seen:
            seen.add(key)
            new.append(e)

for e in new[:20]:
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={"chat_id": CHAT, "text": f" {e.title}\n{e.link}"},
        timeout=20,
    )

json.dump(list(seen)[-2000:], open("seen.json", "w"))
