import json
import os
import google.generativeai as genai
from datetime import datetime

# إعداد Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_health_tips(count=5):
    prompt = "أعطني قائمة 5 نصائح طبية متنوعة لمنصة 'أثر صحي' في ليبيا بتنسيق JSON فقط (Array)."
    response = model.generate_content(prompt)
    clean_json = response.text.strip()
    if clean_json.startswith('```json'):
        clean_json = clean_json[7:-3].strip()
    elif clean_json.startswith('```'):
        clean_json = clean_json[3:-3].strip()
    return json.loads(clean_json)

# المسار
file_path = 'athardata.json'

try:
    print("🤖 جاري توليد النصائح...")
    new_tips = generate_health_tips(5)
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    for tip in new_tips:
        tip['date'] = current_date

    # كتابة الملف مع التأكد من المسار
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(new_tips, f, ensure_ascii=False, indent=2)
    
    print(f"✅ تم كتابة {len(new_tips)} نصيحة في الملف بنجاح!")

except Exception as e:
    print(f"❌ حدث خطأ: {e}")
