# fletfly
**The Component Composition Engine for Flet.**

"Stop writing procedural routing logic. With `fletfly`, fly with flet."

---

## 1. Quick Start.

```python
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

# Declarative tree composition
home = fy.Route('home', fy.use.layout(layout), fy.use.fly_in(fly_in_middleware),
    children=[
        fy.Route('contact', contact_view),
        fy.Route('user', user_view),
        fy.Route('about', fy.use.view(text, value ="About page")),
        fy.Route('error', fy.use.view(lambda: ft.Text("Error page")))
    ])

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

# Auto-detected & named 'CardDeck'
fy.Shared(CardDeck, value='same obj same data') 

# Explicitly named and registered via Router
CardDeck2 = fy.Shared('CardDeck2', CardDeck, value='its me everywhere')

def layout(page):    
    return ft.Column([
        ft.Text("Header"),
        fy.data(page, ft.Text("loading..."), value="names.0"), # for loader
        fy.slot(page),              # Anonymous slot (auto-injected)
        fy.slot(page, "slot_a"),    # named slot (auto-injected)
        fy.slot(page),              # Anonymous slot (auto-injected)
        fy.slot(page, "CardDeck2", shared=True) # stuck always
    ])

async def loader():          
    await asyncio.sleep(4)      # mocking delay for data fetching
    return {"names":["John"]}   # called by "names.0"

def view():
    return (           
    {"slot_a": ft.Text("Sir")},   # Binds to slot named 'slot_a'
    ft.Text("Hi"),      # Binds to first available nameless slot
    "CardDeck"          # shared view returned as part of view
    )

def user_view(page):  # Injected into self or inheritable layout
    return (
        ft.Text(f"{page.fly.params.get('id','default')}"),   # URL params
        {"slot_a":ft.Text(f"{page.fly.query.get('color', 'default')}")}, # URL query
        "CardDeck"   # shared view returned as part of view
    )

def func(param1):
    return True

home = fy.Route(
    fy.use.layout(layout), 
    fy.use.loader(loader), 
    fy.use.view(view),
    children=[
        fy.Route(':id', # Sub route, path: "/home/:id"
            fy.use.view(user_view), 
            fy.use.fly_in(func, inheritable=True, param1='a') 
        )
    ]
)

fy.Router(routes=[home], shared=[CardDeck2], initial_route = "/home",
          error_path="/home", every_level_fallback=False, max_views=5, 
       stack_mode=fy.StackMode.root_all_from_last_home, print_debugs=True)

def main(page):
    # your main stuff per user
    fy.fly(page)
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
home = fy.Route('home')             # explicit path only
shared = fy.Shared('shared')        # explicit name only

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
    category = page.fly.params.get("category", "default")
    user_id = page.fly.params.get("id", "default")
    return ft.Column([
        ft.Text(f" C: {category}"),
        ft.Text(f"id: {user_id}")
    ])

home = fy.Route("{category}",
            fy.use.layout(layout),
            fy.use.view(view, hero=True),          # True means 5 in dynamic, 1 in static
            layout_hero=False,                     # layout_hero in route
            children=[
                fy.Route(":id",
                    fy.use.view(user_view, hero=2) # max 2 pages are saved for different params
        )
    ]
)

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

# Declarative tree composition
home = fy.Route(
    fy.use.layout(layout),
    fy.use.view(view)
)

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

# Declarative tree composition
home = fy.Route(
    fy.use.layout(layout),
    children=[
        fy.Route('settings',
            fy.use.layout(settings_layout, override=True), # override = layout_override
            layout_override=True, # layout_override
        )
    ]
)

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

# Declarative tree composition
home = fy.Route(
    fy.use.view(home_view),
    children=[
        # Child route with fly_in_override passed directly via kwargs props
        fy.Route('admin', 
            fy.use.view(admin_view),
            fly_in_override=True,
            fly_ins = [
                fy.use.fly_in(func, inheritable=True, param1='a'), # Registering inheritable middleware with props
                fy.use.fly_in(check_role, role='user'),             # Registering external function to fly_in explicitly with parameters (change role to "admin", to enter the page)
                fly_in_self
                ],                        # Registering local middleware explicitly
        )
    ]
)

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
import asyncio
import flet as ft
import fletfly as fy

class CardDeck(ft.TextField): pass
shared = fy.Shared(CardDeck, value='I am shared, change me') # auto-named to CardDeck
CardDeck2 = fy.Shared(CardDeck, value='I am shared, change me too')

def home_layout(page):    # Auto-detected layout
    return ft.Column([
        fy.slot(page, "CardDeck", shared=True), # stuck always
        fy.slot(page) 
    ])

def home_view(): 
    return 'CardDeck2'     # Shared but delivered by view

def e_layout(page):
    return ft.Column([
        fy.slot(page, "CardDeck", shared=True),
        fy.slot(page, "CardDeck2", shared=True)
    ])

# Declarative tree composition

# --- Home Route ---
home = fy.Route(
    fy.use.layout(home_layout),
    fy.use.view(home_view)
)

# --- Deep Nested Route (a/b/c/d/e) ---
e = fy.Route('/a/b/c/d/e',
    fy.use.layout(e_layout)
)

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

home = fy.Route(
    fy.use.loader(loader),
    fy.use.view(view)
)

ft.run(fy.fly)
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

# Route instance initialization with kwargs props
profile = fy.Route('profile/:id',
                layout= fy.use.layout(layout),
                fly_ins=[fy.use.fly_in(external_func, auth=True)], # Registering external function to fly_in explicitly
                view=fy.use.view(view),
                role='admin', theme='dark', props={'num':3},
)

def main(page):
    fy.fly(page, 'profile/fletfly')

ft.run(main)
```
</details>

