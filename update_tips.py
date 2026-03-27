import json
import os
import google.generativeai as genai
from datetime import datetime

# إعداد الذكاء الاصطناعي باستخدام المفتاح السري
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_health_tip():
    prompt = """
    أنت خبير صحة عامة وميكروبيولوجيا لمنصة 'أثر صحي' في ليبيا.
    أعطني نصيحة طبية أو تحذيراً صحياً (جديد وغير مكرر).
    المواضيع: (بكتيريا الطعام، مقاومة المضادات، الفيب، نظافة المختبرات، أو عادات يومية).
    الشروط:
    1. اللهجة: عربية فصيحة مبسطة (إنسانية وليست آلية).
    2. التنسيق: JSON فقط كالتالي:
    {"title": "عنوان جذاب", "content": "محتوى مختصر ومفيد", "type": "tip أو warning", "source": "المصدر العلمي (WHO/NCDC/FDA)"}
    """
    response = model.generate_content(prompt)
    # تنظيف الاستجابة من أي علامات Markdown إذا وجدت
    clean_json = response.text.replace('```json', '').replace('```', '').strip()
    return json.loads(clean_json)

# تنفيذ التحديث
file_path = 'athardata.json'

# جلب النصيحة الجديدة
try:
    new_data = generate_health_tip()
    new_data['date'] = datetime.now().strftime("%Y-%m-%d")

    # قراءة الملف الحالي
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            all_tips = json.load(f)
    else:
        all_tips = []

    # إضافة النصيحة في البداية (index 0) لضمان ظهورها كأحدث تحديث
    all_tips.insert(0, new_data)

    # حفظ الملف المعدل
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(all_tips, f, ensure_ascii=False, indent=2)
    
    print("تم إضافة النصيحة بنجاح!")
except Exception as e:
    print(f"حدث خطأ: {e}")
