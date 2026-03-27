import json
import os
import google.generativeai as genai
from datetime import datetime

# 1. إعداد Gemini
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Error connecting to Gemini: {e}")

def generate_health_tips(count=5):
    prompt = f"""
    أنت خبير في الصحة العامة والميكروبيولوجيا لمنصة 'أثر صحي' في ليبيا.
    أعطني قائمة مكونة من {count} نصائح طبية متنوعة (بكتيريا، فيروسات، صحة عامة).
    التنسيق: JSON فقط عبارة عن Array (قائمة) كالتالي:
    [
      {{"title": "عنوان", "content": "نصيحة", "type": "tip", "source": "WHO"}}
    ]
    """
    response = model.generate_content(prompt)
    clean_json = response.text.strip()
    if clean_json.startswith('```json'):
        clean_json = clean_json[7:-3].strip()
    elif clean_json.startswith('```'):
        clean_json = clean_json[3:-3].strip()
    return json.loads(clean_json)

file_path = 'athardata.json'

try:
    # 2. توليد النصائح
    print("🤖 جاري توليد نصائح جديدة...")
    new_tips = generate_health_tips(5)
    current_date = datetime.now().strftime("%Y-%m-%d")

    # 3. معالجة البيانات (تصفير الملف القديم لو كان فيه نص ترحيبي فقط)
    all_tips = []
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                all_tips = json.load(f)
                # لو الملف فيه عنصر واحد فقط (الترحيب)، بنمسحه
                if len(all_tips) <= 1:
                    all_tips = []
            except:
                all_tips = []

    # 4. إضافة النصائح الجديدة
    for tip in reversed(new_tips):
        tip['date'] = current_date
        all_tips.insert(0, tip)

    # 5. الحفظ النهائي
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(all_tips, f, ensure_ascii=False, indent=2)
    
    print(f"✅ نجاح! تم تحديث {len(all_tips)} نصيحة.")

except Exception as e:
    print(f"❌ خطأ: {e}")
