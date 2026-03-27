import json
import os
import google.generativeai as genai
from datetime import datetime
import time

# إعداد Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_health_tips():
    prompt = "أعطني قائمة 5 نصائح طبية متنوعة لمنصة 'أثر صحي' في ليبيا بتنسيق JSON فقط."
    response = model.generate_content(prompt)
    clean_json = response.text.strip()
    if clean_json.startswith('```json'):
        clean_json = clean_json[7:-3].strip()
    elif clean_json.startswith('```'):
        clean_json = clean_json[3:-3].strip()
    return json.loads(clean_json)

file_path = 'athardata.json'

try:
    # 1. قراءة الأرشيف القديم
    archive = []
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                archive = json.load(f)
            except:
                archive = []

    # 2. توليد الجديد
    new_tips = generate_health_tips()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for tip in new_tips:
        tip['date'] = current_time # إضافة الوقت بالدقيقة والثانية لضمان التغيير

    # 3. الدمج
    updated_data = new_tips + archive

    # 4. الكتابة القسرية
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(updated_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ تم التحديث في وقت: {current_time}")

except Exception as e:
    print(f"❌ خطأ: {e}")
