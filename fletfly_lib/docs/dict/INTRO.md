# fletfly
**The Component Composition Engine for Flet.**

"Stop writing procedural routing logic. With `fletfly`, fly with flet."

---

## 1. Quick Start.

```python
import asyncio
import flet as ft
import fletfly as fy

def layout(page):
    return ft.Column([
        ft.Text("Header"),
        fy.slot(page)
    ])

def fly_in_middleware():
    return True

def contact_view():
    return ft.Text("Contact page")

def user_view():
    return ft.Text('User page')

def text(value=''):
    return ft.Text(value)
# Wrap(decorate) your dict with Route() for:
home = fy.Route({           # Auto detection and insertion into routes tree
    "path": None,           # auto-path naming to: '/home'
    "layout": layout,
    "fly_in": fly_in_middleware,
    "children": [
        {"path": "contact", "view": contact_view},
        {"path": "user", "view": user_view},
        {"path": "about", "view": text, "props": {"value": "About page"}},
        {"path": "error", "view": lambda: ft.Text("Error page")}
    ]
})

ft.run(fy.fly)                    # Start Router, with auto detection of routes.
```

## 2. Deeper Dive
Look at this single block of code. It demonstrates:
- Auto detection of routes.
- Auto-path-naming (static & dynamic).
- Hierarchical layout inheritance, and final views.
- Multi & inheritable middlewares system.
- Lazy loading data injection into already opened pages.
- Named and nameless slots(outlets) injection.
- Auto detection by name, decoration, inheritance and values.
- Index detection (for index using programmers).
- Auto arguments manipulation, delivering what's needed including params & query.
- Start router with different options.

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

```python
import asyncio # just for mocking time delay
import flet as ft
import fletfly as fy

class CardDeck(ft.TextField): pass
fy.Shared({                 # Auto detected and added
    "view":CardDeck,        # Auto named to 'CardDeck'
    "value":'its me everywhere' # Auto gathered props.
    })    

CardDeck2 = {               # Explicitly registered via Router
    "name":"CardDeck2",     # Explicitly named
    "view":CardDeck,
    "props":{               # Explicitly mentioned props
        "value":'same obj same data'
    }
}
def layout(page):    # Auto-detected layout by names (layout, frame)
    return ft.Column([
        ft.Text("Header"),
        fy.data(page, ft.Text("loading..."), value="names.0"), # for loader
        fy.slot(page),        # Anonymous slot (auto-injected)
        fy.slot(page, "slot_a"),   # named slot (auto-injected)
        fy.slot(page),        # Anonymous slot (auto-injected)
        fy.slot(page, "CardDeck2", shared=True) # stuck always
    ])

async def loader():          
    await asyncio.sleep(4)     # mocking delay for data fetching
    return {"names":["John"]}  # called by "names.0"

def view():
    return (           
    {"slot_a": ft.Text("Sir")},   # Binds to slot named 'slot_a'
    ft.Text("Hi"),     # Binds to first available nameless slot
    "CardDeck"       # shared view returned as part of view
    )

def user_view(page):  # Injected into self or inheritable layout
    return (
        ft.Text(f"{fy.fly(page).params.get('id','default')}"),   # URL params
        {"slot_a":ft.Text(f"{fy.fly(page).query.get('color', 'default')}")}, # URL query
        "CardDeck"   # shared view returned as part of view
    )

def func(param1):
    return True

home ={             # Explicitly registered via Router.
    "path": 'home',
    "layout": layout,
    "loader": loader,
    "view": view,
    "children": [
        {
            "path": ":id",  # Sub route, path: "/home/:id"
            "view": user_view,
            "fly_in": (func, {"inheritable": True, "param1": "a"})
        }
    ]
}

fy.Router(routes=[home], shared=[CardDeck2], initial_route = "/home",
          error_path="/home", every_level_fallback=False, max_views=5, 
          stack_mode=fy.StackMode.root_all_from_last_home, print_debugs=True)

def main(page):
    fy.fly(page)

if __name__ == "__main__":
    ft.run(main)        
```
</details>

## 3. Strict Explicit vs Magic Implicit.
Not only can you rely on magic auto-naming and detection with a wide variety of aliases, but you can also strictly use the explicit mode, defining all your properties with decorators or direct implementation.
<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

