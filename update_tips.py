import os
import json
import google.generativeai as genai
from datetime import datetime

# 1. إعداد الذكاء الاصطناعي
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

def get_new_tips():
    prompt = """
    أعطني 5 نصائح صحية قصيرة ومفيدة للمجتمع الليبي بناءً على توصيات (WHO, CDC, NCDC).
    يجب أن يكون الرد بتنسيق JSON فقط كقائمة (List)، كل عنصر يحتوي على:
    "title": عنوان النصيحة، "content": شرح مختصر، "type": (إما 'info' أو 'warning')، "source": المصدر.
    تأكد من تنوع المجالات (تغذية، نشاط بدني، نظافة، صحة نفسية).
    """
    response = model.generate_content(prompt)
    # تنظيف النص الناتج ليتحول لـ JSON
    content = response.text.replace('```json', '').replace('```', '').strip()
    return json.loads(content)

def update_file():
    file_path = 'athardata.json'
    
    # تحميل الأرشيف الحالي
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            old_data = json.load(f)
    else:
        old_data = []

    # جلب النصائح الجديدة
    new_tips = get_new_tips()
    today = datetime.now().strftime("%Y-%m-%d")
    
    for tip in new_tips:
        tip['date'] = today
        # إضافة النصيحة في بداية القائمة (لتظهر كأحدث نصيحة)
        if tip['title'] not in [t['title'] for t in old_data]:
            old_data.insert(0, tip)

    # حفظ الملف
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(old_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    update_file()
