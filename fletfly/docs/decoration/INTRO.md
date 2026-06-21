# fletfly
**The Component Composition Engine for Flet.**

"Stop writing procedural routing logic. With `fletfly`, fly with flet."

---

## 1. Quick Start.

```python
import flet as ft
import fletfly as fy

home = fy.Route()                          # Route detection: path auto named to "/home"

@home.use.layout
def layout(page):                       # Auto-detected layout
    return ft.Column([
            ft.Text("Header"),
            fy.slot(page) ])               # Nameless slot for injection
            
@home.use.fly_in
def fly_in():                           # Middleware
    return True

@home.use.child('contact')
def contact():                          # subroute from func, named to "/home/contact"
    return ft.Text("Contact page")      # injected into self layout

@home.use.child('about', value='About page')     # fast route "/home/about"
@home.use.child('error', value='Error page')     # fast route "/home/error"
class A(ft.Text): pass

user = fy.Route('user')                            # Subroute, named to "/home/user"
@user.use.view
def view():                         # main view detection, into layout inject
    return ft.Text('User page')     # injected into parent layout

home.children.append(user)

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

shared = fy.Shared() # Auto-named to CardDeck
@shared.use.view(value='its me everywhere')
class CardDeck(ft.TextField): pass

# Explicitly named & registered via Router.
CardDeck2 = fy.Shared('CardDeck2', CardDeck, value='same obj same data') # Explicitly named

home = fy.Route()  # Route detection: path auto named to "/home"

@home.use.layout
def layout(page):    
    return ft.Column([
        ft.Text("Header"),
        fy.data(page, ft.Text("loading..."), value="names.0"), # for loader
        fy.slot(page),        # Anonymous slot (auto-injected)
        fy.slot(page, "slot_a"),   # named slot (auto-injected)
        fy.slot(page),        # Anonymous slot (auto-injected)
        fy.slot(page, "CardDeck2", shared=True) # stuck always
    ])

@home.use.loader
async def loader():
    await asyncio.sleep(5)   # mocking delay for data fetching
    return {"names":["John"]}  # called by "names.0"

@home.use.view
def view():
    return (
    {"slot_a": ft.Text("Sir")},   # Binds to slot named 'slot_a'
    ft.Text("Hi"),      # Binds to first available nameless slot
    "CardDeck"          # shared view returned as part of view
    )

user = fy.Route(':id')

@user.use.view
def user_view(page):  # Injected into self or inheritable layout
    return (
        ft.Text(f"{page.fly.params.get('id','default')}"),   # URL params
        {"slot_a":ft.Text(f"{page.fly.query.get('color', 'default')}")}, # URL query
        "CardDeck"   # shared view returned as part of view
    )

@user.use.fly_in(inheritable = True, param1='a')
def func(param1):
    return True

home.children.append(user)

fy.Router(routes=[home], shared=[shared], initial_route = "/home",
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

home = fy.Route("{category}", layout_hero=False) # layout_here in route

@home.use.layout
def layout(page):           
    return ft.Column([
        ft.Text("Header"),
        fy.slot(page)
    ])

@home.use.view(hero=True)         # True means 5 in dynamic, 1 in static
def view():
    return ft.Text("Main view")

user = fy.Route(":id")

@user.use.view(hero=2)            # max 2 pages are saved for different params
def user_view(page):
    category = page.fly.params.get("category", "default")
    user_id = page.fly.params.get("id", "default")
    return ft.Column([
        ft.Text(f" C: {category}"),
        ft.Text(f"id: {user_id}")
    ])

home.children.append(user)

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

home = fy.Route()

@home.use.layout
def layout(page):    
    return ft.Column([
        ft.Text("Header"),
        fy.slot(page),        # Anonymous slot (ordered injection)
        fy.slot(page, 1),     # named slot (specific injection)
       fy.slot(page, 'a'),   # named slot (specific injection)
       fy.slot(page, control=ft.Card()), # default=ft.Container
       fy.slot(page, "CardDeck", shared=True) # stuck always to shared view named "CardDeck"
    ])

@home.use.view
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

ft.run(fy.fly)
```
</details>

<small>**[<font size="1">More About Slots</font>](docs/class/SLOTS.md)**</small>

## 6. Layout Override.
Break the inheritance gracefully when you need an isolated view (like a login or settings page) within a nested structure.

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

