import feedparser
from deep_translator import GoogleTranslator
import json
import os
from datetime import datetime

# روابط RSS اللي نجيب منها النصائح
SOURCES = [
    "https://www.who.int/feeds/entity/csr/don/en/rss.xml",
    "https://www.cdc.gov/rss/rss.asp"
]

# كلمات مفتاحية باش نفلتر النصائح
POSITIVE_KEYWORDS = ["health", "nutrition", "exercise", "hygiene", "vaccination", "prevention"]
NEGATIVE_KEYWORDS = ["politics", "economy", "election", "market", "budget"]

def is_valid_tip(entry):
    text = (entry.title + " " + entry.get("summary", "")).lower()
    if any(word in text for word in NEGATIVE_KEYWORDS):
        return False
    return any(word in text for word in POSITIVE_KEYWORDS)

def simplify(text):
    # تبسيط النص
    return text.strip().split(".")[0]

def translate(text):
    return GoogleTranslator(source="en", target="ar").translate(text)

def main():
    tips = []
    for src in SOURCES:
        feed = feedparser.parse(src)
        for entry in feed.entries:
            if is_valid_tip(entry):
                simplified = simplify(entry.title)
                translated = translate(simplified)
                tips.append({"title": simplified, "content": translated})
            if len(tips) >= 5:
                break
        if len(tips) >= 5:
            break

    os.makedirs("data/tips", exist_ok=True)
    latest_path = "data/tips/latest.json"
    archive_path = f"data/tips/archive-{datetime.now().strftime('%Y-%m-%d-%H%M')}.json"

    with open(latest_path, "w", encoding="utf-8") as f:
        json.dump(tips, f, ensure_ascii=False, indent=2)

    with open(archive_path, "w", encoding="utf-8") as f:
        json.dump(tips, f, ensure_ascii=False, indent=2)

    print(f"✅ كتبت {latest_path} وعدد النصائح {len(tips)}")
    print(f"✅ أرشفت في {archive_path}")

if __name__ == "__main__":
    main()
