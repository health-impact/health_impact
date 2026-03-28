import feedparser, json, os
from datetime import datetime
from deep_translator import GoogleTranslator

os.makedirs("data/tips", exist_ok=True)

sources = {
    "WHO": "https://www.who.int/rss-feeds/news-english.xml",
    "FDA": "https://www.fda.gov/about-fda/contact-fda/rss-feeds/press-releases/rss.xml"
}

translator = GoogleTranslator(source='en', target='ar')

def safe_translate(text, chunk_size=4000):
    try:
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        translated_chunks = [translator.translate(chunk) for chunk in chunks]
        return " ".join(translated_chunks)
    except Exception as e:
        print("⚠️ ترجمة فشلت:", e)
        return text

def simplify_tip(text):
    t = text.lower()
    if "vaccine" in t: return "احرص على أخذ اللقاحات الموصى بها لحماية نفسك وعائلتك."
    if "hand" in t or "wash" in t: return "اغسل يديك جيدًا بالماء والصابون لمدة 20 ثانية."
    if "food" in t or "nutrition" in t: return "تناول وجبات صحية ومتوازنة لدعم جهاز المناعة."
    if "exercise" in t or "activity" in t: return "مارس الرياضة يوميًا ولو نصف ساعة."
    if "smoking" in t: return "تجنب التدخين لأنه يزيد من خطر أمراض القلب والرئة."
    return safe_translate(text)

tips = []
for source, url in sources.items():
    print(f"⤷ جلب من {source}")
    feed = feedparser.parse(url)
    for entry in feed.entries[:5]:
        try:
            tip_ar = simplify_tip(entry.get('summary', entry.get('title', '')))
            tips.append({
                "title": safe_translate(entry.get('title', '')),
                "content": tip_ar,
                "source": source
            })
        except Exception as e:
            print("⚠️ خطأ معالجة entry:", e)

# fallback لو النصائح غير كافية أو غير مناسبة
if len(tips) < 5:
    print("ℹ️ استخدام نصائح محلية افتراضية")
    fallback = [
        {"title":"اشرب ماء نظيف","content":"اشرب ماء نظيف يوميًا لتجنب الأمراض المعوية.","source":"Local"},
        {"title":"غسل الخضروات","content":"اغسل الخضروات والفواكه جيدًا قبل الأكل.","source":"Local"},
        {"title":"التطعيمات للأطفال","content":"تأكد من حصول أطفالك على التطعيمات الأساسية في مواعيدها.","source":"Local"},
        {"title":"النظافة الشخصية","content":"اغسل يديك بانتظام خاصة قبل الأكل وبعد استخدام المرحاض.","source":"Local"},
        {"title":"التغذية السليمة","content":"قلل من استهلاك الملح والزيوت لتجنب ارتفاع ضغط الدم.","source":"Local"}
    ]
    tips.extend(fallback)

tips = tips[:5]

latest_path = "data/tips/latest.json"
archive_name = f"data/tips/archive-{datetime.now().strftime('%Y-%m-%d-%H%M')}.json"

# Force write مع طباعة للمراجعة
with open(latest_path, "w", encoding="utf-8") as f:
    json.dump(tips, f, ensure_ascii=False, indent=2)
print(f"✅ كتبت {latest_path} بعدد {len(tips)} نصائح")

with open(archive_name, "w", encoding="utf-8") as f:
    json.dump(tips, f, ensure_ascii=False, indent=2)
print(f"✅ أرشفت في {archive_name}")
