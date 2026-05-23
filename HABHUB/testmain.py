import flet as ft
import random

# متغير بره الـ main (مشترك للسيرفر كله)
total_visitors = 0

def main(page: ft.Page):
    global total_visitors
    total_visitors += 1
    
    # رقم سري بيتولد "جوه" المين لكل يوزر
    session_id = random.randint(1000, 9999)
    
    # الطباعة دي هتظهر في الـ Terminal عندك كل ما تفتح تاب جديد
    print(f"✅ [Terminal] دالة الـ main اشتغلت لليوزر رقم: {total_visitors} | Session ID: {session_id}")
    
    page.add(
        ft.Text(f"أهلاً بك يا هندسة.. أنت الزائر رقم: {total_visitors}", size=30),
        ft.Text(f"كود الجلسة الخاص بك (Session ID): {session_id}", color="blue")
    )

# تشغيل كسيرفر ويب حقيقي على بورت 8080
# افتح اللينك ده في كذا تاب: http://127.0.0.1:8080
ft.run(main, port=8080, view=ft.AppView.WEB_BROWSER)