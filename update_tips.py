import json
import os
from google import genai
from google.genai import types
from datetime import datetime
import random

# إعداد العميل مع تحديد الإصدار المستقر v1
client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"],
    http_options={'api_version': 'v1'} # إجبار النظام على v1 بدل v1beta
)

def generate_health_tips():
    prompt = (
        "أعطني 5 نصائح طبية قصيرة جداً ومفيدة للمجتمع الليبي (باللغة العربية). "
        "ركز على الصحة العامة والميكروبيولوجيا. "
        "يجب أن يكون الرد بتنسيق JSON Array فقط، كل عنصر يحتوي على 'title' و 'content'."
    )
    
    try:
        # تجربة موديل Pro كبديل لـ Flash لكسر عقدة الـ 404
        response = client.models.generate_content(
            model='gemini-1.5-pro', 
            contents=prompt
        )
        
        text = response.text.strip()
        if text.startswith('```json'):
            text = text[7:-3].strip()
        elif text.startswith('```'):
            text = text[3:-3].strip()
        
        return json.loads(text)
    except Exception as e:
        print(f"❌ خطأ في Gemini: {e}")
        return None

file_path = 'athardata.json'

def main():
    print("🚀 محاولة التوليد باستخدام Gemini 1.5 Pro (v1 stable)...")
    new_tips = generate_health_tips()
    
    if not new_tips:
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for tip in new_tips:
        tip['date'] = timestamp
        tip['id'] = f"tip-{random.randint(1000, 9999)}"

    archive = []
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                archive = json.load(f)
        except:
            archive = []

    full_data = new_tips + archive
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ تم التحديث بنجاح! الإجمالي: {len(full_data)}")

if __name__ == "__main__":
    main()
