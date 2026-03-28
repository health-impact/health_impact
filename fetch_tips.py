import json
from datetime import datetime

# نصائح تجريبية باش نتأكد إن الموقع يشتغل
tips = [
    {
        "title": "اغسل يديك بانتظام",
        "content": "غسل اليدين يقلل من انتقال العدوى بنسبة كبيرة.",
        "source": "WHO"
    },
    {
        "title": "قلل من استهلاك الملح",
        "content": "الإفراط في الملح يزيد من خطر ارتفاع ضغط الدم.",
        "source": "FDA"
    },
    {
        "title": "مارس النشاط البدني",
        "content": "30 دقيقة يوميًا من المشي أو الرياضة تحسن صحة القلب.",
        "source": "NCDC"
    },
    {
        "title": "اشرب كمية كافية من الماء",
        "content": "الماء ضروري للحفاظ على وظائف الجسم الحيوية.",
        "source": "WHO"
    },
    {
        "title": "تجنب التدخين",
        "content": "التدخين يزيد من خطر أمراض القلب والرئة.",
        "source": "FDA"
    }
]

# نخزنها في ملف JSON
with open("data/tips/latest.json", "w", encoding="utf-8") as f:
    json.dump(tips, f, ensure_ascii=False, indent=2)

# نعمل نسخة أرشيفية بتاريخ اليوم
archive_name = f"data/tips/archive-{datetime.now().date()}.json"
with open(archive_name, "w", encoding="utf-8") as f:
    json.dump(tips, f, ensure_ascii=False, indent=2)
