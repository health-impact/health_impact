import json
import os
import google.generativeai as genai
from datetime import datetime
import random

# إعداد Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_health_tips():
    # نطلب نصائح بمحتوى ميكروبيولوجي ليبي لضمان التغيير
    prompt = f"أعطني 5 نصائح طبية لمجال الصحة العامة في ليبيا. كود التغيير: {random.randint(100, 999)}. الرد JSON Array فقط."
    response = model.generate_content(prompt)
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

    # 2. محاولة قراءة القديم
    archive = []
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                archive = json.load(f)
        except:
            archive = []

    # 3. الدمج (الجديد فوق)
    full_data = new_tips + archive
    
    # 4. حفظ نهائي مع مسح الملف القديم تماماً (Force Write)
    if os.path.exists(file_path):
        os.remove(file_path)
        
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ تم حفظ {len(full_data)} نصيحة بنجاح.")

except Exception as e:
    print(f"❌ خطأ: {e}")
