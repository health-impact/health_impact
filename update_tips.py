import json
import os
from google import genai
from datetime import datetime
import random

# إعداد العميل (المكتبة الجديدة 2026)
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def generate_health_tips():
    # طلب نصائح طبية تهم المجتمع الليبي
    prompt = (
        f"أعطني 5 نصائح طبية قصيرة ومفيدة جداً (باللغة العربية) لمنصة 'أثر صحي'. "
        f"ركز على الصحة العامة والميكروبيولوجيا. كود التغيير: {random.randint(100, 999)}. "
        f"يجب أن يكون الرد بتنسيق JSON Array فقط، كل عنصر يحتوي على 'title' و 'content'."
    )
    
    try:
        # استخدام الموديل المستقر (Stable)
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt
        )
        
        text = response.text.strip()
        # تنظيف الرد من أي زوائد
        if text.startswith('```json'):
            text = text[7:-3].strip()
        elif text.startswith('```'):
            text = text[3:-3].strip()
        
        return json.loads(text)
    except Exception as e:
        print(f"❌ خطأ أثناء توليد النصائح: {e}")
        return None

file_path = 'athardata.json'

def main():
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
        except: archive = []

    # دمج النصائح الجديدة مع الأرشيف
    full_data = new_tips + archive
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ تم تحديث {len(new_tips)} نصائح طبية بنجاح.")

if __name__ == "__main__":
    main()
