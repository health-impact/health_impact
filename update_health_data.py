import json
import datetime
import os

def update_and_archive():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 1. المعلومات الجديدة اللي بتنزل توا في الموقع
    new_entries = [
        {"title": "مقاومة المضادات", "content": "تنبيه: الاستخدام العشوائي للمضادات الحيوية خطر.", "date": timestamp},
        {"title": "الصحة النفسية", "content": "النوم المنتظم يحسن الأداء الدراسي والمهني.", "date": timestamp},
        {"title": "التغذية", "content": "الخضروات الورقية تعزز المناعة الطبيعية.", "date": timestamp},
        {"title": "النشاط البدني", "content": "الحركة المستمرة تمنع آلام الظهر (Text Neck).", "date": timestamp},
        {"title": "الوقاية", "content": "تعقيم الأسطح يقلل من انتشار بكتيريا Klebsiella.", "date": timestamp}
    ]

    # 2. قراءة البيانات اللي كانت موجودة (بتمشي للأرشيف)
    current_data = []
    if os.path.exists('current_info.json'):
        with open('current_info.json', 'r', encoding='utf-8') as f:
            try:
                current_data = json.load(f)
            except:
                current_data = []

    # 3. تحديث الأرشيف مع جعل "الجديد فوق"
    if current_data:
        archive_data = []
        if os.path.exists('archive_info.json'):
            with open('archive_info.json', 'r', encoding='utf-8') as f:
                try:
                    archive_data = json.load(f)
                except:
                    archive_data = []
        
        # التعديل السحري هنا: نضع الجديد (current_data) + القديم (archive_data)
        # هكي ديما الـ 5 اللي طلعوا توا من الموقع يكونوا هما أول 5 في الأرشيف
        updated_archive = current_data + archive_data

        with open('archive_info.json', 'w', encoding='utf-8') as f:
            json.dump(updated_archive, f, ensure_ascii=False, indent=4)

    # 4. تحديث الملف الحالي
    with open('current_info.json', 'w', encoding='utf-8') as f:
        json.dump(new_entries, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    update_and_archive()
