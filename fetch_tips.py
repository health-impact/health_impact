import feedparser
import json
from datetime import datetime
import os

# روابط RSS الصحيحة (تقدر تبدلها أو تضيف مصادر أخرى)
sources = {
    "WHO": "https://www.who.int/rss-feeds/news-english.xml",
    "FDA": "https://www.fda.gov/about-fda/contact-fda/rss-feeds/press-releases/rss.xml"
    # لو عندك مصدر ثالث (مثلاً NCDC ليبيا) ضيفه هنا
}

tips = []

# نجلب النصائح من كل مصدر
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

# مسار ملف latest.json
latest_path = "data/tips/latest.json"

# نقارن مع النصائح القديمة لو موجودة
if os.path.exists(latest_path):
    with open(latest_path, "r", encoding="utf-8") as f:
        old_tips = json.load(f)
else:
    old_tips = []

# لو النصائح الجديدة مختلفة عن القديمة، نكتبها
if tips and tips != old_tips:
    with open(latest_path, "w", encoding="utf-8") as f:
        json.dump(tips, f, ensure_ascii=False, indent=2)

    # نخزن نسخة أرشيفية بتاريخ + وقت
    archive_name = f"data/tips/archive-{datetime.now().strftime('%Y-%m-%d-%H%M')}.json"
    with open(archive_name, "w", encoding="utf-8") as f:
        json.dump(tips, f, ensure_ascii=False, indent=2)

    print("✅ نصائح جديدة تم حفظها")
else:
    print("ℹ️ لا توجد نصائح جديدة، لم يتم التحديث")
