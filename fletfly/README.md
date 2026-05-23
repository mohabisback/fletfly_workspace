# fletfly
**The Component Composition Engine for Flet.**

"Stop writing procedural routing logic. `fletfly` injects data into your builds, nests views and shared components into multi-layered layouts, reconciles the tree, and preserves state—all with built-in middlewares, microfrontend nav and zero boilerplate."

> 💡 **Note:** `fletfly` is polyglot. We designed the engine to adapt to your coding style. The rest of this guide uses **Class-Based Routing** to demonstrate the engine's hierarchical power, but we fully support multiple paradigms. Choose your weapon:
> * [Class-Based Routing](docs/CLASS.md)
> * [Registry/Dictionary Based](docs/DICT.md)
> * [Functional Based](docs/FUNC.md)
> * [Folder/File Based (Next.js style)](docs/FILE.md)

---

## The 20-Line Engine Shock
Look at this single block of code. It demonstrates auto-pathing (static & dynamic), dynamic (nameless) slot injection, and hierarchical layout inheritance—all without a single manual routing string or `page.add()` call.

```python
from fletfly import Airway, slot
import flet as ft

@Airway
class Home:                                  # 1. Auto-path detection ("/home")
    def layout(page):                        # 2. Inheritable layout structure
        return ft.Column([
            ft.Text("Header"),
            slot(page),                      # Injected Content 1
            slot(page),                      # Injected Content 2
            ft.Text("Footer")
        ])
        
    def build(page):                         # 3. Content for "/home"
        return (
            ft.Text("Hi"),                   # Fills Content 1
            ft.Text("Welcome home")          # Fills Content 2
        )

    @Airway(":id")                           # 4. Auto-resolves to "/home/:id"
    class User:
        def build(page):
            # 5. Inherits Home layout automatically!
            return (
                ft.Text("User profile:"),              # Fills Content 1
                ft.Text(f"{page.params['id']}")        # Fills Content 2
            )
```

2. Layout Overrides
Break the inheritance gracefully when you need an isolated view (like a login or settings page) within a nested structure.

```python
    @Airway("settings", layout_override=True)
    class Settings:
        def layout(page):
            # This layout acts as a new root, ignoring the parent's structure
            return ft.Row([slot(page)])

        def build(page):
            return ft.Text("Settings Panel")
```