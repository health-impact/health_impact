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

def safe_translate(text, chunk_size=4000):
    # نقسم النص الطويل إلى أجزاء صغيرة ونترجم كل جزء
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    translated_chunks = [translator.translate(chunk) for chunk in chunks]
    return " ".join(translated_chunks)

def simplify_tip(text):
    text_lower = text.lower()
    if "vaccine" in text_lower:
        return "احرص على أخذ اللقاحات الموصى بها لحماية نفسك وعائلتك."
    elif "hand" in text_lower or "wash" in text_lower:
        return "اغسل يديك جيدًا بالماء والصابون لمدة 20 ثانية."
    elif "food" in text_lower or "nutrition" in text_lower:
        return "تناول وجبات صحية ومتوازنة لدعم جهاز المناعة."
    elif "exercise" in text_lower or "activity" in text_lower:
        return "مارس الرياضة يوميًا ولو نصف ساعة."
    elif "smoking" in text_lower:
        return "تجنب التدخين لأنه يزيد من خطر أمراض القلب والرئة."
    else:
        return safe_translate(text)

for source, url in sources.items():
    feed = feedparser.parse(url)
    for entry in feed.entries[:5]:  # ناخذ أكثر لضمان 5 نصائح
        tip_ar = simplify_tip(entry.summary)
        tips.append({
            "title": safe_translate(entry.title),
            "content": tip_ar,
            "source": source
        })

# نخلي بس 5 نصائح نهائية
tips = tips[:5]

latest_path = "data/tips/latest.json"

# نقارن مع النصائح القديمة لو موجودة
if os.path.exists(latest_path):
    with open(latest_path, "r", encoding="utf-8") as f:
        old_tips = json.load(f)
else:
    old_tips = []

# لو فيه جديد نكتبها + أرشفة
if tips and tips != old_tips:
    with open(latest_path, "w", encoding="utf-8") as f:
        json.dump(tips, f, ensure_ascii=False, indent=2)

    archive_name = f"data/tips/archive-{datetime.now().strftime('%Y-%m-%d-%H%M')}.json"
    with open(archive_name, "w", encoding="utf-8") as f:
        json.dump(tips, f, ensure_ascii=False, indent=2)

    print("✅ نصائح جديدة مبسطة للمواطنين تم حفظها مع أرشفة")
else:
    print("ℹ️ لا توجد نصائح جديدة، لم يتم التحديث")