```Python
import flet as ft
import fletfly as fy 

# will not be registered by creation
home = {'path':'home'}              # explicit path only
shared = {'name':'shared'}          # explicit name only

fy.Router(
    routes=[home],                  # routes Registered explicitly
    shared=[shared],                # shared Registered explicitly
    initial_route = "/",            # don't let us detect the initial for you
    error_path = "",                # don't let us show our error page, tell us where
    auto_path_naming=False,         # don't let us name your paths
    detect_created_routes=False,    # don't let us gather your created routes
    detect_shared=False,            # don't let us gather your shared
)

def main(page):
    fy.fly(page)
if __name__ == "__main__":
    ft.run(main)
```
</details>

<small>**[<font size="1">More About Aliases, Implicit and Explicit</font>](docs/class/Explicit.md)**</small>

## 4. Persistent Engine: Intelligent Reconciliation & Hero content.
No matter how many views you are opening in the views stack, and how many navigations you made, you only use 1 instance of each layout, 1 instance of each view or shared view, and you can choose whether to garbage it at the end of its usage or keep it alive by the view_hero & layout_hero options.

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

```Python
import asyncio
import flet as ft
import fletfly as fy 

def layout(page):           
    return ft.Column([
        ft.Text("Header"),
        fy.slot(page)
    ])

def view():
    return ft.Text("Main view")

def user_view(page):
    category = fy.fly(page).params.get("category", "default")
    user_id = fy.fly(page).params.get("id", "default")
    return ft.Column([
        ft.Text(f" C: {category}"),
        ft.Text(f"id: {user_id}")
    ])

fy.Route({
    "path": "{category}",
    "layout": layout,
    "layout_hero": False,                  # layout_hero configuration
    "view": (view, {"hero": True}),        # True means 5 in dynamic, 1 in static
    "children": [
        {
            "path": ":id",
            "view": (user_view, {"hero": 2}) # max 2 pages are saved for different params
        }
    ]
})

ft.run(fy.fly)
```
</details>

<small>**[<font size="1">More About State Persistence & Hero</font>](docs/class/HERO.md)**</small>

## 5. Active Injection With Slots (Outlets).
Slots are at your service not the other way around.
- No limit on slots count.
- Named or nameless slots.
- Free slots or stuck to shared views.
- They could be any control you want (ft.Container as default).

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

```python
import flet as ft
import fletfly as fy 

def layout(page):    
    return ft.Column([
        ft.Text("Header"),
        fy.slot(page),        # Anonymous slot (ordered injection)
        fy.slot(page, 1),     # named slot (specific injection)
        fy.slot(page, 'a'),   # named slot (specific injection)
        fy.slot(page, control=ft.Card()), # default=ft.Container
        fy.slot(page, "CardDeck", shared=True) # stuck always to shared view named "CardDeck"
    ])

def view():
    return (
        {1: ft.Text("Going for slot called 1")},
        {'a': ft.Text("Going for slot called a")},
        ft.Text("Going for first nameless slot"),
        ft.Text("Going for second nameless slot"),
        ft.Text("Have no where to go")
    )

def CardDeck(value): 
    return ft.TextField(value)

shared = fy.Shared(CardDeck, value='I am shared')

fy.Route({
    "path": 'home',
    "layout": layout,
    "view": view
})

ft.run(fy.fly)
```
</details>

<small>**[<font size="1">More About Slots</font>](docs/class/SLOTS.md)**</small>

## 6. Layout Override.
Break the inheritance gracefully when you need an isolated view (like a login or settings page) within a nested structure.

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

```python
import asyncio
import flet as ft
import fletfly as fy 

def layout(page):
    return ft.Column([
        ft.Text('Header'),
        fy.slot(page)
    ])

def settings_layout():          
    return ft.Text("I am not a view")  
    # returning one view means, forget everything, show me.
    return ft.View(controls=[ft.Text("I am a view")]) # try this instead

home = fy.Route({
    "path": None,                                  
    "layout": layout,
    "children": [
        {
            "path": "settings",                    # Sub route, path: "/home/settings"
            "layout": (settings_layout, {"override": True}), # with layout
            "layout_override": True                # in the route
        }
    ]
})

ft.run(fy.fly)
```
</details>

<small>**[<font size="1">More About Layouts Overriding</font>](docs/class/Layout.md)**</small>

## 7. Multi & Inheritable Middleware System.
No matter how many middleware checks You want to perform, we have your back.
- General static or instance dependent.
- Sync or async
- Inheritable or Overriden.
- Applied once or applied each view
- True, False and Redirect str returns.

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

