import json
import os
import google.generativeai as genai
from datetime import datetime

try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Error: {e}")

def generate_health_tips(count=5):
    prompt = f"أعطني قائمة {count} نصائح طبية متنوعة لمنصة 'أثر صحي' في ليبيا بتنسيق JSON فقط."
    response = model.generate_content(prompt)
    clean_json = response.text.strip()
    if clean_json.startswith('```json'):
        clean_json = clean_json[7:-3].strip()
    elif clean_json.startswith('```'):
        clean_json = clean_json[3:-3].strip()
    return json.loads(clean_json)

file_path = 'athardata.json'
try:
    new_tips = generate_health_tips(5)
    current_date = datetime.now().strftime("%Y-%m-%d")
    for tip in new_tips:
        tip['date'] = current_date
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(new_tips, f, ensure_ascii=False, indent=2)
    print("✅ Success")
except Exception as e:
    print(f"❌ Error: {e}")
