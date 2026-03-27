import json
import os
import google.generativeai as genai
from datetime import datetime
import random

# إعداد Gemini
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("✅ تم التأكد من مفتاح API")
except Exception as e:
    print(f"❌ خطأ في مفتاح API: {e}")

def generate_health_tips():
    prompt = f"أعطني 5 نصائح طبية لمجال الميكروبيولوجيا والصحة في ليبيا. رقم عشوائي: {random.randint(1, 1000)}. التنسيق JSON Array فقط."
    response = model.generate_content(prompt)
    
    # اطبع الرد في الشاشة السوداء للتأكد
    print(f"🤖 رد Gemini هو: {response.text}")
    
    clean_json = response.text.strip()
    if clean_json.startswith('```json'):
        clean_json = clean_json[7:-3].strip()
    elif clean_json.startswith('```'):
        clean_json = clean_json[3:-3].strip()
    return json.loads(clean_json)

file_path = 'athardata.json'

try:
    # 1. جلب الجديد
    new_tips = generate_health_tips()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for tip in new_tips:
        tip['date'] = timestamp
        tip['id'] = f"tip-{random.randint(1000, 9999)}"

    # 2. قراءة القديم (لو وجد)
    archive = []
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                archive = json.load(f)
                print(f"📂 تم تحميل {len(archive)} نصيحة من الأرشيف")
            except:
                archive = []

    # 3. الدمج والحفظ
    full_data = new_tips + archive
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ تم حفظ الملف بنجاح. الإجمالي: {len(full_data)}")

except Exception as e:
    print(f"💥 خطأ قاتل: {e}")
