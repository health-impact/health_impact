import json
import os
from google import genai
from datetime import datetime
import random

# إعداد العميل باستخدام المكتبة الجديدة والموديل الصحيح
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def generate_health_tips():
    prompt = f"أعطني 5 نصائح طبية لمجال الصحة العامة في ليبيا. كود التغيير: {random.randint(100, 999)}. الرد JSON Array فقط."
    
    try:
        # استخدام موديل 1.5 فلاش بالتنسيق الجديد
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt
        )
        
        text = response.text.strip()
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
    print("🚀 بدء تشغيل البوت المطور...")
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
    
    print(f"✅ تم حفظ {len(full_data)} نصيحة بنجاح.")

if __name__ == "__main__":
    main()