<small>**[<font size="1">More About Props</font>](docs/class/props.md)**</small>

## 11. Microfrontend With Zone and page.fly.
- Add complete projects to your main project, not only one level but nested projects, inserted anywhere in your tree, without changing a letter in your code.
- Use `zone()` function and navigate with `page.fly()`, to reach relative paths in your sub projects.

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

#### Main Project
```Python
import flet as ft
import fletfly as fy 
from _11a import home as Project1 # Imported the Route instance instead of the class

class CardDeck(ft.TextField): pass
shared = fy.Shared(CardDeck, value='I am "CardDeck" shared of Main Zone')

def home_view(): 
    return (
        ft.Text("Main Home page"),
        ft.Button("Go Sub Project", on_click=lambda e: e.page.fly('home/project')),
        'CardDeck' 
    )

project = fy.Zone(Project1) # Zone, auto named to '/home/project'

home = fy.Route(
    fy.use.view(home_view),
    children=[
        project
    ]
)

ft.run(fy.fly)
```
#### Sub Project
```Python
import flet as ft
import fletfly as fy 

class CardDeck(ft.TextField): pass
shared = fy.Shared(CardDeck, hero=True, value='I am "CardDeck" shared of Sub Project')

def sub_home_view():
    return (
        ft.Text("Sub project Home page"),
        ft.Button('Go settings', on_click=lambda e: e.page.fly('home/settings')),
        ft.Button('Go Root Home', on_click=lambda e: e.page.fly('home', root=True)),
        'CardDeck'
    )

def settings_view():
    return (
        ft.Text("Sub project Settings page"),
        ft.Button('Go Home', on_click=lambda e: e.page.fly('home')),
        ft.Button('Go Root Home', on_click=lambda e: e.page.fly('home', root=True)),
        'CardDeck'
    )

home = fy.Route(
    fy.use.view(sub_home_view),
    children=[
        fy.Route('settings',
            fy.use.view(settings_view)
        )
    ]
)

if __name__ == "__main__":
    ft.run(fy.fly)
```
</details>

<small>**[<font size="1">More About Zone and fly</font>](docs/class/zone.md)**</small>

## 12. Every level fallback
- Set your fallback style for any or all levels.
- Define your own overall error page, or let us show our 404.

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

```Python
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

# Declarative tree composition
a = fy.Route(  # Route detection: path auto named to "/a"
    fy.use.view(a_view),
    children=[
        fy.Route('b',
            children=[
                fy.Route(':id',
                    fy.use.view(b_view)
                ),
                fy.Route('*',
                    fy.use.view(b_fallback_view)
                )
            ]
        ),
        fy.Route('*',
            fy.use.view(a_fallback_view)
        )
    ]
)

fy.Router(a, error_path='a/*')

ft.run(fy.fly)
```
</details>

<small>**[<font size="1">More About Fallbacks</font>](docs/class/fallback.md)**</small>

## 13. Deep Nesting & Route Reusability.

- Deeply nested routing structures are fully supported out of the box.

- Route Multi-Instantiation: Reuse the same view multiple times across different paths with different properties.

- Support for stacking multiple `@child` decorators or calling `child()` multiple times with distinct configurations.

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

