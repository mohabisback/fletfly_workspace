# fletfly
**The Component Composition Engine for Flet.**

"Stop writing procedural routing logic. With `fletfly`, fly with flet."

---

## 1. Quick Start.

```python
import flet as ft
import fletfly as fy

class Home(fy.Route):             # Route detection: path auto named to "/home"
    def layout(self, page):    # Auto-detected layout
        return ft.Column([
                ft.Text("Header"),
                fy.slot(page) ])  # Nameless slot for injection
            
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
    
    @fy.child('about', value='About page')     # fast route "/home/about"
    @fy.child('error', value='Error page')     # fast route "/home/error"
    class A(ft.Text): pass

ft.run(fy.fly)                    # Start Router, with auto detection of routes.
```

## 2. Deeper Dive
Look at this single block of code. It demonstrates:
- Auto detection of Class Based Routes, nested subroutes.
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
import flet as ft
import fletfly as fy
import asyncio # just for mocking time delay

@fy.Shared(value="It's me everywhere") # detected & auto named to 'CardDeck'
class CardDeck(ft.TextField): pass
# Explicitly named and registered via Router
shared = fy.Shared('CardDeck2', CardDeck, value='same obj same data')

class Home():                  # Route detection: path auto named to "/home"
    
    def layout(self, page):    # Auto-detected layout by names (layout, frame)
        return ft.Column([
            ft.Text("Header"),
            fy.data(page, ft.Text("loading..."), value="names.0"), # for loader
            fy.slot(page),        # Anonymous slot (auto-injected)
            fy.slot(page, "slot_a"),   # named slot (auto-injected)
            fy.slot(page),        # Anonymous slot (auto-injected)
            fy.slot(page, "CardDeck2", shared=True) # stuck always
        ])
    
    async def loader(self):          # auto detected lazy loader, injects data
        await asyncio.sleep(5)       # mocking delay for data fetching
        return {"names":["John"]}  # called by "names.0"
    
    class Index:               # Auto-detected index
    
        def view(self):        # Auto-detected view by names:
            return (           # (build, content, component, element)
            {"slot_a": ft.Text("Sir")},   # Binds to slot named 'slot_a'
            ft.Text("Hi"),     # Binds to first available nameless slot
            "CardDeck"       # shared view returned as part of view
            )
    
    class _Helper: pass        # Private scope (ignored by router)

    @fy.child(":id")              # Sub route detection, path: "/home/:id"
    class User:
    
        def view(self, page):  # Injected into self or inheritable layout
            return (
                ft.Text(f"{fy.fly(page).params.get('id','default')}"),   # URL params
                {"slot_a":ft.Text(f"{fy.fly(page).query.get('color', 'default')}")}, # URL query
                "CardDeck"   # shared view returned as part of view
            )
    
        @fy.fly_in(inheritable = True, param1='a') # detected by decoration
        @classmethod             # classmethod descriptor auto-unwrapped internally
        def func(cls, param1):
            return True

# handed father of class (or list of fathers of classes)
fy.Router(routes=[Home], shared=[shared], initial_route = "/home",
        error_path="/home", every_level_fallback=False, max_views=5, 
        stack_mode=fy.StackMode.root_all_from_last_home,
        detect_route_subclasses=False, print_debugs=True)


async def main(page):
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
# will not be registered by decoration

class Home(fy.Route):               # will not be registered by inheritence
    path = 'home'
    def layout(self):               # will not be detected by name
        pass
    check = fy.fly_in(lambda _: True)  # will not be detected by value
    
    def settings(self):             # Method will not create a subroute
        pass
    class User:                     # Inner class will not create a subroute
        pass

class Shared(ft.Text):              # will not be registered by creation
    name = 'shared'
