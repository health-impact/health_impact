import json
import os
import google.generativeai as genai
from datetime import datetime
import time

# إعداد الذكاء الاصطناعي
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_health_tips(count=5):
    # طلب 5 نصائح مختلفة في برومبت واحد لضمان التنوع
    prompt = f"""
    أنت خبير في الصحة العامة والميكروبيولوجيا لمنصة 'أثر صحي'.
    أعطني قائمة مكونة من {count} نصائح طبية أو تحذيرات صحية مختلفة تماماً عن بعضها.
    المواضيع: (مقاومة المضادات، الفيب، بكتيريا الغذاء، جودة النوم، غسل اليدين).
    الشروط: 
    1. اللهجة: عربية فصحى مبسطة.
    2. التنسيق: JSON فقط عبارة عن Array (قائمة) كالتالي:
    [
      {{"title": "عنوان 1", "content": "نصيحة 1", "type": "tip", "source": "WHO"}},
      {{"title": "عنوان 2", "content": "نصيحة 2", "type": "warning", "source": "NCDC"}}
    ]
    """
    response = model.generate_content(prompt)
    clean_json = response.text.replace('```json', '').replace('```', '').strip()
    return json.loads(clean_json)

file_path = 'athardata.json'

# إنشاء الملف لو مش موجود
if not os.path.exists(file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump([], f)

try:
    # جلب 5 نصائح جديدة
    new_tips = generate_health_tips(5)
    current_date = datetime.now().strftime("%Y-%m-%d")

    # قراءة الملف الحالي
    with open(file_path, 'r', encoding='utf-8') as f:
        all_tips = json.load(f)

    # إضافة التاريخ لكل نصيحة جديدة ووضعها في بداية القائمة
    for tip in reversed(new_tips): # نعكسهم باش نحافظوا على الترتيب الزمني
        tip['date'] = current_date
        all_tips.insert(0, tip)

    # حفظ الملف (نخزنوا كل شيء، والموقع حيعرض أول 5 بس والأرشيف فيه الباقي)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(all_tips, f, ensure_ascii=False, indent=2)
    
    print(f"تم إضافة {len(new_tips)} نصائح جديدة بنجاح!")

except Exception as e:
    print(f"حدث خطأ: {e}")
