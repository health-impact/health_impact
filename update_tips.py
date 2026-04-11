import os
import re
import json
from datetime import datetime
from google import genai

API_KEY = os.environ["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

PROMPT = "أنت الآن خبير صحة عامة رقمي لمنصة (أثر صحي). مهمتك هي توليد 5 نصائح يومية للمواطن الليبي، بشرط أن يتم اختيار هذه النصائح الخمسة من بين 10 مجالات مختلفة لضمان التنوع وعدم التكرار.

المجالات العشرة هي:

صحة البيئة (المياه، الهواء، النفايات).

سلامة الغذاء (المطاعم، التخزين المنزلي).

مكافحة العدوى (البكتيريا، الأسطح، التعقيم).

الصحة المهنية (سلامة العمال، المكاتب، المختبرات).

صحة الأم والطفل (التوعية، الرضاعة، التطعيمات).

الصحة السلوكية (التدخين، النوم، العادات اليومية).

التوعية الدوائية (المضادات الحيوية، حفظ الأدوية).

الأمراض المزمنة (الوقاية والتعايش مع السكر والضغط).

إدارة الطوارئ (الإسعافات، الأوبئة الموسمية).

الرقابة الصحية (حقوق المستهلك والمعايير الصحية).

المطلوب في كل مرة يشتغل فيها السكربت:

اختر 5 مجالات فقط من العشرة أعلاه (تأكد أنها مختلفة عن آخر مرة).

ولد نصيحة واحدة لكل مجال مختار (الإجمالي 5 نصائح).

اللغة: لهجة ليبية بيضاء محترمة وقريبة من القلب.

المصادر: منظمة الصحة العالمية (WHO) (FDA) (CDC) (NCDC) وغيرها والواقع المحلي الليبي."

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

def get_new_tips():
    # جرّبي كم اسم شائع، ولو فشلوا نطبع المتاح


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
                contents=PROMPT,
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

    new_tips = get_new_tips()
    today = datetime.now().strftime("%Y-%m-%d")

    existing_titles = {t.get("title") for t in old_data if isinstance(t, dict)}
    added = 0

    for tip in new_tips:
        if not isinstance(tip, dict):
            continue
        tip["date"] = today
        title = tip.get("title")
        if title and title not in existing_titles:
            old_data.insert(0, tip)
            existing_titles.add(title)
            added += 1

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(old_data, f, ensure_ascii=False, indent=2)

    print(f"Added {added} new tips for {today}")

if __name__ == "__main__":
    update_file()