fy.Router(
    routes=[Home],                  # Class Registered explicitly
    shared=[Shared],                # Class Registered explicitly 
    initial_route = "/",            # don't let us detect the initial for you
    error_path = "",                # don't let us show our error page, tell us where
    auto_path_naming=False,         # don't let us name your paths
    detect_route_subclasses=False,  # don't let us gather your routes inheriting from Route
    detect_method_routes=False,     # don't let us detect methods as subroutes
    detect_inner_classes=False,     # don't let us detect your inner classes as subroutes
    detect_method_ordinaries=False, # don't let us detect methods as props by name or value
    detect_shared=False)            # don't let us gather your shared
def main(page):
    fy.fly(page)
if __name__ == "__main__":
    ft.run(main)
```
</details>

<small>**[<font size="1">More About Aliases, Implicit and Explicit</font>](docs/Explicit.md)**</small>

## 4. Persistent Engine: Intelligent Reconciliation & Hero content.
No matter how many views you are opening in the views stack, and how many navigations you made, you only use 1 instance of each layout, 1 instance of each view or shared view, and you can choose whether to garbage it at the end of its usage or keep it alive by the view_hero & layout_hero options.

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

```Python
import flet as ft
import fletfly as fy

@fy.Route('{category}', layout_hero=False) # dynamic page
class Home:
    def layout(self, page):           # layout deleted once no view uses it(default)
        return ft.Column([
            ft.Text("Header"),
            fy.slot(page)
            ])
    view_hero = True                  # True means 5 in dynamic, 1 in static
    def view(self):
        return ft.Text("Main view")
    class User:
        path = ":id"                  # dynamic page
        @fy.Route.view(hero=2)           # max 2 pages are saved for different params
        def view(self, category, id):
            return ft.Column([
                    ft.Text(f" C: {category}"),
                    ft.Text(f"id: {id}")
                    ])
ft.run(fy.fly)
```
</details>

<small>**[<font size="1">More About State Persistence & Hero</font>](docs/HERO.md)**</small>

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

class Home(fy.Route):                  
    def layout(self, page):    
        return ft.Column([
            ft.Text("Header"),
            fy.slot(page),        # Anonymous slot (ordered injection)
            fy.slot(page, 1),     # named slot (specific injection)
            fy.slot(page, 'a'),   # named slot (specific injection)
            fy.slot(page, control=ft.Card()), # default=ft.Container
            fy.slot(page, "CardDeck", shared=True) # stuck always to shared view named "CardDeck"
        ])
    def view(self):
        return(
            {1: ft.Text("Going for slot called 1")},
            {'a': ft.Text("Going for slot called a")},
            ft.Text("Going for first nameless slot"),
            ft.Text("Going for second nameless slot"),
            ft.Text("Have no where to go")
            )
@fy.Shared(value='I am shared')
class CardDeck(ft.TextField): pass

ft.run(fy.fly)                 
```
</details>

<small>**[<font size="1">More About Slots</font>](docs/SLOTS.md)**</small>

## 6. Layout Override.
Break the inheritance gracefully when you need an isolated view (like a login or settings page) within a nested structure.

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

```python
import flet as ft
import fletfly as fy

class Home(fy.Route):
    def layout(self, page):
        return ft.Column([
            ft.Text('Header'),
            fy.slot(page)
        ])
    # @child(layout_override=True)     # decoration on class can work
    class Settings:
        layout_override=True           # direct implementation can work too
        @fy.layout(override=True)         # method layout decoration works too
        def layout(self):          
            return ft.Text("I am not a view")
            # returning one view means, forget everything, show me.
            return ft.View(controls=[ft.Text("I am a view")]) # try this instead
ft.run(fy.fly)
```
</details>

<small>**[<font size="1">More About Layouts Overriding</font>](docs/Layout.md)**</small>

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
    
class Home(fy.Route):
    def view(self): return ft.Text("Main view")
    
    class Admin:
        def view(self): return ft.Text("Admin view")
        fly_in_override = True     # overrides all parent inheritable middlewares
        def fly_in_self(self): # middleware, detected by name
            return True
        
        @classmethod               
        @fy.fly_in(inheritable = True, param1='a') # detected by decoration
        def func(cls, param1):
            return True

        d = fy.fly_in(check_role, role='user')  # change role to "admin", to enter the page

def main(page):
    fy.fly(page, '/home/admin')
