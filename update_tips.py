import json
import os
from google import genai
from datetime import datetime
import random

# إعداد العميل
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def get_available_model():
    print("🔍 جاري البحث عن الموديلات المتاحة في حسابك...")
    try:
        # استخراج قائمة الموديلات المتاحة لحسابك
        models = client.models.list()
        model_names = [m.name for m in models]
        print(f"📋 الموديلات المتاحة لك هي: {model_names}")
        
        # الترتيب المفضل للموديلات
        preferences = ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']
        for pref in preferences:
            if pref in model_names:
                print(f"✅ سيتم استخدام الموديل: {pref}")
                return pref
        
        # لو لم يجد المفضل، يأخذ أول موديل يدعم التوليد
        return model_names[0] if model_names else None
    except Exception as e:
        print(f"❌ فشل جلب القائمة: {e}")
        return 'gemini-1.5-flash' # محاولة أخيرة افتراضية

def generate_health_tips(model_name):
    prompt = "أعطني 5 نصائح طبية قصيرة لمجال الميكروبيولوجيا في ليبيا بتنسيق JSON Array فقط."
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        text = response.text.strip()
        if text.startswith('
http://googleusercontent.com/immersive_entry_chip/0
http://googleusercontent.com/immersive_entry_chip/1

---

### 🚀 شن حنديروا توة؟
1. حدث ملف `update_tips.py` بالكود "الذكي" أعلاه.
2. دير **Run workflow**.
3. افتح الـ **Logs** وشوف السطر اللي مكتوب فيه: **"📋 الموديلات المتاحة لك هي:"**.

**لو طلعت القائمة "فاضية" []، معناها المشكلة 100% في الـ API Key نفسه (ممكن محتاج تفعيل Billing في Google Cloud حتى لو النسخة مجانية، أو المفتاح expired).**

**جرب يا دكتور وانسخ لي قائمة الموديلات اللي حتطلعلك في الشاشة السوداء، هادي هي "كلمة السر" اللي حتحل اللغز!** 🔬🌿🚀

هل فكرت في تجربة مفتاح من حساب Gmail آخر للتأكد من أن المشكلة ليست في إعدادات الحساب الحالي؟
