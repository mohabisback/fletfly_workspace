import flet as ft
import fletfly as fy
from fletfly import *
a = ft.Button.__annotations__.get("content")
print(type(a))
b = a.__args__
print(str in b) # True


obj = Route()


text = ft.Text("hi")
con = ft.Container(content = text)

def main(page):
    print("text id:", id(text))
    print("con.content.id:", id(con.content))
    print("con.parent:", con.parent)
    try:
        print(text.page)
    except Exception as e:
        print(e)
    page.add(con)
    print("con.id:", id(con))
    print("text parent:", text.parent)
    print("con.parent:", con.parent)
    print(text.page)
    page.views.clear()
    print("text id:", id(text))
    print("con.content.id:", id(con.content))
    print("con.parent:", con.parent)
    try:
        print(text.page)
    except Exception as e:
        print(e)
ft.run(main)