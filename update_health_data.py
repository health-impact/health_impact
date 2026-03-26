import json
import datetime

def update_and_archive():
    # 1. قائمة بـ 5 معلومات طبية (توا نغيروها لـ API من WHO و NCDC لاحقاً)
    new_entries = [
        {"title": "نصيحة 1", "content": "شرب الماء بانتظام يحسن وظائف الكلى.", "source": "WHO"},
        {"title": "نصيحة 2", "content": "النوم الكافي (7-8 ساعات) ضروري للصحة العقلية.", "source": "NCDC"},
        {"title": "نصيحة 3", "content": "التقليل من السكر يحمي من خطر السكري.", "source": "WHO"},
        {"title": "نصيحة 4", "content": "النشاط البدني اليومي يقوي عضلة القلب.", "source": "Health Research"},
        {"title": "نصيحة 5", "content": "غسل اليدين هو خط الدفاع الأول ضد الأوبئة.", "source": "NCDC"}
    ]
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # 2. قراءة المعلومات الحالية (قبل ما نمسحوها)
    try:
        with open('current_info.json', 'r', encoding='utf-8') as f:
            old_data = json.load(f)
    except:
        old_data = []

    # 3. الأرشفة: لو فيه بيانات قديمة، انقلها لملف الأرشيف وزيد عليها
    if old_data:
        try:
            with open('archive_info.json', 'r', encoding='utf-8') as f:
                archive = json.load(f)
        except:
            archive = []
        
        # إضافة البيانات القديمة للأرشيف (كقائمة)
        if isinstance(old_data, list):
            archive.extend(old_data)
        else:
            archive.append(old_data)

        with open('archive_info.json', 'w', encoding='utf-8') as f:
            json.dump(archive, f, ensure_ascii=False, indent=4)

    # 4. تحديث ملف المعلومات الحالي بـ 5 معلومات جديدة
    # إضافة الوقت لكل معلومة
    for entry in new_entries:
        entry["updated_at"] = timestamp

    with open('current_info.json', 'w', encoding='utf-8') as f:
        json.dump(new_entries, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    update_and_archive()