ft.run(main)
```
</details>

<small>**[<font size="1">More About fly_in Middlewares</font>](docs/FLYIN.md)**</small>

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

@fy.Shared(value='I am shared, change me') # auto named to 'CardDeck'
@fy.Shared('CardDeck2', value='I am shared, change me too')
class CardDeck(ft.TextField): pass

class Home(fy.Route):
    def layout(self, page):    # Auto-detected layout by names (layout, frame)
        return ft.Column([
            fy.slot(page, "CardDeck", shared=True), # stuck always
            fy.slot(page) ])
    def view(self): return 'CardDeck2'     # Shared but delivered by view
class A(fy.Route):
    class B:
        class C:
            class D:
                class E:
                    def layout(self, page):
                        return ft.Column([
                            fy.slot(page, "CardDeck", shared=True),
                            fy.slot(page, "CardDeck2", shared=True)
                        ])
ft.run(fy.fly)
```
</details>

<small>**[<font size="1">More About Shared</font>](docs/SHARED.md)**</small>

## 9. Lazy Loaders & data
Don't keep your users waiting till the data is fetched, open your pages, with default values, use `data()` markers, and fetch your data by `loader()` function.

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

```Python
import asyncio
import flet as ft
import fletfly as fy
class Home(fy.Route):
    async def loader(self):
        await asyncio.sleep(3)    # mocking data of 100 products
        return {"products":[         
                {"name": f"Product {i + 1}",
                "price": f"{ (i + 1) * 10 }$"}
                for i in range(100)]}
    def view(self, page): 
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

<small>**[<font size="1">More About Loaders & data</font>](docs/LOADER.md)**</small>

## 10. Smart Dependency Injection
Stop worrying about matching boilerplate signatures. 
- Write only the parameters that your methods actually need.
- The `page` object, dynamic URL params, and query strings are auto-injected by name.
- Class-level props are automatically inherited by all inner methods and classes.
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

@fy.Route('profile/:id', role='admin', theme='dark', props={'num':3}) # Route props via **kwargs
class Profile:
    # Layout only requests 'theme' from route props
    def layout(self, page, theme): 
        return ft.Column([
            ft.Text(f"Theme: {theme}"),
            fy.slot(page)
        ])
    fly_in = fy.Route.fly_in(external_func, auth=True) # specific props
    # View requests 'id' (dynamic param) and 'role' (route prop)
    def view(self, id, role, num): 
        return ft.Text(f"User {id} with number {num} is logged in as {role}")
def main(page):
    fy.fly(page, 'profile/fletfly')
ft.run(main)
```
</details>

<small>**[<font size="1">More About Props</font>](docs/props.md)**</small>

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

@fy.Shared(value = 'I am "CardDeck" shared of Main Zone')
class CardDeck(ft.TextField): pass

class Home(fy.Route): # Main project '/home'
    def view(self): return (
                ft.Text ("Main Home page"),
                ft.Button("Go Sub Project", on_click=lambda e: fy.fly(e.page, 'home/project')),
                'CardDeck' )
    
    project = fy.Zone(
        modules= Project1,            # module of second project
        # routes = Project1.home,     # if auto-detection is off
        # shared = Project1.shared,   # if auto-detection is off
        # path = 'project'            #if auto-naming is off
            )
ft.run(fy.fly)
```
#### Sub Project
```Python
import flet as ft
import fletfly as fy

@fy.Shared(hero=True, value = 'I am "CardDeck" shared of Sub Project')
class CardDeck(ft.TextField): pass

class Home(fy.Route):
    path = '/home'
    def view(self):
        return (
            ft.Text ("Sub project Home page"),
            ft.Button('Go settings', on_click=lambda e: fy.fly(e.page, 'home/settings')),
            ft.Button('Go Root Home', on_click=lambda e: fy.fly(e.page, 'home', root=True)),
            'CardDeck'
        )
    class Settings:
        path = '/home/settings'
        def view(self):
            return (
                ft.Text ("Sub project Settings page"),
                ft.Button('Go Home', on_click=lambda e: fy.fly(e.page, 'home')),
                ft.Button('Go Root Home', on_click=lambda e: fy.fly(e.page, 'home', root=True)),
                'CardDeck'
            )
