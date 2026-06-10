import flet as ft
import fletfly as fty

# 1. ميدل وير بيعمل ريدايركت لمسار "نسبي"
def mw_redirector():
    print(f"🔄 [MW] Redirecting from: {fty.route}")
    # هل هيروح لـ /login ولا لـ /dashboard/login ؟
    return "login" 

# 2. المشروع الفرعي (البورت)
SubProject = {
    "": lambda p: ft.Text("Sub-Project Home"),
    "login": lambda p: ft.Text("Sub-Project Login Page (Inner)"),
    "redirected_sub": fty.fly_in(mw_redirector)( lambda p: ft.Text("Sub redirected"))
}

# 3. المشروع الرئيسي
Pages = {
    "/": lambda p: ft.Text("Main Home"),
    "login": lambda p: ft.Text("Main Login Page (Global)"),
    
    # البورت راكب هنا
    "dashboard": {
        "app": fty.Zone(SubProject)
    },
    "redirected_main": fty.fly_in(mw_redirector)( lambda p: ft.Text("Main redirected"))
}

def main(page: ft.Page):
    fty.Router(page, Pages)

if __name__ == "__main__":
    ft.run(main)