```python
import flet as ft
import fletfly as fy 

home = fy.Route()

@home.use.layout
def layout(page):
    return ft.Column([
        ft.Text('Header'),
        fy.slot(page)
    ])

settings = fy.Route('settings', layout_override=True) # layout_override

@settings.use.layout(override = True) # override = layout_override
def settings_layout():          
    return ft.Text("I am not a view")  
    # returning one view means, forget everything, show me.
    return ft.View(controls=[ft.Text("I am a view")]) # try this instead

home.children.append(settings)

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
    
home = fy.Route()

@home.use.view
def home_view(): 
    return ft.Text("Main view")

# Child route with fly_in_override passed directly via kwargs props
admin = fy.Route('admin', fly_in_override=True)

@admin.use.view
def admin_view(): 
    return ft.Text("Admin view")

# Registering local middleware explicitly
@admin.use.fly_in
def fly_in_self(): 
    return True

# Registering inheritable middleware with props
@admin.use.fly_in(inheritable=True, param1='a')
def func(param1):
    return True

# Registering external function to fly_in explicitly with parameters
admin.use.fly_in(role='user')(check_role)  # change role to "admin", to enter the page

home.children.append(admin)

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
shared = fy.Shared(CardDeck, value='I am shared, change me') # auto-named to CardDeck
CardDeck2 = fy.Shared(CardDeck, value='I am shared, change me too')

# --- Home Route ---
home = fy.Route()

@home.use.layout
def home_layout(page):    # Auto-detected layout
    return ft.Column([
        fy.slot(page, "CardDeck", shared=True), # stuck always
        fy.slot(page) 
    ])

@home.use.view
def home_view(): 
    return 'CardDeck2'     # Shared but delivered by view


# --- Deep Nested Route (a/b/c/d/e) ---
e =fy.Route('/a/b/c/d/e')

@e.use.layout
def e_layout(page):
    return ft.Column([
        fy.slot(page, "CardDeck", shared=True),
        fy.slot(page, "CardDeck2", shared=True)
    ])

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

home = fy.Route()

@home.use.loader
async def loader():
    await asyncio.sleep(3)    # mocking data of 100 products
    return {"products":[         
            {"name": f"Product {i + 1}",
            "price": f"{ (i + 1) * 10 }$"}
            for i in range(100)]}

@home.use.view
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

# Route instance initialization with kwargs props
profile = fy.Route('profile/:id', role='admin', theme='dark', props={'num':3})

@profile.use.layout
def layout(page, theme): 
    # Layout only requests 'theme' from route props
    return ft.Column([
        ft.Text(f"Theme: {theme}"),
        fy.slot(page)
    ])

# Registering external function to fly_in explicitly
profile.fly_ins.append(fy.Route.fly_in(external_func, auth=True))
# or
profile.use.fly_in(auth=True)(external_func) # decoration immitation

@profile.use.view
def view(id, role, num): 
    # View requests 'id' (dynamic param) and 'role'/'num' (route props)
    return ft.Text(f"User {id} with number {num} is logged in as {role}")

def main(page):
    fy.fly(page, 'profile/fletfly')

ft.run(main)
```
</details>

<small>**[<font size="1">More About Props</font>](docs/class/props.md)**</small>

## 11. Microfrontend With Zone and page.fly.
- Add complete projects to your main project, not only one level but nested projects, inserted anywhere in your tree, without changing a letter in your code.
- Use `zone()` function and navigate with `page.fly()`, to reach relative paths in your sub projects.
- Deliver your module and let us handle the auto-detection magic, or manually provide your routes and shared objects.

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