if __name__ == "__main__":
    ft.run(fy.fly)
```
</details>

<small>**[<font size="1">More About Zone and fly</font>](docs/zone.md)**</small>


## 12. Index vs Child vs Children 
- child is used to add a child, but it is not a property of a Route.
- children is used, but it is a list property
- index is complete but pathless childless child acting as a default for parent which has no view.

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

```Python
import flet as ft
import fletfly as fy


class A(fy.Route):
    @fy.child('b')  
    class B: pass

    @fy.child('c')
    def c(): pass

    @fy.index      
    class D:
        def view(self): return ft.Text("This is index D")
    
    @fy.index      
    def e(): return ft.Text("This is index e")

class F(fy.Route):
    def view(self): return ft.Text("This is index F")
class G(fy.Route):
    class Child1: pass
    def child2(): pass

    class Index:      # only if detect_inner_classes is True
        def view(self): return ft.Text("This is index G")
    def index(self):  # only if detect_method_routes is True
        return ft.Text("This is index g")
    

class X(fy.Route):
    child1 = A
    index = F

ft.run(fy.fly)
```
</details>

<small>**[<font size="1">More About Fallbacks</font>](docs/children.md)**</small>

## 13. Dynamic Routes: Params & Query
- **Flexible Notation:** Dynamic paths are fully supported using three main styles: `:id`, `[id]`, and `{id}`.
- **Visual Tracking:** Dynamic routes are automatically registered in the internal dynamic map and flagged with `[DYN]` on the right side of the printed route tree logs.
- **Data Access:** Route parameters and query strings can be accessed globally via `fy.fly(page).params/.query` and `page.fly.params/.query`.
- **Auto-Injection:** Both params and queries can be accepted directly as named arguments in any `view`, `layout`, or `loader` function.

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

```Python
import flet as ft
import fletfly as fy

class User(fy.Route):
    @fy.child(':id')
    def view(self, id, profile=None, color=None): # 1-through parameters
        return ft.Column([
            ft.Text(f"Argument id: {id}"),
            ft.Text(f"Argument profile: {profile}"),
            ft.Text(f"Argument color: {color}"),
            # 2-through fy.fly(page).params or fy.fly(page).query
            ft.Button("Print fly(page).", on_click=lambda e: print(
                "fly(page).params.get('id'):", fy.fly(e.page).params.get("id"), '\n'
                "fly(page).query.get('profile'):", fy.fly(e.page).query.get("profile"), '\n'
                "fly(page).query.get('color'):", fy.fly(e.page).query.get("color"), '\n'
            )),
            # 3-through page.fly.params or page.fly.query
            ft.Button("Print page.fly.", on_click=lambda e: print(
                "page.fly.params.get('id'):", e.page.fly.params.get("id"), '\n'
                "page.fly.query.get('profile'):", e.page.fly.query.get("profile"), '\n'
                "page.fly.query.get('color'):", e.page.fly.query.get("color"), '\n'
            )),
        ])

def main(page):
    fy.fly(page, 'user/101?profile=premium&color=red')

ft.run(main)
```
</details>

<small>**[<font size="1">More About Fallbacks</font>](docs/dynamic.md)**</small>


## 14. Navigation With `fly(page)` 
### General usage
- Relative Directing according to the current zone, as: fly(page, 'home').
- Absolute Directing according to the root of main zone, as: fly(page, 'home', True).
- Fetches page params & query as: fly(page).params | fly(page).query
### Usage in main function.
- Initiates the core Router engine (if not initiated by `Router()` definition)
- Directing navigation at runtime for each user based on any conditions.

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

```Python
import asyncio
import flet as ft
import fletfly as fy

class Home(fy.Route):
    def view(self):
        return ft.Button('Go Settings', on_click=lambda e: fy.fly(e.page, 'settings'))

