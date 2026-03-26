import json
import datetime
import os

def update_and_archive():
    # 1. تجهيز الـ 5 معلومات الجديدة (المحتوى اللي تبي تعرضه توا)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    new_entries = [
        {"id": 1, "title": "مقاومة المضادات", "content": "الاستخدام العشوائي للمضادات الحيوية يزيد من قوة البكتيريا.", "date": timestamp},
        {"title": "الصحة النفسية", "content": "النوم المنتظم يقلل من مستويات التوتر والقلق اليومي.", "date": timestamp},
        {"title": "التغذية السليمة", "content": "التقليل من السكريات المصنعة يحسن مستويات الطاقة.", "date": timestamp},
        {"title": "النشاط البدني", "content": "المشي لمدة 30 دقيقة يومياً يقي من أمراض القلب.", "date": timestamp},
        {"title": "النظافة العامة", "content": "تعقيم الأسطح في المختبرات يمنع التلوث الخلطي.", "date": timestamp}
    ]

    # 2. قراءة المعلومات الحالية (التي ستصبح "قديمة" وتذهب للأرشيف)
    current_data = []
    if os.path.exists('current_info.json'):
        with open('current_info.json', 'r', encoding='utf-8') as f:
            try:
                current_data = json.load(f)
            except:
                current_data = []

    # 3. تحديث الأرشيف (إضافة القديم فوق الموجود مسبقاً في الأرشيف)
    if current_data:
        archive_data = []
        if os.path.exists('archive_info.json'):
            with open('archive_info.json', 'r', encoding='utf-8') as f:
                try:
                    archive_data = json.load(f)
                except:
                    archive_data = []
        
        # دمج البيانات القديمة مع الأرشيف
        if isinstance(current_data, list):
            archive_data.extend(current_data)
        else:
            archive_data.append(current_data)

        # حفظ الأرشيف المحدث
        with open('archive_info.json', 'w', encoding='utf-8') as f:
            json.dump(archive_data, f, ensure_ascii=False, indent=4)

    # 4. تحديث ملف المعلومات الحالي بالـ 5 الجديدة (عشان تطلع في الموقع)
    with open('current_info.json', 'w', encoding='utf-8') as f:
        json.dump(new_entries, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    update_and_archive()
