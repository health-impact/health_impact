import json
import os
import google.generativeai as genai
from datetime import datetime

# إعداد الذكاء الاصطناعي
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

def generate_tip():
    # نطلب منه نصيحة بلهجة بشرية علمية دقيقة
    prompt = "أعطني نصيحة طبية قصيرة أو تحذير صحي بلهجة عربية علمية مبسطة (إنسانية وليست آلية) تتعلق بالميكروبيولوجيا، مقاومة المضادات، أو العادات الصحية. أجب بتنسيق JSON فقط: {'title': '...', 'content': '...', 'type': 'tip/warning'}"
    response = model.generate_content(prompt)
    return json.loads(response.text)

# 1. قراءة البيانات الحالية
with open('athardata.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 2. توليد النصيحة الجديدة
new_tip = generate_tip()
new_tip['date'] = datetime.now().strftime("%Y-%m-%d")

# 3. الإضافة في البداية لضمان عدم التكرار وأنها تطلع في "آخر التحديثات"
data.insert(0, new_tip)

# 4. حفظ الملف
with open('athardata.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
# هذا الجزء يوضع داخل ملف البايثون لضمان جودة النصيحة
prompt = """
أنت خبير في الصحة العامة والميكروبيولوجيا لمنصة 'أثر صحي'.
أعطني نصيحة طبية أو تحذيراً صحياً جديداً ومبتكراً (غير مكرر).
ركز على: (مقاومة المضادات الحيوية، غسل اليدين، جودة النوم، مخاطر الفيب، أو بكتيريا الطعام).
الشروط: 
1. اللهجة: عربية فصحى مبسطة وقريبة للناس (إنسانية).
2. الطول: لا تتجاوز 30 كلمة.
3. التنسيق: JSON فقط كما يلي: 
{"title": "عنوان جذاب", "content": "محتوى النصيحة", "type": "tip أو warning"}
"""