class Settings(fy.Route):
    def view(self):
        return ft.Text("Settings Page")

async def main(page):
    # Determine the entry point dynamically per user condition
    if 1 == 1: 
        initial_page = 'home'
    fy.fly(page, initial_page) # Initiate the router

    # force directing in a while
    await asyncio.sleep(5)
    fy.fly(page, 'home')

ft.run(main)
```
</details>

<small>**[<font size="1">More About Fallbacks</font>](docs/fly.md)**</small>


## 15. Redirecting With `fly_to` 
- Redirects Navigation traffic to another route when the current page is matched.

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

```Python
@fy.Route('dashboard', n='Dashboard', fly_to='settings') # overrides fly_to='home'
@fy.Route('error', n='Error', fly_to=None) # overrides fly_to='home'
@fy.Route('about', n='About') # fly_to will still be 'home' as the class
class General:
    fly_to = 'home'    # class level property, for redirecting all routes
    def view(self, n):
        return ft.Text(f"{n} Page")

class Settings(fy.Route):
    def view(self):
        return ft.Text("Settings Page")

class Home(fy.Route):
    def view(self):
        return ft.Text("Home Page")

async def main(page):
    fy.fly(page, 'home')

    targets = ['dashboard', 'error', 'about']
    for t in targets:
        await asyncio.sleep(3)
        fy.fly(page, t)

ft.run(main)
```
</details>

<small>**[<font size="1">More About Fallbacks</font>](docs/fly_to.md)**</small>




## 16. Intelligent Reconciliation & Immediate Disposal
The engine operates on a strict Zero-Waste Component Lifecycle designed to optimize memory footprint and execution speed during high-frequency navigation:

- **Strict Content Reconciliation (No Rebuilding):** If an active layout, view, or shared component is required in the subsequent navigation route, fletfly patches it via reference retention. It never destroys or rebuilds the control from scratch. This guarantees that the underlying Flutter state—including runtime user inputs like text fields, focus, and scroll positions—remains completely intact without manual state saving.

- **Instant Deallocation (Zero Hidden References):** The exact moment a layout or view is dropped from the active navigation stack (and is not explicitly flagged as a persistent hero), fletfly immediately deletes all internal references holding it. The component is instantly exposed to Python's garbage collector (gc), ensuring zero heap accumulation or memory leaks over extended application sessions.

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

```Python
import asyncio
import flet as ft
import fletfly as fy

class Workspace(fy.Route):
    path = "workspace"
    
    def layout(self, page): # Persistent layout: Reconciled and never rebuilt from scratch
        return ft.Column([
            ft.Text("Workspace Shared Layout", size=20, weight="bold"),
            ft.TextField(label="Type here to test state retention"), 
            fy.slot(page)
        ])

    class Profile:
        path = ":id"
        created_count = 0 # Global class counters for explicit memory audit
        destroyed_count = 0

        def __init__(self):
            Workspace.Profile.created_count += 1
            self._print_audit("Born")
            
        def __del__(self):
            Workspace.Profile.destroyed_count += 1
            self._print_audit("Dead")

        def _print_audit(self, event):
            active = Workspace.Profile.created_count - Workspace.Profile.destroyed_count
            try:
                print(f"[Memory Audit] Event: {event:<4} | Created: {Workspace.Profile.created_count:<3} | Destroyed: {Workspace.Profile.destroyed_count:<3} | Active in Heap: {active}")
            except OSError:
                pass # Ignore I/O errors during interpreter shutdown
        def view(self, id):
            return ft.Text(f"Profile Content ID: {id}")

async def main(page):
    fy.fly(page, 'workspace/0')
    await asyncio.sleep(5) # time to type and test retention
    for i in range(1, 50): # Simulating 50 sequential transitions to audit memory stability
        await asyncio.sleep(0.05)
        fy.fly(page, f"workspace/{i}")

