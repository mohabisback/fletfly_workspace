# fletfly
**The Component Composition Engine for Flet.**

"Stop writing procedural routing logic. with `fletfly`, fly with flet."

## 1. quick start

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

## 2. deeper dive
Look at this single block of code. It demonstrates:
- auto detection of routes, nested subroutes.
- auto-path-naming (static & dynamic).
- hierarchical layout inheritance, and final views.
- multi & inheritable middlewares system.
- lazy loading data injection into already opened pages.
- named and nameless slots(outlets) injection.
- auto detection by name, decoration, inheritance and values.
- all can be CBV instance dependent or static.
- index detection (for index using programmers).
- auto arguments manipulation, delivering what's needed including params & query.
- start router with different options.

```python
# docs/class/INTRO/deeper_dive.py
from fletfly import Router, Route, slot, fly, child, data, fly_in, NavigationStyle, Shared
import flet as ft
import asyncio # just for mocking time delay

@Shared('CardDeck2', value='its me everywhere')
@Shared(value='same obj same data') # auto named to 'CardDeck'
class CardDeck(ft.TextField): pass

class Home():                  # Route detection: path auto named to "/home"
    
    def layout(self, page):    # Auto-detected layout by names (layout, frame)
        return ft.Column([
            ft.Text("Header"),
            data(page, ft.Text("loading..."), value="names.0"), # for loader
            slot(page),        # Anonymous slot (auto-injected)
            slot(page, "slot_a"),   # named slot (auto-injected)
            slot(page),        # Anonymous slot (auto-injected)
            slot(page, "CardDeck2", shared=True) # stuck always
        ])
    
    async def loader(self):          # auto detected lazy loader, injects data
        await asyncio.sleep(3)       # mocking delay for data fetching
        return {"names":["John"]}  # called by "names.0"
    
    class Index:               # Auto-detected index
    
        def view(self):        # Auto-detected view by names:
            return (           # (build, content, component, element)
            {"slot_a": ft.Text("Sir")},   # Binds to slot named 'slot_a'
            ft.Text("Hi"),     # Binds to first available nameless slot
            "CardDeck"       # shared view returned as part of view
            )
    
    class _Helper: pass        # Private scope (ignored by router)

    @child(":id")              # Sub route detection, path: "/home/:id"
    class User:
    
        def view(self, page):  # Injected into self or inheritable layout
            return (
                ft.Text(f"{page.fly.params.get('id','default')}"),   # URL params
                {"slot_a":ft.Text(f"{page.fly.query.get('color', 'default')}")}, # URL query
                "CardDeck"   # shared view returned as part of view
            )
    
        @fly_in(inheritable = True, param1='a') # detected by decoration
        @classmethod             # classmethod descriptor auto-unwrapped internally
        def func(cls, param1):
            return True

# handed father of class (or list of fathers of classes)
Router(Home, initial_route = "/home", error_path="/home", every_level_fallback=False, max_views=5, 
       navigation_style=NavigationStyle.home_all_from_last_port, detect_route_subclasses=False, print_debugs=True)

def main(page):
    # your main stuff per user
    fly(page)
ft.run(main)            
```

## 3. Persistent Engine: Intelligent Reconciliation & Hero contents
No matter how many views you are opening in the views stack, and how many navigations you made, you only use 1 instance of each layout, 1 instance of each view or shared view, and you can choose whether to garbage it at the end of its usage or keep it alive by the view_hero & layout_hero options.

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
**[Understand State Persistence & Hero](docs/class/HERO.md)**

## 4. Active Injection with Slots (Outlets)
Slots are in your service not the other way around.
- No limit of slot count
- Named or nameless slots
- free slots or skicked to shared views
- could be any control you want (ft.Container as default)


```python
# under construction
```
**[Understand Layouts Overriding](docs/class/Layout.md)**


## 5. Layout Overrides
Break the inheritance gracefully when you need an isolated view (like a login or settings page) within a nested structure.

```python
# under construction
```
**[Understand Layouts Overriding](docs/class/Layout.md)**

## 6. Multi & Inheritable Middleware System
No matter how many middleware checks You want to perform, we have your back.
- General static or instance dependant.
- Sync or async
- Inheritable or Overrided.
- Applied once or applied each view
- True, False and Redirect str returns

```Python
import flet as ft
from fletfly import Route, fly, fly_in

def check_online():            # general middleware without params
    return True

def check_color(param1):       # general middleware with params
    if param1 == 'c': return True
    else: return False

class Home(Route):
    def view(self): return ft.Text("Main view")
    
    fly_in_override = True         # overrides all parent inheritable middlewares
    def fly_in_self(self, id): # middleware, detected by name
        return True
    
    fly_in_online = check_online  # detected by name, static imported from outside
    
    @fly_in(inheritable = True, param1='a') # detected by decoration
    @classmethod             # classmethod descriptor auto-unwrapped internally
    def func(cls, param1):
        return True

    d = fly_in(check_color, param1='e', param2='b') # detect by value, static

    fly_ins = [check_online] # middleware 5, appended to main list
ft.run(fly)
```
**[Understand fly_in Middleware](docs/class/FLYIN.md)**


## 7. Shared Views
A shared view is a view keeping its state outside the herarchial tree, and can be:
- class dependent or function dependent
- garbaged after end of usage or immortal hero
- stuck into a slot of layout, or delivered as a complete or part of a page view
- created at any place of your app and called everywhere

```Python
# under construction
```
**[Understand Shared](docs/class/SHARED.md)**

## 8. Lazy Loaders & data
Don't keep your users waiting till the data is fetched, open your pages, with default values, use data markers, and fetch your data by loader function.
```Python
# under construction
```
**[Understand Loaders & data](docs/class/LOADER.md)**

## 9. Microfrontend With Zone and page.fly
Add complete projects to your main project, without changing a letter in your code.
Use zone() function and navigate with page.fly, to reach relative paths in your sub projects
```Python
# under construction
```
**[Understand Zone and fly](docs/class/Zone.md)**

## 10. Router Configs and Debugs
- Set the max views opened in the same time
- Select the chosen views to build
- Use the builtin routes tree debug, static, dynamic & shared maps debugs
- Set your fallback style, and error page

```Python
# under construction
```
**[Understand Configs](docs/class/CONFIGS.md)**

## 11. Decorators & Attrs vs Name & value detection
- Deliver you classes to the router, or let the library detect them by inheriting from Router, or @Router decoration
- Let the library detect by name or value your attributes, or strictly state your values throught decorators or methods and attributes
```Python
# under construction
```
**[Understand Auto Detection & Naming](docs/class/AUTO.md)**
