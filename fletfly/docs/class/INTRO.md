# fletfly
**The Component Composition Engine for Flet.**

"Stop writing procedural routing logic. With `fletfly`, fly with flet."

---

## 1. Quick Start.

```python
import flet as ft
from fletfly import Route, slot, fly, fly_in, child

class Home(Route):             # Route detection: path auto named to "/home"
    def layout(self, page):    # Auto-detected layout
        return ft.Column([
                ft.Text("Header"),
                slot(page) ])  # Nameless slot for injection
            
    @classmethod
    def fly_in(cls):           # Middleware
        return True
    
    @staticmethod               
    def contact():               # Sub route(method), named to "/home/contact"
        return ft.Text("Contact page")      # injected into self layout
    
    class User:                # Sub route(class), named to "/home/user"
        @classmethod
        def view(cls):         # main view detection, into layout inject
            return ft.Text('User page')     # injected into parent layout
    
    @child('about', value='About page')     # fast route "/home/about"
    @child('error', value='Error page')     # fast route "/home/error"
    class A(ft.Text): pass

ft.run(fly)                    # Start Router, with auto detection of routes.
```

## 2. Deeper Dive
Look at this single block of code. It demonstrates:
- Auto detection of routes, nested subroutes.
- Auto-path-naming (static & dynamic).
- Hierarchical layout inheritance, and final views.
- Multi & inheritable middlewares system.
- Lazy loading data injection into already opened pages.
- Named and nameless slots(outlets) injection.
- Auto detection by name, decoration, inheritance and values.
- All can be CBV instance dependent or static.
- Index detection (for index using programmers).
- Auto arguments manipulation, delivering what's needed including params & query.
- Start router with different options.

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

```python
from fletfly import Router, Route, slot, fly, child, data, fly_in, NavigationStyle, Shared
import flet as ft
import asyncio # just for mocking time delay

@Shared(value='same obj same data') # auto named to 'CardDeck'
class CardDeck(ft.TextField): pass

class Home():                  # Route detection: path auto named to "/home"
    
    def layout(self, page):    # Auto-detected layout by names (layout, frame)
        return ft.Column([
            ft.Text("Header"),
            data(page, ft.Text("loading..."), value="names.0"), # for loader
            slot(page),        # Anonymous slot (auto-injected)
            slot(page, "slot_a"),   # named slot (auto-injected)
            slot(page, "CardDeck", shared=True) # stuck always
        ])
    
    async def loader(self):          # auto detected lazy loader, injects data
        await asyncio.sleep(5)       # mocking delay for data fetching
        return {"names":["John"]}  # called by "names.0"
    
    class Index:               # Auto-detected index
    
        def view(self):        # Auto-detected view by names:
            return (           # (build, content, component, element)
            {"slot_a": ft.Text("Sir")},   # Binds to slot named 'slot_a'
            ft.Text("Hi"),     # Binds to first available nameless slot
            )
    
    class _Helper: pass        # Private scope (ignored by router)

    @child(":id")              # Sub route detection, path: "/home/:id"
    class User:
    
        def view(self, page):  # Injected into self or inheritable layout
            return (
                ft.Text(f"{page.fly.params.get('id','default')}"),   # URL params
                {"slot_a":ft.Text(f"{page.fly.query.get('color', 'default')}")}, # URL query
            )
    
        @fly_in(inheritable = True, param1='a') # detected by decoration
        @classmethod             # classmethod descriptor auto-unwrapped internally
        def func(cls, param1):
            return True

# handed father of class (or list of fathers of classes)
Router(Home, initial_route = "/home", error_path="/home", every_level_fallback=True, max_views=5, navigation_style=NavigationStyle.home_all_from_last_port, detect_route_subclasses=False, print_debugs=True)

def main(page):
    # your main stuff per user
    fly(page)
ft.run(main)            
```
</details>

## 3. Strict Explicit vs Magic Implicit.
Not only can you rely on magic auto-naming and detection with a wide variety of aliases, but you can also strictly use the explicit mode, defining all your properties with decorators or direct implementation.
<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

```Python
from fletfly import Router
Router(
    zone_or_class_or_list=[],       # hand over your class/classes to inject into the tree
    initial_route = "/",            # don't let us detect the initial for you
    error_path = "",                # don't let us show our error page, tell us where
    auto_path_naming=False,         # don't let us name your paths
    detect_created_routes=False,    # don't let us gather your created routes
    detect_route_subclasses=False,  # don't let us gather your routes inheriting from Route
    detect_method_routes=False,     # don't let us detect methods as subroutes
    detect_inner_classes=False,     # don't let us detect your inner classes as subroutes
    detect_method_ordinaries=False) # don't let us detect methods as props by name or value

```
</details>

