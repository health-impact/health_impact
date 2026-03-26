import json
import datetime

def start_bot():
    # 1. هادي المعلومة الجديدة (توا نغيروها لـ API لاحقاً)
    new_info = {
        "title": "تحديث صحي دوري",
        "content": "الالتزام بغسل اليدين يقلل انتشار البكتيريا بنسبة كبيرة.",
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    # 2. نفتحوا الملف الحالي باش نشوفوا شن فيه
    try:
        with open('current_info.json', 'r', encoding='utf-8') as f:
            old_info = json.load(f)
    except:
        old_info = None

    # 3. لو فيه معلومة قديمة، نبعتوها للأرشيف فوراً
    if old_info:
        try:
            with open('archive_info.json', 'r', encoding='utf-8') as f:
                archive_list = json.load(f)
        except:
            archive_list = []
        
        archive_list.append(old_info)
        with open('archive_info.json', 'w', encoding='utf-8') as f:
            json.dump(archive_list, f, ensure_ascii=False, indent=4)

    # 4. نحطوا المعلومة الجديدة في الملف الأساسي
    with open('current_info.json', 'w', encoding='utf-8') as f:
        json.dump(new_info, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    start_bot()