```Python
import asyncio
import flet as ft
import fletfly as fy

def color_page(color='green'): 
    return ft.Text(f"Color is {color}", color=color)

blue_page = fy.Route(color_page, color='blue')
orange_page = fy.Route(fy.use.view(color_page), color='orange')

# Declarative tree composition
a = fy.Route('a',
    children=[
        fy.Route('b',
            children=[
                fy.Route('c',
                    children=[
                        fy.Route('d',
                            children=[
                                fy.Route('e',
                                    fy.use.child('green_page', fy.use.view(color_page, color='green')),
                                    fy.Route('cyan', fy.use.view(color_page), color='cyan'),
                                    blue_page,
                                    children=[
                                        fy.Route('red_page', fy.use.view(color_page), color='red'),   
                                        fy.Route(':color', fy.use.view(color_page)),                  
                                        orange_page
                                            ],
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )

fy.Router(a, print_path_zone='/a/b/c/d/e') # print only this branch

async def main(page):
    fy.fly(page)
    target_pages = [
        'a/b/c/d/e/red-page', 'a/b/c/d/e/blue-page', 'a/b/c/d/e/orange-page',
        'a/b/c/d/e/cyan', 'a/b/c/d/e/green-page', 'a/b/c/d/e/yellow'
    ]
    for _ in range(1): 
        for p in target_pages:
            await asyncio.sleep(2)
            page.fly(p)

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
[fletfly Debug] Time taken during [ importing all modules till start of router ]: 0.68ms
[fletfly Debug] Time taken during [ creating initial tree ]: 0.85ms
[fletfly Debug] Time taken during [ parsing static, dynamic & shared nodes maps ]: 0.42ms
-------------------- fletfly -- tree branch ---------------------
─ /a/b/c/d/e/ ─── cls:               view:               ly:               to:                ins: 0  outs: 0 
    │ -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    ├── :color/ ─────── cls:               view:<color_page>   ly:               to:                ins: 0  outs: 0  [DYN]/a/b/c/d/e/:color
    │ -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    ├── red-page/ ───── cls:               view:<color_page>   ly:               to:                ins: 0  outs: 0  [STC]/a/b/c/d/e/red-page
    │ -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    ├── green-page/ ─── cls:               view:<color_page>   ly:               to:                ins: 0  outs: 0  [STC]/a/b/c/d/e/green-page
    │ -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    ├── cyan-page/ ──── cls:               view:<color_page>   ly:               to:                ins: 0  outs: 0  [STC]/a/b/c/d/e/cyan-page
    │ -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    ├── blue-page/ ──── cls:               view:<color_page>   ly:               to:                ins: 0  outs: 0  [STC]/a/b/c/d/e/blue-page
    │ -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    └── orange-page/ ── cls:               view:<color_page>   ly:               to:                ins: 0  outs: 0  [STC]/a/b/c/d/e/orange-page
      -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 

--------------------- fletfly -- static map ---------------------
layouts=[0]  view="N/A" fly_to=/a/b/c/d/e/red-page  path=''
layouts=[0]  view=<color_page> fly_to=None  path='/a/b/c/d/e/red-page'
layouts=[0]  view=<color_page> fly_to=None  path='/a/b/c/d/e/green-page'
layouts=[0]  view=<color_page> fly_to=None  path='/a/b/c/d/e/cyan-page'
layouts=[0]  view=<color_page> fly_to=None  path='/a/b/c/d/e/blue-page'
layouts=[0]  view=<color_page> fly_to=None  path='/a/b/c/d/e/orange-page'
-------------------- fletfly -- dynamic map ---------------------
layouts=[0]  view=<color_page> fly_to=None  path='/a/b/c/d/e/:color'
-------------------- fletfly -- shared map ----------------------
-----------------------------------------------------------------
[fletfly Debug] Time taken during [ triggering initial _handle_route_change by flet ]: 1717.70ms
---------- match path = / ----------
[fletfly] Redirecting by <fly_to> to: path '/a/b/c/d/e/red-page'
---------- match path = /a/b/c/d/e/red-page ----------
[fletfly Debug] Time taken during [ navigation preparation for reconciling ]: 3.70ms
[fletfly Debug] Time taken during [ reconciling views ]: 0.34ms
[fletfly Debug] Time taken during [ page update ]: 1.48ms
[fletfly Debug] Active views: 1 ['red-page']
[fletfly Debug] Active layouts: 0 
[fletfly Debug] Active shared views: 0 
[fletfly Debug] Active instances: 0 
[fletfly Debug] Hero views: 0 
[fletfly Debug] Hero layouts: 0 
[fletfly Debug] Hero shared: 0 
---------- match path = /a/b/c/d/e/blue-page ----------
[fletfly Debug] Time taken during [ navigation preparation for reconciling ]: 0.67ms
[fletfly Debug] Time taken during [ reconciling views ]: 1.44ms
[fletfly Debug] Time taken during [ page update ]: 1.02ms
[fletfly Debug] Active views: 2 ['red-page', 'blue-page']
[fletfly Debug] Active layouts: 0 
[fletfly Debug] Active shared views: 0 
[fletfly Debug] Active instances: 0 
[fletfly Debug] Hero views: 0 
[fletfly Debug] Hero layouts: 0 
[fletfly Debug] Hero shared: 0 
```
</details>

<small>**[<font size="1">More About Configs</font>](docs/class/CONFIGS.md)**</small>
