import feedparser
from deep_translator import GoogleTranslator
import json
import os
from datetime import datetime

# مصادر صحية موثوقة
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
                tips.append({
                    "category": category,
                    "source": source_name,
                    "original": simplified,
                    "content": translated
                })
                seen.add(simplified)
            if len(tips) >= 5:
                break
        if len(tips) >= 5:
            break

    # لو ما وصلناش ٥ نصائح، نكمل بنصائح ثابتة ونطبع رسالة واضحة
    if len(tips) < 5:
        print("⚠️ لم يتم العثور على ٥ نصائح من المصادر، سيتم استخدام نصائح جاهزة (fallback).")
    while len(tips) < 5:
        fallback = {
            "category": "عام",
            "source": "Fallback",
            "original": "Stay hydrated and drink enough water daily",
            "content": "احرص على شرب كمية كافية من الماء يومياً"
        }
        tips.append(fallback)

    os.makedirs("data/tips", exist_ok=True)
    latest_path = "data/tips/latest.json"
    archive_path = f"data/tips/archive-{datetime.now().strftime('%Y-%m-%d')}.json"

    with open(latest_path, "w", encoding="utf-8") as f:
        json.dump(tips, f, ensure_ascii=False, indent=2)

    with open(archive_path, "w", encoding="utf-8") as f:
        json.dump(tips, f, ensure_ascii=False, indent=2)

    print(f"✅ كتبت {latest_path} وعدد النصائح {len(tips)}")
    print(f"✅ أرشفت في {archive_path}")

if __name__ == "__main__":
    main()