```Python
import flet as ft
import fletfly as fy 

def check_role(role='user'):          # general middleware with params
    return True if role == 'admin' else 'home'
    
def home_view(): 
    return ft.Text("Main view")

def admin_view(): 
    return ft.Text("Admin view")

def fly_in_self(): 
    return True

def func(param1):
    return True

home = {
    "path": "home",
    "view": home_view,
    "children": [
        {
            "path": "admin",          # Sub route, path: "/home/admin"
            "view": admin_view,
            "fly_in_override": True,  # Overriding parent middlewares
            "fly_ins": [
                (func, {"inheritable": True, "param1": "a"}), # Inheritable middleware with props via tuple
                (check_role, {"role": "user"}),               # External function with parameters via tuple
                fly_in_self                                   # Local middleware callable directly
            ]
        }
    ]
}

fy.Router(home)

def main(page):
    fy.fly(page, '/home/admin')

ft.run(main=main)
```
</details>

<small>**[<font size="1">More About fly_in Middlewares</font>](docs/class/FLYIN.md)**</small>

## 8. Shared Views.
A shared view is a view keeping its state outside the hierarchical tree, and can be:
- Class dependent or function dependent.
- Disposed after end of usage or immortal hero.
- Stuck into a slot of layout, or delivered as a complete or part of a page view.
- Created anywhere in your app and called everywhere.

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

```Python
import flet as ft
import fletfly as fy

class CardDeck(ft.TextField): pass

# Auto detected and added
fy.Shared({
    "view": CardDeck,
    "value": 'I am shared, change me'
})

# Explicitly registered via Router
CardDeck2 = {
    "name": "CardDeck2",
    "view": CardDeck,
    "props": {
        "value": 'I am shared, change me too'
    }
}

def home_layout(page):
    return ft.Column([
        fy.slot(page, "CardDeck", shared=True),
        fy.slot(page) 
    ])

def home_view(): 
    return 'CardDeck2'

def e_layout(page):
    return ft.Column([
        fy.slot(page, "CardDeck", shared=True),
        fy.slot(page, "CardDeck2", shared=True)
    ])

# --- Home Route Dict ---
home = {
    "path": "home",
    "layout": home_layout,
    "view": home_view
}

# --- Deep Nested Route Dict ---
e = {
    "path": "a/b/c/d/e",
    "layout": e_layout
}

fy.Router([home, e], shared=[CardDeck2])

ft.run(fy.fly)
```
</details>

<small>**[<font size="1">More About Shared</font>](docs/class/SHARED.md)**</small>

## 9. Lazy Loaders & data
Don't keep your users waiting till the data is fetched, open your pages, with default values, use `data()` markers, and fetch your data by `loader()` function.

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

```Python
import asyncio
import flet as ft
import fletfly as fy

async def loader():
    await asyncio.sleep(3)    # mocking data of 100 products
    return {"products":[         
            {"name": f"Product {i + 1}",
            "price": f"{ (i + 1) * 10 }$"}
            for i in range(100)]}

def view(page): 
    return ft.GridView(expand=True, max_extent=200, spacing=10, controls =[
            ft.Card(content=ft.Column(alignment=ft.Alignment.CENTER, controls=[
                fy.data(page, 
                    ft.Text(value='loading...',
                             size=16,
                             weight='bold'),
                    value=f"products.{i}.name"),
                fy.data(page, 
                    ft.Text(value='loading...',
                             size=14,
                             color='green'),
                    value=f"products.{i}.price")
            ]))
            for i in range(100)
        ])   

home = {
    "path": "home",
    "loader": loader,
    "view": view
}

fy.Router(home)

async def main(page):
    fy.fly(page)

ft.run(main=main)
```
</details>

<small>**[<font size="1">More About Loaders & data</font>](docs/class/LOADER.md)**</small>

## 10. Smart Dependency Injection
Stop worrying about matching boilerplate signatures. 
- Write only the parameters that your methods actually need.
- The `page` object, dynamic URL params, and query strings are auto-injected by name.
- Route-level props are automatically inherited by all route functions (view, layout, loader).
- specific props dedicated to individual external functions or middlewares.
- Pass your props via explicit `props = {}`, no-boilerplate `**kwargs`, or combining both.

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

