import flet as ft
import fletfly as fty

def say_hi(name):
    print("hi", name)
    return True

def say_bye(name, age):
    print("bye", name, ", your age is:", age)
    return True

def main(page: ft.Page):
    # بنبعت قائمة (List) فيها الدالتين مباشرة
    Pages = {
        "": lambda _: ft.Text("Home Page"),
        "$midwares": [(say_hi, "mohab"), (say_bye, "mohab", 44)],
        "sub":{
            "$midwares": (say_bye, "Bilal", 15),
            "subsub":{
                "": lambda _: ft.Text("Sub Page"),
            }
        }
    }
    
    fty.Airline(page, Pages)

if __name__ == "__main__":
    ft.run(main)