import json
import os
import google.generativeai as genai
from datetime import datetime

# إعداد مفتاح الـ API
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def generate_health_tips():
    model = genai.GenerativeModel('gemini-pro')
    
    # أمر مخصص بدقة للصحة العامة في ليبيا ويتطابق مع كود HTML الخاص بك
    prompt = """
    أعطني 5 نصائح توعوية دقيقة في مجال الصحة العامة (Public Health) تناسب المجتمع في ليبيا (مثل جودة المياه، الأمراض الموسمية، أنماط الحياة).
    يجب أن يكون الرد بتنسيق JSON Array فقط.
    كل عنصر يجب أن يحتوي على المفاتيح التالية حصراً:
    - "title": عنوان النصيحة.
    - "content": تفاصيل النصيحة (سطرين كحد أقصى).
    - "type": إما "tip" (لنصيحة عادية) أو "warning" (لتحذير صحي مهم).
    - "source": اكتب منظمة حقيقية مثل "WHO" أو "NCDC" أو "أثر صحي".
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # تنظيف النص لضمان كونه JSON صالح
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
            
        return json.loads(text)
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return None

def main():
    new_tips = generate_health_tips()
    if not new_tips:
        print("⚠️ فشل التوليد، لن يتم تحديث الملف.")
        return

    file_path = 'athardata.json'
    
    # تنسيق التاريخ ليتناسب مع الواجهة
    timestamp = datetime.now().strftime("%Y-%m-%d | %H:%M")
    for tip in new_tips:
        tip['date'] = timestamp

    # نظام الأرشفة (قراءة القديم وإضافة الجديد في البداية)
    archive = []
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                archive = json.load(f)
        except:
            archive = []

    # دمج النصائح (الـ 5 الجديدة ستكون في الأعلى دائماً)
    full_data = new_tips + archive
    
    # حفظ الملف
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)
    
    print("✅ تم إضافة 5 نصائح جديدة وأرشفة القديمة بنجاح!")

if __name__ == "__main__":
    main()
