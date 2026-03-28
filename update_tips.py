import json
import os
import random
from datetime import datetime
from google import genai

# إعداد العميل
api_key = os.environ.get("GEMINI_API_KEY")

def main():
    file_path = 'athardata.json'
    timestamp = datetime.now().strftime("%Y-%m-%d | %H:%M")
    
    # نصائح احتياطية في حال فشل الـ AI
    new_tips = [
        {"title": "غسل اليدين", "content": "اغسل يديك بانتظام للوقاية من العدوى.", "type": "وقاية", "source": "أثر صحي"},
        {"title": "شرب الماء", "content": "تأكد من شرب مياه نظيفة ومعقمة.", "type": "بيئة", "source": "أثر صحي"}
    ]

    try:
        if api_key:
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents="أعطني 3 نصائح طبية قصيرة جداً للمجتمع الليبي بتنسيق JSON array فقط."
            )
            text = response.text.strip()
            if "
http://googleusercontent.com/immersive_entry_chip/0
http://googleusercontent.com/immersive_entry_chip/1

---

#### الخطوة 2: تأكد من الـ Secrets في GitHub
بما إن البرنامج يفشل في استخدام الـ AI، تأكد من الآتي:
1. اذهب لـ **Settings** > **Secrets and variables** > **Actions**.
2. هل يوجد سر اسمه **Exactly** `GEMINI_API_KEY`؟ (تأكد من الحروف الكبيرة).
3. هل القيمة (Value) هي المفتاح اللي يبدأ بـ `AIza...`؟

---

#### الخطوة 3: تشغيل الـ Action
بعد حفظ الكود الجديد في `update_tips.py` وتعديل الـ Secrets إذا لزم الأمر، شغل الـ **Action** مرة تانية.

**ليش المرة هادي حتنجح؟**
لأن الكود الجديد "مُجبر" يصنع الملف حتى لو الـ AI ما ردش عليه (حيصنعه بنصائح احتياطية)، وهكي الـ GitHub Actions حيلقى ملف يرفعه للمستودع وتطلع العلامة الخضراء ومعاها تحديث للملف.



**هيا يا دكتور، جرب الكود "المبسط" هذا وشغل الـ Action، وحتلقى ملف `athardata.json` رجع يظهر في المستودع فوراً!** 🚀🔬🌿