ft.run(main)
```
</details>

<small>**[<font size="1">More About Children & Nesting</font>](docs/CHILDREN.md)**</small>

## 17. Every level fallback
- Set your fallback style for any or all levels.
- Define your own overall error page, or let us show our 404.

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

```Python
import flet as ft
import fletfly as fy
class A(fy.Route):      
    def view(self): return ft.Text('Normal class A view')
    class B:
        class C:
            path = ":id"
            def view(self, id, color='black'): return ft.Text(f"{id} page, color is {color}")
        class Fallback: # special fallback for zone C
            path = "*"
            def view(self): return ft.Text('Fallback for B zone')
    @fy.child(path="*") # use path = "*" for fallback
    class Fallback:
        def view(self): return ft.Text('Fallback for A zone')

fy.Router(error_path='a/*')

ft.run(fy.fly)
```
</details>

<small>**[<font size="1">More About Fallbacks</font>](docs/fallback.md)**</small>


## 18. Auto Tree Injection, Deep Nesting.

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

# deep path injects the path directly deep beside his brothers deep in the tree
@fy.Route('a/b/c/d/e/blue', color = 'blue') 
class ColorPage:
    path = ':color'
    def __init__(self, color='green'):
        self.color = color
    def view(self): return ft.Text(f"Color is {self.color}", color=self.color)

# another deep injection
green_page = fy.Route(ColorPage, 'a/b/c/d/e/green',  color = 'green')          # child

class A(fy.Route):
    layout=lambda page: (ft.Text("Layout Header"), fy.slot(page))
    fly_in=lambda: True  # middleware for all descendents)
    class B:
        class C:
            class D:
                class E:    
                    children=[
                        ColorPage       
                        ]
                    child1 = fy.child(ColorPage, 'cyan', color='cyan')
                    child2 = fy.child(ColorPage, 'red', color='red')

fy.Router([A, green_page], print_path_zone='/a/b/c/d/e', ) # print only this branch
async def main(page):
    fy.fly(page)
    target_pages = ['a/b/c/d/e/red', 'a/b/c/d/e/blue', 'a/b/c/d/e/orange',
                    'a/b/c/d/e/cyan', 'a/b/c/d/e/green', 'a/b/c/d/e/yellow']
    for _ in range(1): 
        for p in target_pages:
            await asyncio.sleep(2)
            fy.fly(page, p)
ft.run(main)
```
</details>

<small>**[<font size="1">More About Children & Nesting</font>](docs/CHILDREN.md)**</small>

## 19. Router Configs and Debugs Example
- Set the max views opened in the same time.
- Select the chosen views to build in stack mode.
- Use the builtin routes tree debug, static, dynamic & shared maps debugs.
- Set your fallback style, and error page.
- Use the terminal to follow your router, print a branch only option.
- The terminal in previous section 13 example would look like this:

<details>
<summary><font size="7"><b>👁️ Terminal Example</b></font></summary>

