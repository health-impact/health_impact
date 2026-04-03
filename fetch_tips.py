import feedparser
from deep_translator import GoogleTranslator
import json
import os
from datetime import datetime
from collections import Counter

SOURCES = {
    "WHO": "https://www.who.int/feeds/entity/csr/don/en/rss.xml",
    "CDC": "https://tools.cdc.gov/api/v2/resources/media/403372.rss",
    "UNICEF": "https://www.unicef.org/rss.xml"
}

CATEGORIES = {
    "التغذية": ["nutrition", "diet", "food"],
    "الصحة النفسية": ["mental", "stress", "psychology"],
    "الوقاية": ["prevention", "safety", "protection"],
    "التطعيم": ["vaccine", "immunization"],
    "النظافة": ["hygiene", "clean", "sanitation"]
}

FALLBACK_TIPS = [
    ("التغذية", "Fallback", "Eat more fruits and vegetables", "تناول المزيد من الفواكه والخضروات"),
    ("الصحة النفسية", "Fallback", "Take short breaks to relax", "خذ فترات راحة قصيرة للاسترخاء"),
    ("الوقاية", "Fallback", "Wash your hands regularly", "اغسل يديك بانتظام"),
    ("التطعيم", "Fallback", "Keep your vaccinations up to date", "حافظ على تحديث تطعيماتك"),
    ("النظافة", "Fallback", "Maintain clean surroundings", "حافظ على نظافة البيئة من حولك")
]

def classify_tip(text):
    text_lower = text.lower()
    for category, keywords in CATEGORIES.items():
        if any(word in text_lower for word in keywords):
            return category
    return "عام"

def translate(text):
    return GoogleTranslator(source="en", target="ar").translate(text)

def main():
    tips = []
    seen = set()

    for source_name, url in SOURCES.items():
        feed = feedparser.parse(url)
        for entry in feed.entries:
            text = entry.title + " " + entry.get("summary", "")
            category = classify_tip(text)
            simplified = text.strip().split(".")[0]
            if simplified not in seen:
                translated = translate(simplified)
                tip = {
                    "category": category,
                    "source": source_name,
                    "original": simplified,
                    "content": translated
                }
                tips.append(tip)
                seen.add(simplified)
                print(f"📝 نصيحة: {tip['original']} | التصنيف: {tip['category']} | المصدر: {tip['source']}")
            if len(tips) >= 5:
                break
        if len(tips) >= 5:
            break

    if len(tips) < 5:
        print("⚠️ سيتم استخدام نصائح جاهزة (fallback).")
    i = 0
    while len(tips) < 5 and i < len(FALLBACK_TIPS):
        cat, src, orig, cont = FALLBACK_TIPS[i]
        tip = {
            "category": cat,
            "source": src,
            "original": orig,
            "content": cont
        }
        tips.append(tip)
        print(f"📝 نصيحة (fallback): {tip['original']} | التصنيف: {tip['category']} | المصدر: {tip['source']}")
        i += 1

    os.makedirs("data/tips", exist_ok=True)
    latest_path = "data/tips/latest.json"
    archive_path = f"data/tips/archive-{datetime.now().strftime('%Y-%m-%d')}.json"

    with open(latest_path, "w", encoding="utf-8") as f:
        json.dump(tips, f, ensure_ascii=False, indent=2)

    with open(archive_path, "w", encoding="utf-8") as f:
        json.dump(tips, f, ensure_ascii=False, indent=2)

    print(f"✅ كتبت {latest_path} وعدد النصائح {len(tips)}")
    print(f"✅ أرشفت في {archive_path}")

    cat_counts = Counter([tip["category"] for tip in tips])
    print("📊 عدد النصائح حسب التصنيف:")
    for cat, count in cat_counts.items():
        print(f"{cat}: {count}")

    sources_used = [tip["source"] for tip in tips]
    print("📊 ملخص المصادر:")
    for src in set(sources_used):
        count = sources_used.count(src)
        print(f"{src}: {count} نصيحة/نصائح")

if __name__ == "__main__":
    main()