```python
import flet as ft
import fletfly as fy

def external_func(auth=False):
    print("Middleware check passed")
    return auth

def layout(page, theme): 
    # Layout only requests 'theme' from route props
    return ft.Column([
        ft.Text(f"Theme: {theme}"),
        fy.slot(page)
    ])

def view(id, role, num): 
    # View requests 'id' (dynamic param) and 'role'/'num' (route props)
    return ft.Text(f"User {id} with number {num} is logged in as {role}")

profile = {
    "path": "profile/:id",
    "layout": layout,
    "view": view,
    "fly_ins": [
        (external_func, {"auth": True})  # Explicit middleware with parameters via tuple
    ],
    "role": "admin",     # Auto collected prop
    "theme": "dark",     # Auto collected prop
    "props": {"num": 3}  # Explicit props
}

fy.Router(profile)

async def main(page):
    fy.fly(page, 'profile/fletfly')

ft.run(main=main)
```
</details>

<small>**[<font size="1">More About Props</font>](docs/class/props.md)**</small>

## 11. Microfrontend With Zone and fy.fly(page).
- Add complete projects to your main project, not only one level but nested projects, inserted anywhere in your tree, without changing a letter in your code.
- Use `zone()` function and navigate with `fy.fly(page, )`, to reach relative paths in your sub projects.
- Deliver your module and let us handle the auto-detection magic, or manually provide your routes and shared objects.

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

#### Main Project
```Python
import flet as ft
import fletfly as fy 
import _11a as Project1 # import module of sub project

class CardDeck(ft.TextField): pass

fy.Shared({ # Auto detected, named and added
    "view": CardDeck,
    "value": 'I am "CardDeck" shared of Main Zone'
})

def home_view(): 
    return (
        ft.Text("Main Home page"),
        ft.Button("Go Sub Project", on_click=lambda e: e.fy.fly(page, 'home/project')),
        'CardDeck' 
    )

home = {
    "path": "home",
    "view": home_view,
    "children": [
        fy.Zone(
            modules= Project1,      # you have to pass the module itself
            routes = Project1.home, # we can't auto-detect unless wrapped
          # shared = Project1.shared   # it is auto-detected by wrapping
            path = 'project',    
            )       
    ]
}

fy.Router(home)

async def main(page):
    fy.fly(page)

ft.run(main=main)
```
#### Sub Project
```Python
import flet as ft
import fletfly as fy 

class CardDeck(ft.TextField): pass

# Auto detected, named and added
fy.Shared({
    "view": CardDeck,
    "hero": True,
    "value": 'I am "CardDeck" shared of Sub Project'
})

def sub_home_view():
    return (
        ft.Text("Sub project Home page"),
        ft.Button('Go settings', on_click=lambda e: e.fy.fly(page, 'home/settings')),
        ft.Button('Go Root Home', on_click=lambda e: e.fy.fly(page, 'home', root=True)),
        'CardDeck'
    )

def settings_view():
    return (
        ft.Text("Sub project Settings page"),
        ft.Button('Go Home', on_click=lambda e: e.fy.fly(page, 'home')),
        ft.Button('Go Root Home', on_click=lambda e: e.fy.fly(page, 'home', root=True)),
        'CardDeck'
    )

home = {
    "path": "home",
    "view": sub_home_view,
    "children": [
        {
        "path": "settings",
        "view": settings_view
        }
    ]
}


async def main(page):
    fy.fly(page)

if __name__ == "__main__":
    fy.Router(home)       # Router must be here
    ft.run(main=main)
```
</details>

<small>**[<font size="1">More About Zone and fly</font>](docs/class/zone.md)**</small>

## 12. Every level fallback
- Set your fallback style for any or all levels.
- Define your own overall error page, or let us show our 404.

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

```Python
import asyncio
import flet as ft
import fletfly as fy

def a_view(): 
    return ft.Text('Normal class A view')

def a_fallback_view(): 
    return ft.Text('Fallback for A zone')

def b_fallback_view(): 
    return ft.Text('Fallback for B zone')

def b_view(id, color): 
    return ft.Text(f"{id} page, color is {color}")

a = {
    "path": "a",
    "view": a_view,
    "children": [
        {
        "path": "b",
        "children": [
            {
           "path": ":id",
            "view": b_view
            },
            {
            "path": "*",
            "view": b_fallback_view
            }
        ]
        },
        {
        "path": "*",
        "view": a_fallback_view
        }
    ]
}

fy.Router(a, error_path='a/*')

ft.run(fy.fly)
```
</details>

<small>**[<font size="1">More About Fallbacks</font>](docs/class/fallback.md)**</small>

## 13. Auto Tree Injection, Deep Nesting & Route Reusability.

