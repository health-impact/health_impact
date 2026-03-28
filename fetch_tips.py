import feedparser
import json
from datetime import datetime
import os
from googletrans import Translator

sources = {
    "WHO": "https://www.who.int/rss-feeds/news-english.xml",
    "FDA": "https://www.fda.gov/about-fda/contact-fda/rss-feeds/press-releases/rss.xml"
}

tips = []
translator = Translator()

# نجلب النصائح من كل مصدر ونترجمها للعربية
for source, url in sources.items():
    feed = feedparser.parse(url)
    for entry in feed.entries[:2]:  # ناخذ 2 من كل مصدر
        title_ar = translator.translate(entry.title, dest="ar").text
        content_ar = translator.translate(entry.summary, dest="ar").text

        tips.append({
            "title": title_ar,
            "content": content_ar,
            "source": source
        })

# نخلي بس 5 نصائح
tips = tips[:5]

latest_path = "data/tips/latest.json"

# نقارن مع النصائح القديمة لو موجودة
if os.path.exists(latest_path):
    with open(latest_path, "r", encoding="utf-8") as f:
        old_tips = json.load(f)
else:
    old_tips = []

# لو فيه جديد نكتبها
if tips and tips != old_tips:
    with open(latest_path, "w", encoding="utf-8") as f:
        json.dump(tips, f, ensure_ascii=False, indent=2)

    archive_name = f"data/tips/archive-{datetime.now().strftime('%Y-%m-%d-%H%M')}.json"
    with open(archive_name, "w", encoding="utf-8") as f:
        json.dump(tips, f, ensure_ascii=False, indent=2)

    print("✅ نصائح جديدة تم حفظها بالعربية")
else:
    print("ℹ️ لا توجد نصائح جديدة، لم يتم التحديث")
