import json
import os
import google.generativeai as genai
from datetime import datetime

# إعداد الاتصال بـ Gemini
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"❌ خطأ في الإعداد: {e}")

def generate_health_tips():
    # برومبت مخصص للصحة العامة والميكروبيولوجيا في ليبيا
    prompt = """
    أنت أخصائي صحة عامة وميكروبيولوجي.
    أريد 5 نصائح طبية توعوية جديدة (تخص البكتيريا، الفيروسات، الوقاية، أو الصحة العامة في المجتمع الليبي).
    الرد يجب أن يكون بصيغة JSON فقط كقائمة مصفوفة (Array) بهذا التنسيق:
    [
      {"title": "عنوان النصيحة", "content": "المحتوى العلمي", "type": "tip", "source": "أثر صحي"}
    ]
    تأكد من عدم وجود أي نص خارج الأقواس.
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
    print("🤖 جاري توليد نصائح جديدة...")
    
    # 1. جلب البيانات القديمة (الأرشيف)
    archive = []
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                archive = json.load(f)
            except json.JSONDecodeError:
                archive = []

    # 2. توليد البيانات الجديدة
    new_tips = generate_health_tips()
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    for tip in new_tips:
        tip['date'] = current_date

    # 3. دمج الجديد في أعلى القائمة (لكي يظهر في الواجهة وينزل القديم للأرشيف)
    updated_data = new_tips + archive

    # 4. حفظ الملف بالكامل
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(updated_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ نجاح! تمت إضافة {len(new_tips)} نصائح. إجمالي النصائح في الأرشيف: {len(updated_data)}")

except Exception as e:
    print(f"❌ حدث خطأ: {e}")