- **Auto Tree Injection:** Stop manually nesting complex subtrees. Just define your paths, and the engine automatically handles the routing hierarchy. We will inject descendents for you, inheriting all layouts & middlwares.
- **Deep Nesting:** Deeply nested routing structures are fully supported out of the box.
- **Route Multi-Instantiation:** Reuse the same view (or class) multiple times across different paths with different properties.
- **Stacking Children:** Support for stacking multiple `@child` decorators or calling `child()` multiple times with distinct configurations.
<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

```Python
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
```
</details>

<small>**[<font size="1">More About Children & Nesting</font>](docs/class/CHILDREN.md)**</small>

## 14. Router Configs and Debugs Example
- Set the max views opened in the same time.
- Select the chosen views to build in stack mode.
- Use the builtin routes tree debug, static, dynamic & shared maps debugs.
- Set your fallback style, and error page.
- Use the terminal to follow your router, print a branch only option.
- The terminal in previous section 13 example would look like this:

<details>
<summary><font size="7"><b>👁️ Terminal Example</b></font></summary>

```text
[fletfly Debug] Time taken during [ importing all modules till start of router ]: 0.34ms
[fletfly Debug] Time taken during [ creating initial tree ]: 1.13ms
[fletfly Debug] Time taken during [ parsing static, dynamic & shared nodes maps ]: 0.71ms
-------------------- fletfly -- tree branch ---------------------
─ /a/b/c/d/e/ ─── cls:               view:               ly:               to:                ins: 0  outs: 0 
    │ -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    ├── blue/ ───────── cls:               view:<color_page>   ly:               to:                ins: 0  outs: 0  [STC]/a/b/c/d/e/blue
    │ -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    ├── green/ ──────── cls:               view:<color_page>   ly:               to:                ins: 0  outs: 0  [STC]/a/b/c/d/e/green
    │ -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    ├── red/ ────────── cls:               view:<color_page>   ly:               to:                ins: 0  outs: 0  [STC]/a/b/c/d/e/red
    │ -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    └── :color/ ─────── cls:               view:<color_page>   ly:               to:                ins: 0  outs: 0  [DYN]/a/b/c/d/e/:color
      -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 

--------------------- fletfly -- static map ---------------------
layouts=[0]  view="N/A" fly_to=/a/b/c/d/e/red  path=''
layouts=[1]  view="N/A" fly_to=None  path='/a'
layouts=[1]  view=<color_page> fly_to=None  path='/a/b/c/d/e/blue'
layouts=[1]  view=<color_page> fly_to=None  path='/a/b/c/d/e/green'
layouts=[1]  view=<color_page> fly_to=None  path='/a/b/c/d/e/red'
-------------------- fletfly -- dynamic map ---------------------
layouts=[1]  view=<color_page> fly_to=None  path='/a/b/c/d/e/:color'
-------------------- fletfly -- shared map ----------------------
-----------------------------------------------------------------
http://127.0.0.1:11729
[fletfly Debug] Time taken during [ triggering initial _handle_route_change by flet ]: 2894.62ms
---------- match path = / ----------
[fletfly] Redirecting by <fly_to> to: path '/a/b/c/d/e/red'
---------- match path = /a/b/c/d/e/red ----------
[fletfly Debug] Time taken during [ navigation preparation for reconciling ]: 0.57ms
[fletfly Debug] Time taken during [ reconciling views ]: 3.51ms
[fletfly Debug] Time taken during [ page update ]: 2.94ms
[fletfly Debug] Active views: 2 ['a', 'red']
[fletfly Debug] Active layouts: 1 ['a']
[fletfly Debug] Active shared views: 0 
[fletfly Debug] Active instances: 0 
[fletfly Debug] Hero views: 0 
[fletfly Debug] Hero layouts: 0 
[fletfly Debug] Hero shared: 0 
---------- match path = /a/b/c/d/e/blue ----------
[fletfly Debug] Time taken during [ navigation preparation for reconciling ]: 1.04ms
[fletfly Debug] Time taken during [ reconciling views ]: 1.27ms
[fletfly Debug] Time taken during [ page update ]: 1.80ms
[fletfly Debug] Active views: 2 ['a', 'blue']
[fletfly Debug] Active layouts: 1 ['a']
[fletfly Debug] Active shared views: 0 
[fletfly Debug] Active instances: 0 
[fletfly Debug] Hero views: 0 
[fletfly Debug] Hero layouts: 0 
[fletfly Debug] Hero shared: 0 
```
</details>

<small>**[<font size="1">More About Configs</font>](docs/class/CONFIGS.md)**</small>
