import json
import os
import random
from datetime import datetime
from google import genai

# إعداد الاتصال بموديل Gemini 1.5 Flash الأحدث
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def generate_health_tips():
    """توليد نصائح توعوية طبية مخصصة للمجتمع الليبي"""
    prompt = (
        "أعطني 5 نصائح توعوية طبية قصيرة جداً ومفيدة للمجتمع الليبي في مجال الصحة العامة (Public Health). "
        "ركز على الوقاية من الأمراض، جودة المياه، التوعية البيئية، وسلامة الغذاء. "
        "يجب أن يكون الرد بتنسيق JSON Array فقط، وكل عنصر يحتوي حصراً على المفاتيح: "
        "'title', 'content', 'type', 'source'."
    )
    
    try:
        # استخدام الموديل الأحدث والمستقر والمجاني
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        
        text = response.text.strip()
        
        # تنظيف النص لضمان تحويله لـ JSON
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
            
        return json.loads(text)
    except Exception as e:
        print(f"❌ خطأ أثناء التوليد: {e}")
        return None

def main():
    print("🚀 جاري تحديث بيانات أثر صحي...")
    
    if not api_key:
        print("❌ خطأ: لم يتم العثور على المفتاح في GitHub Secrets")
        return

    new_tips = generate_health_tips()
    
    if not new_tips:
        return

    file_path = 'athardata.json'
    timestamp = datetime.now().strftime("%Y-%m-%d | %H:%M")
    
    for tip in new_tips:
        tip['date'] = timestamp
        tip['id'] = f"tip-{random.randint(1000, 9999)}"

    # نظام الأرشفة التراكمي (دمج الجديد مع القديم)
    archive = []
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                archive = json.load(f)
        except:
            archive = []

    # دمج النصائح (الجديد في الأعلى)
    full_data = new_tips + archive
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ نجاح! تم تحديث الأرشيف بإجمالي: {len(full_data)} نصيحة")

if __name__ == "__main__":
    main()