<small>**[<font size="1">More About Aliases, Implicit and Explicit</font>](docs/class/Explicit.md)**</small>

## 4. Persistent Engine: Intelligent Reconciliation & Hero content.
No matter how many views you are opening in the views stack, and how many navigations you made, you only use 1 instance of each layout, 1 instance of each view or shared view, and you can choose whether to garbage it at the end of its usage or keep it alive by the view_hero & layout_hero options.

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

```Python
import flet as ft
from fletfly import Route, slot, fly
class Home(Route):
    layout_hero = False       # layout garbaged once no view uses it
    def layout(self, page):           
        return ft.Column([
            ft.Text("Header"),        
            slot(page)
            ])
    view_hero = True          # True means 1 in static, but 5 in dynamic
    def view(self):
        return ft.Text("Main view")
ft.run(fly)
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
from fletfly import Route, slot, fly, Shared
import flet as ft

class Home(Route):                  
    def layout(self, page):    
        return ft.Column([
            ft.Text("Header"),
            slot(page),        # Anonymous slot (ordered injection)
            slot(page, 1),        # named slot (specific injection)
            slot(page, 'a'),           # named slot (specific injection)
            slot(page, control=ft.Card()),  # default=ft.Container
            slot(page, "CardDeck", shared=True) # stuck always to shared view named "CardDeck"
        ])
    def view(self):
        return(
            {1: ft.Text("Going for slot called 1")},
            {'a': ft.Text("Going for slot called a")},
            ft.Text("Going for first nameless slot"),
            ft.Text("Going for second nameless slot"),
            ft.Text("Has nowhere to go")
            )
@Shared(value='I am shared')
class CardDeck(ft.TextField): pass

ft.run(fly)             
```
</details>

<small>**[<font size="1">More About Slots</font>](docs/class/SLOTS.md)**</small>

## 6. Layout .
Break the inheritance gracefully when you need an isolated view (like a login or settings page) within a nested structure.

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

```python
import flet as ft
from fletfly import Route, fly, slot, layout, child

class Home(Route):
    def layout(self, page):
        return ft.Column([
            ft.Text('Header'),
            slot(page)
        ])
    # @child(layout_override=True)     # decoration on class can work
    class Settings:
        layout_override=True           # direct implementation can work too
        @layout(override=True)         # method layout decoration works too
        def layout(self):          
            # returning one view means, forget everything, show me.
            return ft.View(controls=[ft.Text("I am a view")])
            # return ft.Text("I am not a view")  # try this instead
ft.run(main)
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
from fletfly import Route, fly, fly_in

def check_role(role='user'):          # general middleware with params
    return True if role == 'admin' else 'home'
    
class Home(Route):
    def view(self): return ft.Text("Main view")
    
    class Admin:
        def view(self): return ft.Text("Admin view")
        fly_in_override = True     # overrides all parent inheritable middlewares
        def fly_in_self(self): # middleware, detected by name
            return True
        
        @classmethod               
        @fly_in(inheritable = True, param1='a') # detected by decoration
        def func(cls, param1):
            return True

        d = fly_in(check_role, role='user')  # change role to "admin", to enter the page

def main(page):
    fly(page, '/home/admin')
ft.run(main)
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
from fletfly import Route, slot, fly, Shared
import flet as ft

@Shared(value='I am shared, change me') # auto named to 'CardDeck'
@Shared('CardDeck2', value='I am shared, change me too')
class CardDeck(ft.TextField): pass

class Home(Route):
    def layout(self, page):    # Auto-detected layout by names (layout, frame)
        return ft.Column([
            slot(page, "CardDeck", shared=True), # stuck always
            slot(page) ])
    def view(self): return 'CardDeck2'     # Shared but delivered by view
class A(Route):
    class B:
        class C:
            class D:
                class E:
                    def layout(self, page):
                        return ft.Column([
                            slot(page, "CardDeck", shared=True),
                            slot(page, "CardDeck2", shared=True)
                        ])
ft.run(fly)
```
</details>

<small>**[<font size="1">More About Shared</font>](docs/class/SHARED.md)**</small>

## 9. Lazy Loaders & data
Don't keep your users waiting till the data is fetched, open your pages, with default values, use data markers, and fetch your data by loader function.

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