```text
[fletfly Debug] Time taken during [ importing all modules till start of router ]: 0.51ms
[fletfly Debug] Time taken during [ creating initial tree ]: 2.25ms
[fletfly Debug] Time taken during [ parsing static, dynamic & shared nodes maps ]: 0.45ms
-------------------- fletfly -- tree branch ---------------------
─ /a/b/c/d/e/ ─── cls:<E>            view:               ly:               to:                ins: 0  outs: 0 
    │ -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    ├── blue/ ───────── cls:<ColorPage>    view:"view"         ly:               to:                ins: 0  outs: 0  [STC]/a/b/c/d/e/blue
    │ -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    ├── :color/ ─────── cls:<ColorPage>    view:"view"         ly:               to:                ins: 0  outs: 0  [DYN]/a/b/c/d/e/:color
    │ -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    ├── cyan/ ───────── cls:<ColorPage>    view:"view"         ly:               to:                ins: 0  outs: 0  [STC]/a/b/c/d/e/cyan
    │ -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    ├── red/ ────────── cls:<ColorPage>    view:"view"         ly:               to:                ins: 0  outs: 0  [STC]/a/b/c/d/e/red
    │ -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    └── green/ ──────── cls:<ColorPage>    view:"view"         ly:               to:                ins: 0  outs: 0  [STC]/a/b/c/d/e/green
      -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 

--------------------- fletfly -- static map ---------------------
layouts=[0]  view="N/A" fly_to=/a/b/c/d/e/red  path=''
layouts=[1]  view="N/A" fly_to=UNSET  path='/a'
layouts=[1]  view="view" fly_to=UNSET  path='/a/b/c/d/e/blue'
layouts=[1]  view="view" fly_to=UNSET  path='/a/b/c/d/e/cyan'
layouts=[1]  view="view" fly_to=UNSET  path='/a/b/c/d/e/red'
layouts=[1]  view="view" fly_to=UNSET  path='/a/b/c/d/e/green'
-------------------- fletfly -- dynamic map ---------------------
layouts=[1]  view="view" fly_to=UNSET  path='/a/b/c/d/e/:color'
-------------------- fletfly -- shared map ----------------------
-----------------------------------------------------------------
http://127.0.0.1:35615
[fletfly Debug] Time taken during [ triggering initial _handle_route_change by flet ]: 1387.39ms
---------- match path = / ----------
[fletfly] Redirecting by <fly_to> to: path '/a/b/c/d/e/red'
---------- match path = /a/b/c/d/e/red ----------
[fletfly Debug] Time taken during [ navigation preparation for reconciling ]: 1.15ms
[fletfly Debug] Time taken during [ reconciling views ]: 5.49ms
[fletfly Debug] Time taken during [ page update ]: 5.13ms
[fletfly Debug] Active views: 2 ['a', 'red']
[fletfly Debug] Active layouts: 1 ['a']
[fletfly Debug] Active shared views: 0 
[fletfly Debug] Active instances: 1 ['red']
[fletfly Debug] Hero views: 0 
[fletfly Debug] Hero layouts: 0 
[fletfly Debug] Hero shared: 0 
---------- match path = /a/b/c/d/e/blue ----------
[fletfly Debug] Time taken during [ navigation preparation for reconciling ]: 0.97ms
[fletfly Debug] Time taken during [ reconciling views ]: 1.13ms
[fletfly Debug] Time taken during [ page update ]: 2.29ms
[fletfly Debug] Active views: 2 ['a', 'blue']
[fletfly Debug] Active layouts: 1 ['a']
[fletfly Debug] Active shared views: 0 
[fletfly Debug] Active instances: 1 ['blue']
[fletfly Debug] Hero views: 0 
[fletfly Debug] Hero layouts: 0 
[fletfly Debug] Hero shared: 0 
```
</details>

<small>**[<font size="1">More About Configs</font>](docs/CONFIGS.md)**</small>


## 20. Route Copy & Reusability

- **Route Multi-Instantiation:** Reuse the same Route (or class) multiple times across different paths with different properties.
- You can use multiple decorations on the same class, or reference the class multiple times.
- The initiated routes do not have to be at the same level in the tree structure.
- **Strict Memory Isolation:** The engine automatically maintains strict memory isolation between instances. Even when sharing the same class blueprint, each route treats its underlying component as an independent node in the navigation tree with its own distinct lifecycle and state.

<details>
<summary><font size="7"><b>👁️ Code Example</b></font></summary>

```Python
import asyncio
import flet as ft
import fletfly as fy

@fy.Route('blue', color='blue') 
@fy.Route('blue/red', color='red')  # Multi-decoration on the same class
class ColorPage:
    def view(self, color='black'): 
        return ft.Text(f"Color is {color}", color=color)

# Repetition by referencing the class directly
green = fy.Route(ColorPage, 'blue/red/green', color='green') 

# Repetition via copy (shallow copy of a route instance)
cyan = green.copy('blue/red/green/cyan', color='cyan')

async def main(page):
    fy.fly(page)
    target_pages = ['blue', 'blue/red', 'blue/red/green', 'blue/red/green/cyan']
    for p in target_pages:
        await asyncio.sleep(2)
        fy.fly(page, p)

ft.run(main)
```
</details>

<small>**[<font size="1">More About Children & Nesting</font>](docs/CHILDREN.md)**</small>
