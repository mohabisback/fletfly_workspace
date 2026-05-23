import os
import re

# المصدر
source = "fletfly/docs/class/INTRO.md"

# الأهداف (الهدف + البادئة اللي محتاجها عشان يوصل للـ docs من مكان الملف)
targets = {
    "README.md": "fletfly/",           # في الروت، بنضيف fletfly/ عشان يوصل للـ docs
    "fletfly/README.md": ""           # جوه المكتبة، الروابط بتبدأ بـ docs/ مباشرة
}

# قراءة المصدر
with open(source, 'r', encoding='utf-8') as f:
    content = f.read()

def sync_links(text, prefix):
    # نعدل الروابط اللي بتبدأ بـ docs/ عشان تشتغل من مكان الملف الهدف
    def replace(match):
        text_content = match.group(1)
        link_path = match.group(2)
        return f"[{text_content}]({prefix}{link_path})"

    return re.sub(r'\[([^\]]+)\]\((docs/[^)]+)\)', replace, text)

# التنفيذ
for target, prefix in targets.items():
    # التأكد من المسار قبل إنشاء المجلد
    dir_name = os.path.dirname(target)
    if dir_name:  # تأكد إنه مش فاضي قبل ما تنشئه
        os.makedirs(dir_name, exist_ok=True)
    
    # تعديل الروابط
    new_content = sync_links(content, prefix)
    
    # الكتابة
    with open(target, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Synced to: {target}")