#### Main Project
```Python
import flet as ft
import fletfly as fy 
import _11a as Project1 # Import module of Sub project

shared = fy.Shared()
@shared.use.view(value='I am "CardDeck" shared of Main Zone')
class CardDeck(ft.TextField): pass

home = fy.Route() # Main project '/home'

@home.use.view
def home_view(): 
    return (
        ft.Text("Main Home page"),
        ft.Button("Go Sub Project", on_click=lambda e: e.page.fly('home/project')),
        'CardDeck' 
    )
    
project = fy.Zone(
    modules= Project1,          # module of second project
  # routes = Project1.home,     # if auto-detection is off
  # shared = Project1.shared,   # if auto-detection is off
  # path = 'project'            #if auto-naming is off
    )
home.children.append(project)

ft.run(fy.fly)
```
#### Sub Project
```Python
import flet as ft
import fletfly as fy 

class CardDeck(ft.TextField): pass
shared = fy.Shared(CardDeck, hero=True, value='I am "CardDeck" shared of Sub Project')

home = fy.Route()

@home.use.view
def sub_home_view():
    return (
        ft.Text("Sub project Home page"),
        ft.Button('Go settings', on_click=lambda e: e.page.fly('home/settings')),
        ft.Button('Go Root Home', on_click=lambda e: e.page.fly('home', root=True)),
        'CardDeck'
    )

settings = fy.Route()

@settings.use.view
def settings_view(page):
    return (
        ft.Text("Sub project Settings page"),
        ft.Button('Go Home', on_click=lambda e: e.page.fly('home')),
        ft.Button('Go Root Home', on_click=lambda e: e.page.fly('home', root=True)),
        'CardDeck'
    )

home.children.append(settings)

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

a = fy.Route()  # Route detection: path auto named to "/a"

@a.use.view
def a_view(): 
    return ft.Text('Normal class A view')

a_fallback = fy.Route('*')

@a_fallback.use.view
def a_fallback_view(): 
    return ft.Text('Fallback for A zone')

b = fy.Route()

b_fallback = fy.Route('*')

@b_fallback.use.view
def b_fallback_view(): 
    return ft.Text('Fallback for B zone')

c = fy.Route(':id')

@c.use.view
def b_view(id, color): 
    return ft.Text(f"{id} page, color is {color}")

b.children.extend([c, b_fallback])
a.children.extend([b, a_fallback])

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
import flet as ft
import fletfly as fy 
import asyncio


# Auto detected by wrapping
blue_page=fy.Route(
    path="a/b/c/d/e/blue", # injected directly beside his brothers
    color="blue"
)

# delivered to router
green_page = fy.Route(
    path="a/b/c/d/e/green", # injected directly beside his brothers
)

a = fy.Route(
    path="a", 
    layout=lambda page: (ft.Text("Layout Header"), fy.slot(page)), 
    fly_in=lambda: True  # middleware for all descendents
)
b = fy.Route(path="b")
c = fy.Route(path="c")
d = fy.Route(path="d")
e = fy.Route(path="e")

a.children.append(b)
b.children.append(c)
c.children.append(d)
d.children.append(e)

@blue_page.use.view                 # route uses the func as view
@green_page.use.view(color='green') # route uses the func as view
@e.use.child('red', color='red')    # creates sub route with func as view
@e.use.child(':color')              # creates sub route with func as view
def color_page(color='black'): 
    return ft.Text(f"Color is {color}", color=color)

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
[fletfly Debug] Time taken during [ creating initial tree ]: 0.98ms
[fletfly Debug] Time taken during [ parsing static, dynamic & shared nodes maps ]: 0.67ms
-------------------- fletfly -- tree branch ---------------------
─ /a/b/c/d/e/ ─── cls:               view:               ly:               to:                ins: 0  outs: 0 
    │ -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    ├── blue/ ───────── cls:               view:<color_page>   ly:               to:                ins: 0  outs: 0  [STC]/a/b/c/d/e/blue
    │ -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    ├── :color/ ─────── cls:               view:<color_page>   ly:               to:                ins: 0  outs: 0  [DYN]/a/b/c/d/e/:color
    │ -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    ├── red/ ────────── cls:               view:<color_page>   ly:               to:                ins: 0  outs: 0  [STC]/a/b/c/d/e/red
    │ -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    └── green/ ──────── cls:               view:<color_page>   ly:               to:                ins: 0  outs: 0  [STC]/a/b/c/d/e/green
      -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 

--------------------- fletfly -- static map ---------------------
layouts=[0]  view="N/A" fly_to=/a/b/c/d/e/red  path=''
layouts=[1]  view="N/A" fly_to=None  path='/a'
layouts=[1]  view=<color_page> fly_to=None  path='/a/b/c/d/e/blue'
layouts=[1]  view=<color_page> fly_to=None  path='/a/b/c/d/e/red'
layouts=[1]  view=<color_page> fly_to=None  path='/a/b/c/d/e/green'
-------------------- fletfly -- dynamic map ---------------------
layouts=[1]  view=<color_page> fly_to=None  path='/a/b/c/d/e/:color'
-------------------- fletfly -- shared map ----------------------
-----------------------------------------------------------------
http://127.0.0.1:11869
[fletfly Debug] Time taken during [ triggering initial _handle_route_change by flet ]: 2867.81ms
---------- match path = / ----------
[fletfly] Redirecting by <fly_to> to: path '/a/b/c/d/e/red'
---------- match path = /a/b/c/d/e/red ----------
[fletfly Debug] Time taken during [ navigation preparation for reconciling ]: 1.32ms
[fletfly Debug] Time taken during [ reconciling views ]: 3.81ms
[fletfly Debug] Time taken during [ page update ]: 2.71ms
[fletfly Debug] Active views: 2 ['a', 'red']
[fletfly Debug] Active layouts: 1 ['a']
[fletfly Debug] Active shared views: 0 
[fletfly Debug] Active instances: 0 
[fletfly Debug] Hero views: 0 
[fletfly Debug] Hero layouts: 0 
[fletfly Debug] Hero shared: 0 
---------- match path = /a/b/c/d/e/blue ----------
[fletfly Debug] Time taken during [ navigation preparation for reconciling ]: 1.03ms
[fletfly Debug] Time taken during [ reconciling views ]: 1.02ms
[fletfly Debug] Time taken during [ page update ]: 1.56ms
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
