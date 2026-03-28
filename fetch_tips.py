#!/usr/bin/env python3
# fetch_tips.py
import os
import json
import re
from datetime import datetime
import feedparser

# اختياري: استبدل بمترجمك أو API key إذا لزم
try:
    from deep_translator import GoogleTranslator
    TRANSLATOR_AVAILABLE = True
except Exception:
    TRANSLATOR_AVAILABLE = False

# إعدادات
os.makedirs("data/tips", exist_ok=True)
LATEST_PATH = "data/tips/latest.json"
ARCHIVE_PREFIX = "data/tips/archive-"

# قائمة مصادر بيضاء متخصصة نصائح وإرشادات للمواطن
SOURCES = {
    "WHO": "https://www.who.int/rss-feeds/news-english.xml",
    "CDC": "https://www.cdc.gov/feed.xml",
    # أضف هنا روابط RSS موثوقة محلية أو إقليمية لوزارة الصحة أو مواقع إرشادية
    # "MinistryOfHealth": "https://example.gov/health/rss"
}

# كلمات مفتاحية إيجابية وسلبية لتحسين الصلة
POSITIVE_KEYWORDS = {
    "vaccine","vaccination","immunize","immunity",
    "hand","wash","hygiene","soap","sanitize",
    "water","hydrate","dehydration",
    "nutrition","diet","food","healthy","calories",
    "exercise","activity","fitness","workout",
    "smoking","quit smoking","tobacco",
    "sleep","insomnia","rest","mental health",
    "pregnancy","child","baby","infant","elderly",
    "fever","cough","symptom","prevent","prevention","treatment","first aid"
}

NEGATIVE_KEYWORDS = {
    "election","vote","stock","market","court","policy","minister","parliament",
    "economy","inflation","budget","tax","currency","trade"
}

# تنظيف نص واستخراج جمل
def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'\r\n|\r', '\n', text)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def contains_any(text, keywords):
    t = text.lower()
    return any(k in t for k in keywords)

def is_relevant(raw_text):
    text = clean_text(raw_text)
    if not text:
        return False, "empty"
    if len(text) < 30:
        return False, "too_short"
    if len(text) > 2000:
        return False, "too_long"
    if contains_any(text, NEGATIVE_KEYWORDS):
        return False, "negative_keyword"
    if contains_any(text, POSITIVE_KEYWORDS):
        return True, "positive_keyword"
    return False, "no_positive_keyword"

def extract_tip(raw_text):
    ok, reason = is_relevant(raw_text)
    if not ok:
        return None, reason
    text = clean_text(raw_text)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    for s in sentences:
        if contains_any(s, POSITIVE_KEYWORDS) and len(s) > 20:
            return s.strip(), "accepted_sentence"
    # fallback: take first meaningful chunk
    return text[:200].strip(), "accepted_fallback"

# ترجمة آمنة لجملة واحدة فقط
def safe_translate(text, src='en', tgt='ar'):
    if not text:
        return text
    if TRANSLATOR_AVAILABLE:
        try:
            return GoogleTranslator(source=src, target=tgt).translate(text)
        except Exception as e:
            print("⚠️ ترجمة فشلت:", e)
            return text
    else:
        # لو المترجم غير متوفر نعيد النص الأصلي
        return text

# جمع ومعالجة الخلاصات
def fetch_and_process():
    tips = []
    rejected = []
    for source_name, url in SOURCES.items():
        print(f"⤷ جلب من {source_name} ({url})")
        try:
            feed = feedparser.parse(url)
        except Exception as e:
            print(f"⚠️ خطأ في جلب {source_name}: {e}")
            continue
        entries = feed.entries or []
        print(f"   - وجدت {len(entries)} مدخلات")
        for entry in entries[:10]:
            title = entry.get('title', '') or ''
            summary = entry.get('summary', '') or entry.get('description', '') or ''
            preview = (title + " " + summary)[:800]
            raw = summary if summary else title
            tip_text, reason = extract_tip(raw)
            if tip_text:
                # ترجمة الجملة المختارة فقط
                translated_tip = safe_translate(tip_text)
                translated_title = safe_translate(title) if title else translated_tip[:60]
                tips.append({
                    "title": translated_title,
                    "content": translated_tip,
                    "source": source_name,
                    "meta": {"reason": reason, "preview": preview[:200]}
                })
                print(f"   ✅ مقبول من {source_name}: {reason} -- preview: {preview[:80]}")
            else:
                rejected.append({"source": source_name, "reason": reason, "preview": preview[:120]})
                print(f"   ❌ مرفوض من {source_name}: {reason} -- preview: {preview[:80]}")
    return tips, rejected

# كتابة وادراج fallback لو لزم
def ensure_minimum_tips(tips, min_count=5):
    if len(tips) >= min_count:
        return tips
    print("ℹ️ عدد النصائح غير كاف، إضافة نصائح محلية افتراضية")
    fallback = [
        {"title":"اشرب ماء نظيف","content":"اشرب ماء نظيف يوميًا لتجنب الأمراض المعوية.","source":"Local"},
        {"title":"غسل الخضروات","content":"اغسل الخضروات والفواكه جيدًا قبل الأكل.","source":"Local"},
        {"title":"التطعيمات الأساسية","content":"تأكد من حصول الأطفال على التطعيمات الأساسية في مواعيدها.","source":"Local"},
        {"title":"النظافة الشخصية","content":"اغسل يديك بانتظام خاصة قبل الأكل وبعد استخدام المرحاض.","source":"Local"},
        {"title":"النشاط البدني","content":"مارس نشاطًا بدنيًا يوميًا ولو 30 دقيقة لتحسين الصحة العامة.","source":"Local"}
    ]
    for f in fallback:
        tips.append({"title": f["title"], "content": f["content"], "source": f["source"], "meta": {"reason": "fallback"}})
    return tips[:min_count]

def write_latest_and_archive(tips):
    now = datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
    archive_path = f"{ARCHIVE_PREFIX}{now}.json"
    try:
        with open(LATEST_PATH, "w", encoding="utf-8") as f:
            json.dump(tips, f, ensure_ascii=False, indent=2)
        with open(archive_path, "w", encoding="utf-8") as f:
            json.dump(tips, f, ensure_ascii=False, indent=2)
        print(f"✅ كتبت {LATEST_PATH} وعدد النصائح {len(tips)}")
        print(f"✅ أرشفت في {archive_path}")
    except Exception as e:
        print("⚠️ خطأ عند الكتابة:", e)

def main():
    print("START fetch_tips")
    tips, rejected = fetch_and_process()
    tips = ensure_minimum_tips(tips, min_count=5)
    # نأخذ أول 5 نصائح فريدة حسب المحتوى
    unique = []
    seen = set()
    for t in tips:
        key = (t.get("content","").strip()[:120])
        if key not in seen:
            seen.add(key)
            unique.append(t)
        if len(unique) >= 5:
            break
    write_latest_and_archive(unique)
    # طباعة ملخص للـ logs
    print("---- Summary ----")
    print(f"Accepted tips: {len(unique)}")
    print(f"Rejected entries: {len(rejected)}")
    if rejected:
        print("Sample rejections:")
        for r in rejected[:5]:
            print(f" - {r['source']}: {r['reason']} -- {r['preview'][:80]}")
    print("END fetch_tips")

if __name__ == "__main__":
    main()
