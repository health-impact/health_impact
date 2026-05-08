import os
import re
import json
from datetime import datetime
from google import genai

API_KEY = os.environ["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

# الأقسام الـ 11 المعتمدة مع الكلمات المفتاحية للتصنيف التلقائي
CATEGORIES = {
    "مكافحة العدوى": ["مكافحة العدوى", "العدوى", "تعقيم", "الجراثيم", "الميكروبات", "الفيروس", "البكتيريا", "التطهير"],
    "صحة الأم والطفل": ["الأم", "الطفل", "الرضاعة", "الحمل", "الولادة", "الرضيع", "اليونيسف", "UNICEF"],
    "الصحة المدرسية": ["مدرسية", "مدرسة", "الطلاب", "المدارس", "الأطفال في المدرسة"],
    "سلامة الغذاء": ["سلامة الغذاء", "الأطعمة", "التسمم الغذائي", "الغذاء المحفوظ", "تاريخ الصلاحية"],
    "الأمراض المزمنة": ["أمراض مزمنة", "السكري", "ضغط الدم", "أمراض القلب", "السمنة", "السرطان"],
    "الصحة البيئية": ["بيئية", "البيئة", "تلوث الهواء", "مياه الشرب", "النفايات", "الصرف الصحي"],
    "الصحة النفسية": ["نفسية", "نفسي", "القلق", "الاكتئاب", "الضغط النفسي", "السلوكية", "الصحة النفسية"],
    "التغذية": ["التغذية", "تغذية", "الفيتامينات", "البروتين", "الكالسيوم", "النظام الغذائي"],
    "النشاط البدني": ["نشاط بدني", "رياضة", "التمارين", "المشي", "ممارسة الرياضة"],
    "التوعية الدوائية": ["دواء", "أدوية", "التوعية الدوائية", "المضادات الحيوية", "الجرعة", "الوصفة الطبية"],
    "إدارة الطوارئ": ["طوارئ", "إسعاف", "الإسعافات الأولية", "الحوادث", "الكوارث", "الإنعاش"],
}

PROMPT_TEMPLATE = """
اعطيني نصيحة صحية جديدة... 
وضيف خانة اسمها notif_text فيها جملة مشوقة للإشعار.

أعطني 5 نصائح ومعلومات وارشادات صحية قصيرة ومفيدة كأنك خبير في جميع مجالات الصحة العامة.

**مهم جداً**: يجب أن تغطي النصائح الخمس هذه الأقسام تحديداً (قسم واحد على الأقل لكل نصيحة):
{required_categories}

لا تتجاوز هذه الأقسام المطلوبة. لا تكتب عن صحة الأم والطفل أو مكافحة العدوى فقط.

وزّع الكروت الخمسة كالتالي من حيث الشكل:
- 2 كروت: نصائح طبية مباشرة
- 1 كرت: فقرة 'صح أو خطأ' لتصحيح مفهوم شائع
- 1 كرت: 'تحدي اليوم' (Daily Challenge) يطلب من القارئ فعل شيء صحي بسيط
- 1 كرت: معلومة 'هل كنت تعلم؟' علمية ومختصرة

يجب أن يكون الرد بتنسيق JSON فقط كقائمة (List)، كل عنصر يحتوي على:
"title": عنوان النصيحة،
"content": شرح مختصر،
"type": (إما 'info' أو 'warning')،
"source": المصدر (من WHO, CDC, NCDC, UNICEF حسب الموضوع)،
"category": اسم القسم الذي تنتمي إليه النصيحة (من الأقسام المحددة أعلاه فقط).

للمجتمع الليبي. تجنب التكرار.
"""

def classify_tip(tip: dict) -> str:
    """Classify a tip into one of the 11 categories based on its content."""
    text = (tip.get("title", "") + " " + tip.get("content", "") + " " + tip.get("source", "")).lower()
    for cat, keywords in CATEGORIES.items():
        if any(kw.lower() in text for kw in keywords):
            return cat
    return "عام"

def get_category_counts(data: list) -> dict:
    """Count how many tips exist per category."""
    counts = {cat: 0 for cat in CATEGORIES}
    for item in data:
        if not isinstance(item, dict):
            continue
        cat = item.get("category") or classify_tip(item)
        if cat in counts:
            counts[cat] += 1
    return counts

def choose_required_categories(counts: dict, n: int = 5) -> list:
    """Select the n least-represented categories to focus on next."""
    sorted_cats = sorted(counts.items(), key=lambda x: x[1])
    return [cat for cat, _ in sorted_cats[:n]]

def get_previous_tips(file_path, limit=30):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [item['title'] for item in data[:limit] if isinstance(item, dict) and 'title' in item]
    except:
        return []

def _extract_json_array(text: str):
    cleaned = text.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(cleaned)
    except Exception:
        pass
    m = re.search(r"\[[\s\S]*\]", cleaned)
    if not m:
        raise ValueError(f"Response did not contain a JSON array:\n{cleaned}")
    return json.loads(m.group(0))

def list_available_models():
    print("Listing available models:")
    try:
        for m in client.models.list():
            name = getattr(m, "name", None) or str(m)
            print("MODEL:", name)
    except Exception as e:
        print("Failed to list models:", e)

def get_new_tips(existing_titles=None, required_categories=None):
    # بناء قسم الأقسام المطلوبة
    if required_categories:
        cats_formatted = "\n".join(f"- {cat}" for cat in required_categories)
    else:
        cats_formatted = "\n".join(f"- {cat}" for cat in CATEGORIES)

    prompt = PROMPT_TEMPLATE.format(required_categories=cats_formatted)

    # بناء قسم النصائح السابقة لتجنب التكرار
    if existing_titles:
        titles_list = "\n".join(f"- {t}" for t in existing_titles[:30])
        prompt += f"\n\nتجنب تمامًا توليد أي نصيحة مشابهة للنصائح التالية الموجودة مسبقًا:\n{titles_list}\n"


    candidates = [
    "models/gemini-2.5-flash",
    "models/gemini-2.0-flash",
    "models/gemini-flash-latest",
    "models/gemini-2.5-pro",
    "models/gemini-pro-latest",
]

    last_err = None
    for model_name in candidates:
        try:
            resp = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            text = getattr(resp, "text", None) or str(resp)
            tips = _extract_json_array(text)
            if not isinstance(tips, list):
                raise ValueError("Expected a JSON list.")
            return tips
        except Exception as e:
            last_err = e

    print("No candidate model worked. Will print available models now.")
    list_available_models()
    raise RuntimeError(f"All model attempts failed. Last error: {last_err}")

def update_file():
    file_path = "athardata.json"

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            old_data = json.load(f)
    else:
        old_data = []

    existing_titles = [t.get("title", "") for t in old_data if isinstance(t, dict)]
    existing_titles_set = set(existing_titles)
    existing_contents = {t.get("content", "").strip() for t in old_data if isinstance(t, dict)}

    # حساب توزيع الأقسام الحالي واختيار الأقسام الأقل تمثيلاً
    category_counts = get_category_counts(old_data)
    required_categories = choose_required_categories(category_counts, n=5)
    print(f"توزيع الأقسام الحالي: {category_counts}")
    print(f"الأقسام المطلوبة لهذه الدورة: {required_categories}")

    new_tips = get_new_tips(existing_titles=existing_titles, required_categories=required_categories)
    today = datetime.now().strftime("%Y-%m-%d")

    added = 0

    for tip in new_tips:
        if not isinstance(tip, dict):
            continue
        tip["date"] = today
        # إضافة حقل التصنيف إذا لم يوجد
        if not tip.get("category"):
            tip["category"] = classify_tip(tip)
        title = tip.get("title", "").strip()
        content = tip.get("content", "").strip()
        if not title:
            continue
        if title in existing_titles_set:
            print(f"Skipped duplicate title: {title}")
            continue
        if content and content in existing_contents:
            print(f"Skipped duplicate content for: {title}")
            continue
        old_data.insert(0, tip)
        existing_titles_set.add(title)
        existing_contents.add(content)
        added += 1

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(old_data, f, ensure_ascii=False, indent=2)

    print(f"Added {added} new tips for {today}")

if __name__ == "__main__":
    update_file()