```Python
import asyncio
import flet as ft
from fletfly import Route, data, fly
class Home(Route):
    async def loader(self):
        await asyncio.sleep(3)    # mocking data of 100 products
        return {"products":[         
                {"name": f"Product {i + 1}",
                "price": f"{ (i + 1) * 10 }$"}
                for i in range(100)]}
    def view(self, page): 
        return ft.GridView(expand=True, max_extent=200, spacing=10, controls =[
                ft.Card(content=ft.Column(alignment=ft.Alignment.CENTER, controls=[
                    data(page, 
                        ft.Text(value='loading...',
                                 size=16,
                                 weight='bold'),
                        value=f"products.{i}.name"),
                    data(page, 
                        ft.Text(value='loading...',
                                 size=14,
                                 color='green'),
                        value=f"products.{i}.price")
                ]))
                for i in range(100)
            ])   
ft.run(fly) 
```
</details>

<small>**[<font size="1">More About Loaders & data</font>](docs/class/LOADER.md)**</small>

## 10. Microfrontend With Zone and page.fly.
Add complete projects to your main project, not only one level but nested projects, inserted anywhere in your tree, without changing a letter in your code.
Use zone() function and navigate with page.fly, to reach relative paths in your sub projects.

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

#### Main Project
```Python
import flet as ft
from fletfly import Route, Zone, fly
from b10_zone import Home as Project1

class Home(Route): # Main project
    path = '/home'
    def view(self, page): return ft.Button("Go Project", on_click=lambda e: e.page.fly('home/project'))
    Project = Zone(Project1) # Zone

ft.run(fly)
```
#### Sub Project
```Python
import flet as ft
from fletfly import Route, fly

class Home(Route):
    path = '/home'
    def view(self, page):
        return ft.Column([
            ft.Text ("Sub project Home page"),
            ft.Button('Go settings', on_click=lambda e: e.page.fly('home/settings'))
        ])
    class Settings:
        path = '/home/settings'
        def view(self, page):
            return ft.Column([
                ft.Text ("Sub project Settings page"),
                ft.Button('Go Home', on_click=lambda e: e.page.fly('home'))
            ])
if __name__ == "__main__":
    ft.run(fly)
```
</details>

<small>**[<font size="1">More About Zone and fly</font>](docs/class/Zone.md)**</small>

## 11. Every level fallback
- Set your fallback style for any or all levels.
- Define your own overall error page, or let us show our 404.

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

```Python
import flet as ft
from fletfly import Route, Router, fly, child
import asyncio
class A(Route):      
    def view(self): return ft.Text('Normal class A view')
    class B:
        path = ":id"
        def view(self, id, color): return ft.Text(f"{id} page, color is {color}")
        class Fallback: # special fallback for zone C
            path = "*"
            def view(self): return ft.Text('Fallback for B zone')
    @child(path="*") # use path = "*" for fallback
    class Fallback:
        def view(self): return ft.Text('Fallback for A zone')

Router(error_path='a/*')
async def main(page):
    fly(page)
    target_pages = ['a/123?color="red"', 'a/b/c/d/e/f/g/h/i/j/k/l', 'a/m/n/o/p/q/r/s', 'something']
    for _ in range(3):
        for p in target_pages:
            await asyncio.sleep(5)
            page.fly(p)
ft.run(main)
```
</details>

<small>**[<font size="1">More About Fallbacks</font>](docs/class/fallback.md)**</small>

## 12. Very Deep Nesting.
- @child decorator or children list implementation are at your service.
- Multiple decorators stacking on the same class with different props.

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

```Python
import flet as ft
from fletfly import Route, Router, fly, child
import asyncio
class A(Route):      
    class B:
        class C:
            class D:
                class E:
                    @child('red_page', color = 'red')
                    @child(':color')
                    class ColoredPage:
                        def __init__(self, color='green'):
                            self.color = color
                        def view(self): return ft.Text(f"Color is {self.color}", color=self.color)
                    magenta_page = child(ColoredPage, color = 'magenta')
                    green_page = child(ColoredPage, color = 'green')
                    children=[
                        child(ColoredPage, 'blue-page', color='blue'),
                        child(ColoredPage, 'orange-page', color='orange')
                        ]
Router(print_path_zone='/a/b/c/d/e', )
async def main(page):
    fly(page)
    target_pages = ['a/b/c/d/e/red-page', 'a/b/c/d/e/blue-page', 'a/b/c/d/e/orange-page',
                    'a/b/c/d/e/brown-page', 'a/b/c/d/e/green-page', 'a/b/c/d/e/yellow']
    for _ in range(1): 
        for p in target_pages:
            await asyncio.sleep(3)
            page.fly(p)
ft.run(main)
```
</details>

