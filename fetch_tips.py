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

    # لو ما وصلناش ٥ نصائح، نكمل بنصائح ثابتة
    while len(tips) < 5:
        fallback = {
            "category": "عام",
            "source": "Dummy",
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
