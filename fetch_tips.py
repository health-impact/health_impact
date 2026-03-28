import feedparser
import json
from datetime import datetime

# روابط RSS من المصادر الرسمية
sources = {
    "WHO": "https://www.who.int/feeds/entity/csr/don/ar/rss.xml",
    "FDA": "https://www.fda.gov/about-fda/contact-fda/rss-feeds/press-releases/rss.xml",
    "NCDC": "https://ncdc.gov.ly/rss"  # مثال، لو فيه رابط رسمي
}

tips = []

for source, url in sources.items():
    feed = feedparser.parse(url)
    for entry in feed.entries[:2]:  # ناخذ 2 من كل مصدر
        tips.append({
            "title": entry.title,
            "content": entry.summary,
            "source": source
        })

# نخلي بس 5 نصائح
tips = tips[:5]

# نخزنها في ملف JSON
with open("data/tips/latest.json", "w", encoding="utf-8") as f:
    json.dump(tips, f, ensure_ascii=False, indent=2)

# نعمل نسخة أرشيفية بتاريخ اليوم
archive_name = f"data/tips/archive-{datetime.now().date()}.json"
with open(archive_name, "w", encoding="utf-8") as f:
    json.dump(tips, f, ensure_ascii=False, indent=2)
