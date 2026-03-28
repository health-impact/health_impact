import feedparser
import json
from datetime import datetime
import os

sources = {
    "WHO": "https://www.who.int/feeds/entity/csr/don/ar/rss.xml",
    "FDA": "https://www.fda.gov/about-fda/contact-fda/rss-feeds/press-releases/rss.xml",
    "NCDC": "https://ncdc.gov.ly/rss"  # مثال
}

tips = []

for source, url in sources.items():
    feed = feedparser.parse(url)
    for entry in feed.entries[:2]:
        tips.append({
            "title": entry.title,
            "content": entry.summary,
            "source": source
        })

tips = tips[:5]

# لو فيه ملف قديم latest.json نقارن
latest_path = "data/tips/latest.json"
if os.path.exists(latest_path):
    with open(latest_path, "r", encoding="utf-8") as f:
        old_tips = json.load(f)
else:
    old_tips = []

# لو النصائح الجديدة مختلفة عن القديمة، نكتبها
if tips != old_tips:
    with open(latest_path, "w", encoding="utf-8") as f:
        json.dump(tips, f, ensure_ascii=False, indent=2)

    archive_name = f"data/tips/archive-{datetime.now().strftime('%Y-%m-%d-%H%M')}.json"
    with open(archive_name, "w", encoding="utf-8") as f:
        json.dump(tips, f, ensure_ascii=False, indent=2)

    print("✅ نصائح جديدة تم حفظها")
else:
    print("ℹ️ لا توجد نصائح جديدة، لم يتم التحديث")
