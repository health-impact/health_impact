import json
import os
import google.generativeai as genai
from datetime import datetime

# 1. إعداد الذكاء الاصطناعي
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("✅ تم الاتصال بمفتاح Gemini بنجاح.")
except Exception as e:
    print(f"❌ خطأ في إعداد Gemini: {e}")

def generate_health_tips(count=5):
    prompt = f"""
    أنت خبير في الصحة العامة والميكروبيولوجيا لمنصة 'أثر صحي' في ليبيا.
    أعطني قائمة مكونة من {count} نصائح طبية أو تحذيرات صحية متنوعة (بكتيريا، فيروسات، صحة عامة).
    التنسيق: JSON فقط عبارة عن Array (قائمة) كالتالي:
    [
      {{"title": "عنوان", "content": "نصيحة", "type": "tip", "source": "WHO"}}
    ]
    """
    response = model.generate_content(prompt)
    # تنظيف النص من أي علامات markdown
    clean_json = response.text.strip()
    if clean_json.startswith('```json'):
        clean_json = clean_json[7:-3].strip()
    elif clean_json.startswith('```'):
        clean_json = clean_json[3:-3].strip()
    
    return json.loads(clean_json)

# المسار الحقيقي للملف في بيئة GitHub Actions
file_path = os.path.join(os.getcwd(), 'athardata.json')
print(f"📂 مسار الملف المستخدم: {file_path}")

try:
    # 2. جلب النصائح
    print("🤖 جاري توليد النصائح من Gemini...")
    new_tips = generate_health_tips(5)
    current_date = datetime.now().strftime("%Y-%m-%d")
    print(f"✨ تم توليد {len(new_tips)} نصائح بنجاح.")

    # 3. معالجة الملف
    all_tips = []
    if os.path.exists(file_path):
        print("📖 ملف athardata.json موجود، جاري القراءة...")
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                all_tips = json.load(f)
            except:
                all_tips = []
    else:
        print("⚠️ الملف غير موجود، سيتم إنشاؤه.")

    # 4. دمج البيانات الجديدة في البداية
    for tip in reversed(new_tips):
        tip['date'] = current_date
        all_tips.insert(0, tip)

    # 5. الحفظ الفعلي والقسري
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(all_tips, f, ensure_ascii=False, indent=2)
    
    # تأكيد الحفظ برمجياً
    if os.path.getsize(file_path) > 0:
        print(f"✅ تم حفظ الملف بنجاح. الحجم الحالي: {os.path.getsize(file_path)} بايت.")
    else:
        print("❌ فشل الحفظ: الملف لا يزال فارغاً!")

except Exception as e:
    print(f"💥 حدث خطأ غير متوقع: {e}")
    
