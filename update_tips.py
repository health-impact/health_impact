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
