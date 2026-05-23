# Class Based Views Attributes

## Runtime Configuration Injection
💡 **Exclusive to CBV:**
Airway CBV is designed to be highly dynamic. Unlike rigid frameworks, we enable Runtime Configuration Injection, giving you full freedom to inject, override, or modify your configurations on the fly without structural limitations.

Our Engine ensures safety: Even though you are free to "play" with attributes, our validation layer monitors every change to keep your application state consistent and crash-free.

📌 **Note:** Runtime changes take effect only upon the next invocation of the `build`, `layout`, or relevant attribute.

⚠️ **Caution:** `path` and `subroutes` (children) are immutable at runtime and require a full router restart to reflect changes.


## Atributes References

### 1. Fixed Attributes
These attributes never change during runtime. They require a complete router startup as the overall static, dynamic, and shared maps depend on them.

| Attribute | Type | Description |
| :--- | :--- | :--- |
| `path` | `str` | The URL or route identifier. |
| `subways` | `list[Airway]` | Child route definitions. |

### 2. Configuration (Static Attributes)
These attributes define the structure, identity, and lifecycle behavior of your route. They must be defined as static class variables.

| Attribute | Type | Description |
| :--- | :--- | :--- |
| `title` | `str` | The display title for the route. |
| `icon` | `str` | The icon associated with the route. |
| `fly_to` | `str` | Target path for redirection. |
| `is_zone` | `bool` | Defines if this route acts as a distinct operational zone. |
| `build_hero` | `bool/int` | Persistence strategy for the build (True/False or cache size). |
| `layout_hero` | `bool/int` | Persistence strategy for the layout (True/False or cache size). |
| `layout_override` | `bool` | Flag to override parent layout. |
| `fly_in_override` | `bool` | Flag to override parent `fly_in` middleware. |
| `fly_out_override` | `bool` | Flag to override parent `fly_out` middleware. |

### 3. Operational (Methods / Hooks)
These attributes define the execution logic. They must be implemented as class methods (`def`).

| Attribute | Expected Type | Description |
| :--- | :--- | :--- |
| `build` | `method` | Returns the view content to be rendered. |
| `layout` | `method` | Returns the layout structure wrapping the view. |
| `fly_in` | `method` | Middleware logic executed before entering the view. |
| `fly_out` | `method` | Middleware logic executed before leaving the view. |
| `post_fly` | `method` | Hook executed after the navigation and build are complete. |

---

> ⚠️ **Engine Validation:**
> The `Airway Engine` inspects these definitions during instantiation. If you attempt to assign an operational method to a configuration attribute, or provide a static value where an operational method is required, the Engine will trigger a validation error to prevent runtime instability.
---

## Attributes Set

