import asyncio
import flet as ft
import fletfly as fy

def color_page(color='black'): 
    return ft.Text(f"Color is {color}", color=color)

# Auto detected by wrapping
fy.Route({ # this will directly go beside his brothers deep in the tree
    "path": "a/b/c/d/e/blue", # look at the tree printed in next section
    "view": color_page,
    "color": "blue"
})
# delivered to router
green_page = {
    "path": "a/b/c/d/e/green",          # will directly go beside his brothers
    "view": (color_page, {"color": "green"}) # notice the printed tree next section
}

a = {
    "path": "a",
    "layout": lambda page: (ft.Text("Layout Header"), fy.slot(page)),
    "fly_in": lambda: True,   # middleware for all descendents
    "children": [
        {
        "path": "b",
        "children": [
            {
            "path": "c",
            "children": [
                {
                "path": "d",
                "children": [
                    {
                    "path": "e",
                    "children": [
                        {
                        "path": "red",
                        "view": fy.use.view(color_page, color="red"),
                        },
                        {
                        "path": ":color",
                        "view": color_page
                        },
                    ]
                    }
                ]
                }
            ]
            }
        ]
        }
    ]
}

fy.Router([a, green_page], print_path_zone='/a/b/c/d/e') # print only this branch

async def main(page):
    fy.fly(page)
    target_pages = [
        'a/b/c/d/e/red', 'a/b/c/d/e/blue', 'a/b/c/d/e/orange',
        'a/b/c/d/e/cyan', 'a/b/c/d/e/green', 'a/b/c/d/e/yellow'
    ]
    for _ in range(1): 
        for p in target_pages:
            await asyncio.sleep(2)
            fy.fly(page, p)

ft.run(main)