import os
import re
import json
from datetime import datetime
from google import genai

API_KEY = os.environ["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

PROMPT = """
أعطني 5 نصائح ومعلومات وارشادات صحية قصيرة ومفيدة في جميع مجالات الصحة العامة أريدك أن تنوع في محتوى الكروت اليومية (5 كروت). لا تجعلها كلها نصائح مباشرة، بل وزعها كالتالي:

2 كروت: نصائح طبية مباشرة  (في جميع اقسام الصحة العامة الي مختارينهم).

1 كرت: فقرة 'صح أو خطأ' لتصحيح المفاهيم الشائعة (في جميع اقسام الصحة العامة الي مختارينهم).

1 كرت: 'تحدي اليوم' (Daily Challenge) يطلب من القارئ فعل شيء صحي بسيط.

1 كرت: معلومة 'هل كنت تعلم في جمسع اقسام الصحة العامةالي مختارينهم؟' علمية ومختصرة. للمجتمع الليبي بناءً على توصيات (WHO, CDC, NCDC, UNICEF,).
يجب أن يكون الرد بتنسيق JSON فقط كقائمة (List)، كل عنصر يحتوي على:
"title": عنوان النصيحة، "content": شرح مختصر، "type": (إما 'info' أو 'warning')، "source": المصدر.
تأكد من تنوع المجالات (تأكد من تنوع المجالات (تغذية، صحة بيئية، سلامة الغذاء، الصحة المهنية، صحة الأم و والطفل، الصحة السلوكية، التوعية الدوائية، الأمراض المزمنة، علم الأوبئة، الصحة المدرسية.  ادارة الطوارئ، الرقابة الصحية، مكافحة العدوى، نشاط بدني، نظافة، صحة نفسية).).
"عند توليد كل نصيحة، يجب أن تلتزم بذكر المصدر ونوع المعلومة يعني في اي قسم ف الصحة العامة الي اخترناهم نكل نصيحة تكون ف جانب  من جوانب الصحة العامة العشرة الي اخترناهم مع الحرص على عدم تكرار الصائح والتقليل من نصائح النشاط البدني 
"""

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