<small>**[<font size="1">More About Children & Nesting</font>](docs/class/CHILDREN.md)**</small>

## 13. Router Configs and Debugs Example
- Set the max views opened in the same time.
- Select the chosen views to build.
- Use the builtin routes tree debug, static, dynamic & shared maps debugs.
- Set your fallback style, and error page.
- Use the terminal to follow your router, print a branch only option.
- The terminal in previous section 12 example would look like this:

<details>
<summary><font size="7"><b>👁️ Terminal Example</b></font></summary>

```text
[fletfly Debug] Time taken during [ importing all modules till start of router ]: 0.80ms
[fletfly Debug] Time taken during [ creating initial tree ]: 2.09ms
[fletfly Debug] Time taken during [ parsing static, dynamic & shared nodes maps ]: 0.74ms
-------------------- fletfly -- tree branch ---------------------
─ /a/b/c/d/e/ ─── cls:<E>            view:               ly:               to:                ins: 0  outs: 0 
    │ -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    ├── blue-page/ ──── cls:<ColoredPage>  view:"view"         ly:               to:                ins: 0  outs: 0  [STC]/a/b/c/d/e/blue-page
    │ -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    ├── orange-page/ ── cls:<ColoredPage>  view:"view"         ly:               to:                ins: 0  outs: 0  [STC]/a/b/c/d/e/orange-page
    │ -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    ├── :color/ ─────── cls:<ColoredPage>  view:"view"         ly:               to:                ins: 0  outs: 0  [DYN]/a/b/c/d/e/:color
    │ -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    ├── red-page/ ───── cls:<ColoredPage>  view:"view"         ly:               to:                ins: 0  outs: 0  [STC]/a/b/c/d/e/red-page
    │ -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    ├── magenta-page/ ─ cls:<ColoredPage>  view:"view"         ly:               to:                ins: 0  outs: 0  [STC]/a/b/c/d/e/magenta-page
    │ -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    └── green-page/ ─── cls:<ColoredPage>  view:"view"         ly:               to:                ins: 0  outs: 0  [STC]/a/b/c/d/e/green-page
      -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 

--------------------- fletfly -- static map ---------------------
layouts=[0]  view="N/A" fly_to=/a/b/c/d/e/red-page  path=''
layouts=[0]  view="view" fly_to=None  path='/a/b/c/d/e/blue-page'
layouts=[0]  view="view" fly_to=None  path='/a/b/c/d/e/orange-page'
layouts=[0]  view="view" fly_to=None  path='/a/b/c/d/e/red-page'
layouts=[0]  view="view" fly_to=None  path='/a/b/c/d/e/magenta-page'
layouts=[0]  view="view" fly_to=None  path='/a/b/c/d/e/green-page'
-------------------- fletfly -- dynamic map ---------------------
layouts=[0]  view="view" fly_to=None  path='/a/b/c/d/e/:color'
-------------------- fletfly -- shared map ----------------------
-----------------------------------------------------------------
[fletfly Debug] Time taken during [ triggering initial _handle_route_change by flet ]: 3264.29ms
---------- match path = / ----------
[fletfly] Redirecting by <fly_to> to: path '/a/b/c/d/e/red-page'
---------- match path = /a/b/c/d/e/red-page ----------
[fletfly Debug] Time taken during [ navigation preparation for reconciling ]: 0.74ms
[fletfly Debug] Time taken during [ reconciling views ]: 0.34ms
[fletfly Debug] Time taken during [ page update ]: 1.30ms
[fletfly Debug] Active views: 1 ['red-page']
[fletfly Debug] Active layouts: 0 
[fletfly Debug] Active shared views: 0 
[fletfly Debug] Active instances: 1 ['red-page']
[fletfly Debug] Hero views: 0 
[fletfly Debug] Hero layouts: 0 
[fletfly Debug] Hero shared: 0 
---------- match path = /a/b/c/d/e/blue-page ----------
[fletfly Debug] Time taken during [ navigation preparation for reconciling ]: 0.63ms
[fletfly Debug] Time taken during [ reconciling views ]: 0.29ms
[fletfly Debug] Time taken during [ page update ]: 0.86ms
[fletfly Debug] Active views: 1 ['blue-page']
[fletfly Debug] Active layouts: 0 
[fletfly Debug] Active shared views: 0 
[fletfly Debug] Active instances: 1 ['blue-page']
[fletfly Debug] Hero views: 0 
[fletfly Debug] Hero layouts: 0 
[fletfly Debug] Hero shared: 0 
```
</details>

<small>**[<font size="1">More About Configs</font>](docs/class/CONFIGS.md)**</small>
