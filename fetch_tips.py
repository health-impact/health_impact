import feedparser
import json
from datetime import datetime
import os
from deep_translator import GoogleTranslator

sources = {
    "WHO": "https://www.who.int/rss-feeds/news-english.xml",
    "FDA": "https://www.fda.gov/about-fda/contact-fda/rss-feeds/press-releases/rss.xml"
}

tips = []
translator = GoogleTranslator(source='en', target='ar')

def simplify_tip(text):
    # تبسيط النصيحة للمواطنين
    if "vaccine" in text.lower():
        return "احرص على أخذ اللقاحات الموصى بها لحماية نفسك وعائلتك."
    elif "hand" in text.lower():
        return "اغسل يديك جيدًا بالماء والصابون لمدة 20 ثانية."
    elif "food" in text.lower() or "nutrition" in text.lower():
        return "تناول وجبات صحية ومتوازنة لدعم جهاز المناعة."
    elif "exercise" in text.lower():
        return "مارس الرياضة يوميًا ولو نصف ساعة."
    else:
        # لو النص مش واضح، نترجمه ونخليه كما هو
        return translator.translate(text)

for source, url in sources.items():
    feed = feedparser.parse(url)
    for entry in feed.entries[:5]:
        content_ar = translator.translate(entry.summary)
        tip_ar = simplify_tip(entry.summary)

        tips.append({
            "title": translator.translate(entry.title),
            "content": tip_ar,
            "source": source
        })

tips = tips[:5]

latest_path = "data/tips/latest.json"

if os.path.exists(latest_path):
    with open(latest_path, "r", encoding="utf-8") as f:
        old_tips = json.load(f)
else:
    old_tips = []

if tips and tips != old_tips:
    with open(latest_path, "w", encoding="utf-8") as f:
        json.dump(tips, f, ensure_ascii=False, indent=2)

    archive_name = f"data/tips/archive-{datetime.now().strftime('%Y-%m-%d-%H%M')}.json"
    with open(archive_name, "w", encoding="utf-8") as f:
        json.dump(tips, f, ensure_ascii=False, indent=2)

    print("✅ نصائح جديدة مبسطة للمواطنين تم حفظها")
else:
    print("ℹ️ لا توجد نصائح جديدة، لم يتم التحديث")
