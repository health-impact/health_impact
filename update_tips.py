import json
import os
import google.generativeai as genai
from datetime import datetime
import random

# إعداد Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_health_tips():
    # طلبنا من الذكاء الاصطناعي تنويع النصائح لضمان التغيير
    prompt = f"أعطني 5 نصائح طبية لمجال الميكروبيولوجيا والصحة في ليبيا. رقم المجموعة العشوائي: {random.randint(1, 1000)}. التنسيق JSON Array فقط."
    response = model.generate_content(prompt)
    clean_json = response.text.strip()
    if clean_json.startswith('```json'):
        clean_json = clean_json[7:-3].strip()
    elif clean_json.startswith('```'):
        clean_json = clean_json[3:-3].strip()
    return json.loads(clean_json)

file_path = 'athardata.json'

try:
    # 1. قراءة القديم
    archive = []
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                archive = json.load(f)
            except:
                archive = []

    # 2. توليد الجديد مع بصمة زمنية دقيقة جداً
    new_tips = generate_health_tips()
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    
    for tip in new_tips:
        tip['date'] = timestamp
        # إضافة معرف فريد لكل نصيحة لكسر حالة "Everything up-to-date"
        tip['id'] = f"tip-{now.timestamp()}-{random.randint(100, 999)}"

    # 3. الدمج (الجديد في البداية)
    updated_data = new_tips + archive

    # 4. الكتابة القسرية مع ترتيب عشوائي طفيف لضمان اختلاف الملف
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(updated_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ تم تحديث {len(new_tips)} نصيحة في وقت: {timestamp}")

except Exception as e:
    print(f"❌ خطأ: {e}")
