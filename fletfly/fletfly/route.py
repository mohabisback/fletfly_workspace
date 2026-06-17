from __future__ import annotations
import flet as ft
import re, sys, inspect, asyncio, os, importlib.util, time, builtins
from typing import overload, Callable, Any, Type, Union, TYPE_CHECKING
try:
    from js import console # type: ignore
    _HAS_JS = True
except ImportError:
    _HAS_JS = False
_original_print = builtins.print

def smart_print(*args, **kwargs):
    if _HAS_JS:
        msg = " ".join(map(str, args))
        console.log(msg)
    _original_print(*args, **kwargs)
builtins.print = smart_print


class General:
    # Routes
    _registered_children = set()
    _routed_classes = set()
    _pending_routes = set()
    _pending_shared = set()
    _inherited_classes = set()
    _main_zone_tree = {}
    _shared_routes = {}
    shared_map = {}
    _attr_prefix = "$"
    _zones = []
    _reserved_anchor_modules = set()

    # Router
    initial_route = ""
    auto_path_naming = True
    detect_created_routes = True
    detect_method_routes = True
    detect_method_ordinaries = True
    detect_route_subclasses = True
    detect_inner_classes = True
    print_debugs = True
    _shared_routes = {}
    _router_instance = None

__all__ = ['route', 'fly_ins', 'fly_outs', 'Zone', 'slot', 'data', 'fly', 'fly_around']

_page_err_msg = f"""

🚨 [Core Concept] Why the (page) argument is mandatory:
Flet executes the main(page) function from scratch for every single web user, handing over their exclusive page session. Therefore, you must create a session-related instance for any user-interactive, changeable content.
If you ignore the page argument, User A's actions will affect User B on all levels.
To fix this, you must add your control instances to that specific page or a view on that page. Additionally, any user-level state or variables must be stored within that page session.

fletfly.Router router, depends completely on page sessions to securely support high-level multi-slots in layouts and views with automatic or manual naming.

💡 How we handle sessions together perfectly:
We will pass the (page) argument to your functions, and we expect you to pass it back inside slot(page). This ensures every user gets an isolated instance. Example:
def layout(page):
    return ...your design... slot(page, 'slot_name') ... slot(page, 3)  ...your design...
           ...your design... slot(page) ...slot(page, 'shared_1', ft.Card(), True)...your design...
              (auto-named to 10000001)^                                    ^ (True=Stick to 'shared_1')
"""
aliases = {
    "path": ["path", "url", "route"],
    "view_hero": [ "view_hero", "build_hero", "component_hero", "element_hero", "contents_hero", "controls_hero",],
    "view": [ "view", "build", "viewer", "component", "element", "contents", "controls",],
    "fly_ins": ["fly_ins"],
    "fly_in_override": ["fly_in_override", "loader_override", "canActivate_override", "beforeEnter_override", "middleware_override", "beforeLoad_override",],
    "fly_in": ["fly_in", "canActivate", "beforeEnter", "middleware", "beforeLoad",],
    "fly_out_override": ["fly_out_override", "canDeactivate_override", "beforeUnload_override",],
    "fly_outs": ["fly_outs"],
    "fly_out": ["fly_out", "canDeactivate", "beforeUnload",],
    "layout_override": ["layout_override", "frame_override",],
    "layout_hero": ["layout_hero", "hero_frame",],
    "layout": ["layout", "frame",],
    "fly_to": ["fly_to", "redirect", "redirectTo",],
    "title": ["title", ],
    "icon": ["icon", "logo",],
    "children": ["children", "subroutes", "routes", "screens", "subs"],
    "child": ["child", "subroute", "sub"],
    "index": ["index", "default"],
    "fly_around": ["fly_around", "shared", "shared_view"],
    "loader": ["loader", "binder", "hydrator"],
    "name":["name"],
    "hero":["hero"]
}
_rev_aliases = {val:k for k in aliases.keys() for val in aliases.get(k)}

def _is_flet_instance(value, or_class = False) -> bool:

    if not or_class and isinstance(value, type): return False

    cls = value if isinstance(value, type) else type(value)
        
    if issubclass(cls, ft.Control):
        return True
        
    return False

def _call_with_payload(func, page, availables: list[dict], params=True, query=True):
    if availables is None: availables = []
    elif isinstance(availables, dict): availables = [availables]
    payload = _get_set_payload(func) 
    if not payload:
        try:
            return func()
        except TypeError as e:
            # Catching TypeError only to prevent hiding real bugs inside func
            if "argument" in str(e) or "takes" in str(e):
                return func(page)
            raise

    merged_data = {}
    for data in availables + ([page.fly.params] if params else []) + ([page.fly.query] if query else []):
        if data:
            for k, v in data.items():
                if k not in merged_data:
                    merged_data[k] = v
    run_args = {}
    is_bound = hasattr(func, "__self__")
    for i, (key, val) in enumerate(payload["params"].items()):
        if is_bound and i == 0: continue # pass self & cls

        if key == "page" and val is True:
            run_args["page"] = page
            continue
            
        if key in merged_data:
            run_args[key] = merged_data[key]
        elif val != "_fletfly":
            run_args[key] = val
        else:
            raise ValueError(f"[fletfly] Missing required argument: '{key}' for func: <{getattr(func, "__name__", type(func).__name__)}>.")
            
    if payload.get("kwargs", False):
        for k, v in merged_data.items():
            if k not in run_args:
                run_args[k] = v
    
    try:
        return func(**run_args)
    except TypeError as e:
        if "argument" in str(e) or "takes" in str(e):
            func_name = getattr(func, "__name__", type(func).__name__)
            raise TypeError(f"[fletfly] {e} - maybe you forgot 'self' or 'cls' parameter in <{func_name}>?") from e
        raise

def _get_set_payload(func) -> dict | None:
    bare_func = getattr(func, "__func__", func)
    payload = getattr(bare_func, "_payload_fletfly", None)
    if payload is not None:
        return payload    
        
    if not inspect.isfunction(bare_func) and not inspect.isclass(bare_func) and not inspect.ismethod(bare_func): return
        
    try:
        params = list(inspect.signature(bare_func).parameters.values())
    except (ValueError, TypeError) as e:
        print(f"[fletfly] Can't get function payload, because of error:", e)
        return None

    payload = {"params":{}, "kwargs":False}
    # If the handler is a class and hasn't overridden object.__init__,
    # bypass parameter validation to avoid inheriting (*args, **kwargs) from object.

    if isinstance(bare_func, type) and (bare_func.__init__ == object.__init__ or bare_func.__init__ == Route.__init__):
        params = []
    for p in params:
        # Reject *args and positional-only arguments
        if p.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.VAR_POSITIONAL):
            raise ValueError(f"[fletfly] Positional-only arguments and *args are not allowed in route handlers: '{p.name}'")
            
        # View the flat payload
        if p.kind == inspect.Parameter.VAR_KEYWORD:
            payload["kwargs"] = True
        elif p.name == "page":
            payload["params"]["page"] = True
        elif p.default != inspect.Parameter.empty:
            payload["params"][p.name] = p.default
        else:
            payload["params"][p.name] = "_fletfly"
            
    try:
        bare_func._payload_fletfly = payload
    except AttributeError:
        pass    
        
    return payload

class _FuncDict(dict):
    def __init__(self, func, name:str, props:dict=None):
        super().__init__({"func": func, "name": name, "props": props if props else {}})

class _MethodHandler:
    set_type = "_"
    expected_func = "func"
    expected = {"props":(dict, {})}
    def __init__(self, value=None, ctx=None):
        self.value = value
        self.ctx = ctx
    def __get__(self, instance, owner):
        if instance is None: return self
        # Fetch the current actual value from the instance
        val = getattr(instance, self.set_name, self.value)
        # Return a new wrapper instance holding the value and context
        return self.__class__(value=val, ctx=instance)
    # Emulation methods
    def __getitem__(self, key):
        if isinstance(self.value, dict):
            return self.value[key]
        raise TypeError(f"'{type(self.value).__name__}' object is not subscriptable")
    def __contains__(self, item):
        if isinstance(self.value, dict):
            return item in self.value
        return False
    def get(self, key, default=None):
        if isinstance(self.value, dict):
            return self.value.get(key, default)
        return default
    def __eq__(self, other):
        return self.value == other
    def __str__(self):
        return str(self.value)
    def __repr__(self):
        return repr(self.value)

    def __set__(self, instance, value):
        if instance is not None:
            if self.set_type == "list":
                if self.name == "fly_in":
                    instance.fly_ins.append(value)
                elif self.name == "fly_out":
                    instance.fly_outs.append(value)
                elif self.name == "child":
                    instance.children.append(value)
            else:
                final_val = None
                if value is None: pass
                else:
                    if getattr(instance, self.set_name, None) is not None:
                        print(f"[fletfly] WARNING: second re-setting of {self.name} for route route '{instance.path}'.")
                    if self.name == "index":
                        idx = self._child_item(value)
                        if idx:
                            idx.path = ""
                            final_val = idx
                    else:
                        final_val = self._func_item(value)
                setattr(instance, self.set_name, final_val)
    
    def _get_expected_and_props(self, kwargs):
        not_expected = dict(kwargs)
        expected = {}
        self_expected = (self.expected | _MethodHandler.expected)
        for item in kwargs:
            if item in self_expected:
                expected_type = self_expected[item][0]
                if kwargs[item] is not None and not isinstance(kwargs[item], expected_type):
                    raise TypeError(f"[fletfly] Argument '{item}' must be of type {expected_type.__name__}")
                not_expected.pop(item)
                self_expected.pop(item)
                expected[item] = kwargs[item]
        for item in self_expected: # remaining expected items
            if self_expected[item][1] is not None:
                expected[item] = self_expected[item][1]

        for special in ["hero", "override"]:
            val = expected.pop(special, "not there")
            if val != "not there":
                expected[f"{self.name}_{special}"] = val
        
        props = (expected.pop("props", {})or{}) | not_expected
                           
        return expected, props
    
    def _child_route_from_callable(self, clbl):
        route = Route()
        General._pending_routes.discard(route)
        if isinstance(clbl, type):
            route._class = clbl
        else:
            route.view = _FuncDict(func=clbl, name="view")
        return route

    def _child_item(self, item):
        if item is None: return None
        if isinstance(item, Route):
            return item
        elif callable(item):
            _get_set_payload(item)
            return self._child_route_from_callable(item)
        elif isinstance(item, (tuple, list)):
            if len(item) == 2 and callable(item[0]) and isinstance(item[1], dict):
                _get_set_payload(item[0])
                way = self._child_route_from_callable(item[0])
                way.props.update(item[1])
                return way
            else:
                raise TypeError(f"[fletfly] Positional arguments are not allowed to pass {self.name} arguments, named arguments only.\n"+
                                f"Use <{self.name}> method as: my_route.{self.name}(callable, role='user', color='red') or\n"+
                                f"Use <{self.name}> function as: my_route.{self.name} = {self.name}(callable, role='user', color='red') or\n"+
                                f"Use tuple of callable and dict as: my_route.{self.name.rstrip('s')} = (callable, {'role':'user', 'color':'red'}) or\n"+
                                f"Append into a list as: my_route.{self.name}s.extend(callable1, (callable2, dict), {self.name}(callable, a=1))")
        else:
            raise TypeError(f"❌ [fletfly] Expected Route | callable | (callable, props_dict) tuple | list of any of the above, but got '{type(item).__name__}'")
    
    def _get_func_dict(self, func, expected_not):
        _get_set_payload(func)
        final_dic = _FuncDict(func=func, name=self.name)
        expected, props = self._get_expected_and_props(expected_not if expected_not else {})
        final_dic["props"] = props
        if "inheritable" in expected: final_dic["inheritable"] = expected.pop("inheritable", None)
        if "apply_per_view" in expected: final_dic["apply_per_view"] = expected.pop("apply_per_view", None)
        final_dic.update(expected)
        return final_dic
    
    def _func_item(self, item):
        if item is None: return None
        elif isinstance(item, _FuncDict):
            return item
        elif callable(item) or isinstance(item, str):
            _get_set_payload(item)
            return self._get_func_dict(item, {})
        elif isinstance(item, (tuple, list)):
            if len(item) == 2 and (callable(item[0]) or isinstance(item[0], str)) and isinstance(item[1], dict):
                return self._get_func_dict(item[0], item[1])
            else:
                raise TypeError(f"[fletfly] Positional arguments are not allowed to pass {self.name} arguments, named arguments only.\n"+
                                f"Use <{self.name}> method as: my_route.{self.name}(callable, role='user', color='red') or\n"+
                                f"Use <{self.name}> function as: my_route.{self.name} = {self.name}(callable, role='user', color='red') or\n"+
                                f"Use tuple of callable and dict as: my_route.{self.name.rstrip('s')}"+" = (callable, {'role':'user', 'color':'red'}) or\n"+
                                f"Append into a list as: my_route.{self.name}s.extend(callable1, (callable2, dict), {self.name}(callable, a=1))")
        else:
            raise TypeError(f"❌ [fletfly] Expected _FuncDict | callable | (callable, props_dict) tuple | list of any of the above, but got '{type(item).__name__}'")
    
    def _pre_process_core(self, *args, **kwargs):
        no_decorator = False
        expected = self.expected | _MethodHandler.expected
        keys = list(expected.keys())
        func = None
        config = {}
        if args:
            if callable(args[0]):
                if self.expected_func in kwargs:
                    raise ValueError(f"[fletfly] Can't have 2 '{self.expected_func}' in arguments")
                func = args[0]
                remaining_args = args[1:]
            elif len(args)> 1 and callable(args[1]):
                if self.expected_func in kwargs:
                    raise ValueError(f"[fletfly] Can't have 2 '{self.expected_func}' in arguments")
                func = args[1]
                remaining_args = (args[0], *args[2:])
            else:
                if self.expected_func in kwargs:
                    raise ValueError(f"[fletfly] Cannot pass positional arguments when '{self.expected_func}' is provided as a keyword argument.")
                remaining_args = args
        else:
            func = kwargs.pop(self.expected_func, None)
            if func is not None and not callable(func):
                raise ValueError(f"[fletfly] Argument '{self.expected_func}' must be callable.")
            remaining_args = ()
        if func and (remaining_args or kwargs): no_decorator = True
        
        # get not bounded bare func
        func = getattr(func, "__func__", func)

        if len(remaining_args) > len(keys):
            raise ValueError(f"[fletfly] Function expected {len(keys)} arguments but got {len(remaining_args)}")    
        for i, val in enumerate(remaining_args):
            key = keys[i]
            expected_type = expected[key][0]  # Get type from tuple
            
            if key in kwargs:
                raise ValueError(f"[fletfly] Can't have 2 '{key}' in arguments")
            
            if val is not None and not isinstance(val, expected_type):
                
                raise TypeError(f"[fletfly] Argument '{expected_type}' must be of type {expected_type.__name__}")
            
            config[key] = val

        config.update(kwargs)

        return self._process_core(func, config, no_decorator)

    def _process_core(self, first_arg, config_args: dict, direct_call_with_args):
        _fletfly_= "_fletfly_"

        config_args = dict(config_args) if config_args else {}

        instance = None if self.ctx is None or isinstance(self.ctx, type) else self.ctx

        def _inject_func_into_route(route, wrapped_func):
            if self.set_type == "list":
                getattr(route, self.set_name).append(wrapped_func)               # add function to route list
            else:
                old_func = getattr(route, self.set_name, None)
                if isinstance(old_func, _FuncDict):
                    old_func = old_func["func"]
                new_func = wrapped_func["func"] if isinstance(wrapped_func, _FuncDict) else wrapped_func
                
                if old_func and old_func != new_func:
                    raise ValueError(f"[fletfly] Route route already has a {self.name} function")
                else:
                    setattr(route, self.set_name, wrapped_func)
            return route
        
        def _inject_details_into_route(route, expected_kwargs):
            for key, val in expected_kwargs.items():
                if val is not None:
                    setattr(route, key, val)
            return route

        def _inject_child_parents(route, kwargs):
            parents = list(kwargs.get("parents") or [])
            parents += [instance] if instance else []
            if parents:
                for parent in parents:
                    if isinstance(parent, Route): 
                        parent.children.append(route)   # append the class to the route instance
                    elif isinstance(parent, type):
                        _fletfly_children="_fletfly_children"
                        if not hasattr(parent, _fletfly_children):
                            setattr(parent, _fletfly_children, set())
                        getattr(parent, _fletfly_children, set()).add(route)
                    else:
                        raise ValueError(f"[fletfly] Only type Route (route) or class is allowed as parent.")
        
        def _index_child(route, kwargs):
            if self.name == "index":
                route.path = ""
                if instance:
                    setattr(instance, self.set_name, route)
            else:
                _inject_child_parents(route, kwargs)
            return route
        
        def _child_from_class(clas, kwargs):
            route = Route()
            route._class=clas
            General._pending_routes.discard(route)
            expected, props = self._get_expected_and_props(kwargs)
            route.props.update(props)
            _inject_details_into_route(route, expected)
            return _index_child(route, kwargs)
        
        def _child_from_func(func, kwargs):
            route = Route()
            General._pending_routes.discard(route)
            wrapped = self._get_func_dict(func, kwargs)
            expected, props = self._get_expected_and_props(kwargs)
            route.view = wrapped
            route.props.update(props)
            _inject_details_into_route(route, expected)
            return _index_child(route, kwargs)
        
        def _child_from_args(kwargs):
            route = Route()
            General._pending_routes.discard(route)
            expected, props = self._get_expected_and_props(kwargs)
            route.props.update(props)
            _inject_details_into_route(route, expected)
            return _index_child(route, kwargs)
        
        def _special_from_class(clas, kwargs):
            if instance: raise ValueError(f"[fletfly] Can't use {self.name}(class), a class can't be converted to a {self.name}. functions and methods only.")
            route = Route()
            route._class=clas
            expected, props = self._get_expected_and_props(kwargs)
            route.props.update(props)
            _inject_details_into_route(route, expected)
            return route
        
        def _set_func_as_mine(func, kwargs):
            expected, _ = self._get_expected_and_props(kwargs)
            wrapped_func = self._get_func_dict(func, kwargs)
            _inject_func_into_route(instance, wrapped_func)
            _inject_details_into_route(instance, expected)
            return instance
        
        def _set_details_for_my_next(kwargs):
            expected, props = self._get_expected_and_props(kwargs)
            setattr(instance, f"_fletfly_waiting_{self.set_name}", props)
            _inject_details_into_route(instance, expected)
            return instance
        
        def _inject_details_into_class_or_method(class_or_func, kwargs):
            expected, props = self._get_expected_and_props(kwargs)
            dic = {"props": props}
            for key, val in expected.items():
                if val is not None:
                    dic[key] = val
            lis = getattr(class_or_func, _fletfly_ + self.name, None)
            if lis is None:
                lis = []
                setattr(class_or_func, _fletfly_ + self.name, lis)
            lis.append(dic)

        dec = "_fletfly_decorated"
        if isinstance(first_arg, type):
            _get_set_payload(first_arg)
            if direct_call_with_args:
                if self.name in ("child", "index"):
                    if instance:
                        # 1.1.0) obj.child(class, 'user', parents=[] ) # CB route + inject, -> obj
                        return _child_from_class(first_arg, config_args) # handles inject into parents if any.
                    else:
                        # 1.0.0) child(class,'user', parents=[]) # CB route + inject -> obj
                        return _child_from_class(first_arg, config_args) # handles inject into parents if any.
                elif self.name in ("layout", "view", "fly_in", "fly_out", "loader"):
                    if instance:
                        # 2.1.0) obj.layout(class, 'user') # ->                       # Chaining -> instance
                        _set_func_as_mine(first_arg, config_args)
                        return instance
                    else:                     
                        # 2.0.0) layout(class, 'user') # CB route (special) -> dict   # direct
                        return self._get_func_dict(first_arg, config_args)
            else:      
                if instance:
                    setattr(instance, dec, first_arg)
                    # 1.1.1) obj.child(class)=@obj.child/class # CB route+inject+MCA -> class
                    if self.name in ("child", "index"):
                        _child_from_class(first_arg, {}) # handles inject into parents if instance
                    elif self.name in ("layout", "view", "fly_in", "fly_out", "loader"):
                    # 2.1.1) obj.layout(class)=@obj.layout/class # -> Ambiguous, ValueError
                        _set_func_as_mine(first_arg, {})
                        return instance
                else:
                    # 1.0.1) child(class)=@child/class # CB route + MCA child-> class
                    # 2.0.1) layout(class)=@layout/class # CB route (special) MCA child-> class
                    _inject_details_into_class_or_method(first_arg,{})
                return first_arg         
        # decorating a func or method without calling @layout | @Route.layout | @route.layout:
        elif callable(first_arg):
            _get_set_payload(first_arg)
            if direct_call_with_args:
                if self.name in ("child", "index"):
                    if instance:
                        # 1.3.0)obj.child(func, 'user', parents=[]) # FIB route + inject, -> obj
                        return _child_from_func(first_arg, config_args)
                    else:
                        # 1.2.0)child(func, 'user', parents=[]) # FIB route + inject-> obj, 
                        return _child_from_func(first_arg, config_args)
                elif self.name in ("layout", "view", "fly_in", "fly_out", "loader"):
                    # 2.3.0)obj.layout(func, 'user') # set method as mine -> obj
                    if instance:
                        _set_func_as_mine(first_arg, config_args)
                        return instance
                    # 2.2.0)layout(func, 'user') # dict -> dict, 
                    else:
                        return self._get_func_dict(first_arg, config_args)
            else:             
                if instance:
                    setattr(instance, dec, first_arg)
                    if self.name in ("child", "index"):
                        # 1.3.1)obj.child(func)=@obj.child/func # FIB route+inject+MMA -> func
                        return _child_from_func(first_arg, {})    
                    elif self.name in ("layout", "view", "fly_in", "fly_out", "loader"):
                        # 2.3.1)obj.layout(func)=@obj.layout/func # set method as mine & MMA me -> func
                        return _set_func_as_mine(first_arg, {})
                else:
                    # 1.2.1)child(func)=@child/func # MMA child-> func,
                    # 2.2.1)layout(func)=@layout/func # MMA me-> func, 
                    _inject_details_into_class_or_method(first_arg, {})    
                return first_arg
        
        elif instance and self.name in ("child", "index"):
            # 1.1.2)@obj.child(parents=[], 'user')/class or obj.child("user") # CB route+inject+MCA -> class
            # 1.3.2)@obj.child(parents=[], 'user')/func or obj.child("user) # FIB route+inject+MMA -> func
            return _child_from_args(config_args)
                
        else:
            def wrapper(func_or_class):
                if instance:
                    setattr(instance, dec, func_or_class)
                # get real function not bounded by @classmethod or shit
                func_or_class = getattr(func_or_class, "__func__", func_or_class)
                _get_set_payload(func_or_class)
                _inject_details_into_class_or_method(func_or_class, config_args)
                if isinstance(func_or_class, type):
                    # 1.0.2) @child(parents=[], 'user')/class # CB route+inject+ MCA child, -> class
                    if self.name in ("child", "index"):
                        _child_from_class(func_or_class, config_args)
                    # 2.0.2)@layout('user')/class # CB route (special) + MCA child -> class
                    
                    elif self.name in ("layout", "view", "fly_in", "fly_out", "loader"):
                        _special_from_class(func_or_class, config_args) # handles error if instance    
                        if instance:
                            # 2.1.2)@obj.layout('user')/class or obj.layout("user") # -> Ambiguous, ValueError
                            _set_func_as_mine(func_or_class, config_args)
                else:
                    # 1.2.2)@child(parents=[], 'user')/func # FIB route+inject+MMA -> func
                    if self.name in ("child", "index"):
                        _child_from_func(func_or_class, config_args)
                    elif self.name in ("layout", "view", "fly_in", "fly_out", "loader"):
                        # 2.2.2)@layout('user')/func # MMA me, -> func
                        if instance:
                            # 2.3.2)@obj.layout('user')/func or obj.layout("user"), # set method as mine & MMA me -> obj
                            _set_func_as_mine(func_or_class, config_args)
                return func_or_class
            return wrapper

obj = Route()
@obj.layout
def func(): pass

obj.layout()


class _Layout(_MethodHandler):
    name = "layout"
    set_name = "_layout"
    expected = {"hero": (bool, None), "override": (bool, None)}
    def __get__(self, instance, owner):
        return super().__get__(instance, owner)
    def __call__(self, *args, **kwargs):
        """1/2 Decorator, as: @layout(True, False)\n\n2/2 Direct call, as: layout(my_func, par1=arg1, par2=arg2)"""
        return self._pre_process_core(*args, **kwargs)

class _View(_MethodHandler):
    name = "view"
    set_name = "_view"
    expected = {"hero": (bool, None)}
    @overload
    def __call__(self, hero: bool = None, props:dict=None, **kwargs:Any) -> Callable[[Union[Type[Any], Callable[..., Any]]], Any]: ...
    @overload
    def __call__(self, func: Callable[..., Any], hero: bool = None, props:dict=None, **kwargs: Any) -> Any: ...
    def __call__(self, *args, **kwargs):
        """1/2 Decorator, as: @view(True)\n\n2/2 Direct call, as: view(my_func, par1=arg1, par2=arg2)"""
        return self._pre_process_core(*args, **kwargs)

class _Loader(_MethodHandler):
    name = "loader"
    set_name = "_loader"
    expected = {}
    @overload
    def __call__(self, props:dict=None, **kwargs:Any) -> Callable[[Union[Type[Any], Callable[..., Any]]], Any]: ...
    @overload
    def __call__(self, func: Callable[..., Any], props:dict=None, **kwargs: Any) -> Any: ...
    def __call__(self, *args, **kwargs):
        """1/2 Decorator, as: @loader(True)\n\n2/2 Direct call, as: loader(my_func, par1=arg1, par2=arg2)"""
        return self._pre_process_core(*args, **kwargs)
    
class _FlyIn(_MethodHandler):
    name = "fly_in"
    set_name = "fly_ins"
    set_type = "list"
    expected = {"inheritable": (bool, True), "apply_per_view": (bool, False), "override": (bool, None)}
    @overload # Func decorator
    def __call__(self, inheritable: bool = True, apply_per_view: bool = False, props:dict=None, **kwargs:Any) -> Callable[[Union[Type[Any], Callable[..., Any]]], Any]: ...
    @overload # Class decorator
    def __call__(self, override: bool = None, props:dict=None, **kwargs:Any) -> Callable[[Union[Type[Any], Callable[..., Any]]], Any]: ...
    @overload # Func call
    def __call__(self, func: Callable[..., bool|str], inheritable: bool = True, apply_per_view: bool = False, props:dict=None, **kwargs: Any) -> Any: ...
    @overload # Class call
    def __call__(self, cls: Callable[..., bool|str], override: bool = False, props:dict=None, **kwargs:Any) -> Any: ...
    def __call__(self, *args, **kwargs):
        """1-2 /4 Func | Class decorator, as: @fly_in(True)\n\n
        2-3 /4 Func | Class call, as: fly_in(my_func, True)"""
        if "cls" in kwargs: kwargs = {"func": kwargs.pop("cls"), **kwargs}
        return self._pre_process_core(*args, **kwargs)

class _FlyOut(_MethodHandler):
    name = "fly_out"
    set_name = "fly_outs"
    set_type = "list"
    expected = {"inheritable": (bool, False), "apply_per_view": (bool, False), "override": (bool, None)}
    @overload # Func decorator
    def __call__(self, inheritable: bool = False, apply_per_view: bool = False, props:dict=None, **kwargs:Any) -> Callable[[Union[Type[Any], Callable[..., Any]]], Any]: ...
    @overload # Class decorator
    def __call__(self, override: bool = None, props:dict=None, **kwargs:Any) -> Callable[[Union[Type[Any], Callable[..., Any]]], Any]: ...
    @overload # Func call
    def __call__(self, func: Callable[..., bool|str], inheritable: bool=False, apply_per_view: bool=False, props:dict=None, **kwargs: Any) -> Any: ...
    @overload # Class call
    def __call__(self, cls: Callable[..., bool|str], override: bool=False, props:dict=None, **kwargs:Any) -> Any: ...
    def __call__(self, *args, **kwargs):
        """1-2 /4 Func | Class decorator, as: @fly_out(True)\n\n
        2-3 /4 Func | Class call, as: fly_out(my_func, True)"""
        if "cls" in kwargs: kwargs = {"func": kwargs.pop("cls"), **kwargs}
        return self._pre_process_core(*args, **kwargs)

class _Child(_MethodHandler):
    name = "child"
    set_name = "children"
    set_type = "list"     
    expected = {"path": (str,None), "parents": (list,None),
                "view": (object,None), "children": (list,None),
                "fly_to": (str,None), "layout": (object, None), "layout_override": (bool,None),
                "fly_ins":(list, None), "fly_in_override": (bool,None),
                "fly_outs":(list, None), "fly_out_override": (bool,None),
                "is_zone": (bool,None), "view_hero": (bool,None), "layout_hero": (bool,None),
                "title": (str,None), "icon": (str,None), "loader":(object,None)}
    @overload # Decorator on a function
    def __call__(self,
                 path:str=None, parents:list[Route|type]=None,
                 children:list[Route]=None,
                 fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 is_zone:bool=None, view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any 
                 ) -> Callable[[Union[Type[Any], Callable[..., Any]]], Any]: ...
    @overload # Decorator on a class
    def __call__(self,
                 path:str=None, parents:list[Route|type]=None,
                 view=None, children:list[Route]=None,
                 fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 is_zone:bool=None, view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any
                 ) -> Callable[[Union[Type[Any], Callable[..., Any]]], Any]: ...
    @overload # Direct call with function
    def __call__(self, func: Callable[..., bool|str],
                 path:str=None, parents:list[Route|type]=None,
                 children:list[Route]=None,
                 fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 is_zone:bool=None, view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any)-> Any: ...

    @overload # Direct call with a class
    def __call__(self, cls: type,
                 path:str=None, parents:list[Route|type]=None,
                 view=None, children:list[Route]=None,
                 fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 is_zone:bool=None, view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any) -> Any: ...
    def __call__(self, *args, **kwargs):
        """1-2 /4 func | class decorator: @child('home', [clsA, clsB])
        \n\n3-4 /4 func | class call, as: child(cls1, 'user', par1=arg1)"""
        if "cls" in kwargs: kwargs = {"func": kwargs.pop("cls"), **kwargs}
        return self._pre_process_core(*args, **kwargs)

class _Index(_MethodHandler):
    name = "index"
    set_name = "_index"
    expected = {"view": (object,None),
                "fly_to": (str,None), "layout": (object, None), "layout_override": (bool,None),
                "fly_ins":(list, None), "fly_in_override": (bool,None),
                "fly_outs":(list, None), "fly_out_override": (bool,None),
                "is_zone": (bool,None), "view_hero": (bool,None), "layout_hero": (bool,None),
                "title": (str,None), "icon": (str,None), "loader":(object,None)}
    @overload # Decorator on a function
    def __call__(self, fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 is_zone:bool=None, view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any 
                 ) -> Callable[[Union[Type[Any], Callable[..., Any]]], Any]: ...
    @overload # Decorator on a class
    def __call__(self, view=None, fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 is_zone:bool=None, view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any
                 ) -> Callable[[Union[Type[Any], Callable[..., Any]]], Any]: ...
    @overload # Direct call with function
    def __call__(self, func: Callable[..., bool|str],
                 fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 is_zone:bool=None, view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any)-> Any: ...
    @overload # Direct call with a class
    def __call__(self, cls: type, view=None,
                 fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 is_zone:bool=None, view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any) -> Any: ...
    def __call__(self, *args, **kwargs):
        """1-2 /4 func | class decorator: @index('home', [clsA, clsB])
        \n\n3-4 /4 func | class call, as: index(cls1, 'user', par1=arg1)"""
        if "cls" in kwargs: kwargs = {"func": kwargs.pop("cls"), **kwargs}
        return self._pre_process_core(*args, **kwargs)

class _StrAttr(str):
    def __new__(cls, name: str, value=None, ctx=None):
        # Pass a string representation to str.__new__
        str_val = "None" if value is None else str(value)
        return str.__new__(cls, str_val)
    def __init__(self, name: str, value=None, ctx=None):
        self.name = name
        self.set_name = f"_{name}"
        self.value = value
        self.ctx = ctx
    def __get__(self, instance, owner):
        if instance is None:
            return self
        # Read from the internal variable
        val = getattr(instance, self.set_name, self.value)
        # Return the hybrid string object to support both regex and chaining
        return self.__class__(self.name, value=val, ctx=instance)
    def __set__(self, instance, value):
        if instance is not None:
            # Store None directly, otherwise store as string
            actual_val = value if value is None else str(value)
            setattr(instance, self.set_name, actual_val)
    def __call__(self, value=None):
        # Store None directly, otherwise store as string
        actual_val = value if value is None else str(value)
        if instance := self.ctx:
            setattr(instance, self.set_name, actual_val)
            return instance
        return actual_val

class _BoolAttr:
    def __init__(self, name: str, value=None, ctx=None):
        self.name = name
        self.set_name = f"_{name}"
        self.value = value  
        self.ctx = ctx
    def __get__(self, instance, owner):
        if instance is None:
            return self
        val = getattr(instance, self.set_name, self.value)
        # Return a new wrapper instance with the current value and context
        return self.__class__(self.name, value=val, ctx=instance)
    def __set__(self, instance, value):
        if instance is not None:
            actual_val = value if value is None else bool(value)
            setattr(instance, self.set_name, actual_val)
    def __call__(self, value=None):
        actual_val = value if value is None else bool(value)
        if instance := self.ctx:
            setattr(instance, self.set_name, actual_val)
            return instance
        return actual_val
    def __bool__(self):
        return bool(self.value)
    def __str__(self):
        return str(self.value)
    def __repr__(self):
        return str(self.value)
    def __eq__(self, other):
        if isinstance(other, bool):
            return bool(self) == other
        return self.value == other

class _HeroAttr:
    def __init__(self, name: str, value=None, ctx=None):
        self.name = name
        self.set_name = f"_{name}"
        self.value = value  
        self.ctx = ctx
    def __get__(self, instance, owner):
        if instance is None:
            return self
        val = getattr(instance, self.set_name, self.value)
        # Return a new wrapper instance with the current value and context
        return self.__class__(self.name, value=val, ctx=instance)
    def __set__(self, instance, value):
        if instance is not None:
            setattr(instance, self.set_name, value)
    def __call__(self, value=None):
        if instance := self.ctx:
            setattr(instance, self.set_name, value)
            return instance
        return value
    def __bool__(self):
        return bool(self.value)
    def __str__(self):
        return str(self.value)
    def __repr__(self):
        return str(self.value)
    def __eq__(self, other):
        if isinstance(other, (bool, int)):
            return int(self.value or 0) == int(other)
        return self.value == other
    def __int__(self):
        return int(self.value or 0)

class _DictAttr(dict):
    def __init__(self, name: str, value=None, ctx=None):
        # Convert None to an empty dictionary as the default initial state
        dict_val = {} if value is None else dict(value)
        super().__init__(dict_val)
        self.name = name
        self.set_name = f"_{name}"
        self.value = dict_val
        self.ctx = ctx
    def __get__(self, instance, owner):
        if instance is None:
            return self       
        # Read from internal variable, fallback to current value (empty dict)
        val = getattr(instance, self.set_name, self.value)        
        # Ensure internal None is treated as an empty dictionary
        val = {} if val is None else val
        return self.__class__(self.name, value=val, ctx=instance)
    def __set__(self, instance, value):
        if instance is not None:
            # Always store as dict, convert None to empty dict
            actual_val = {} if value is None else dict(value)
            setattr(instance, self.set_name, actual_val)
    def __call__(self, value=None):
        # Always store as dict, convert None to empty dict
        actual_val = {} if value is None else dict(value)
        if instance := self.ctx:
            setattr(instance, self.set_name, actual_val)
            return instance
        return actual_val
    def _sync_back(self):
        """Keeps the internal raw dict in sync with wrapper mutations."""
        if self.ctx is not None:
            setattr(self.ctx, self.set_name, dict(self))
    def clear(self):
        super().clear()
        self._sync_back()
    def pop(self, key, *args):
        val = super().pop(key, *args)
        self._sync_back()
        return val
    def popitem(self):
        val = super().popitem()
        self._sync_back()
        return val
    def setdefault(self, key, default=None):
        val = super().setdefault(key, default)
        self._sync_back()
        return val
    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self._sync_back()
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._sync_back()
    def __delitem__(self, key):
        super().__delitem__(key)
        self._sync_back()
    def __ior__(self, other):
        # Support for the |= operator (Python 3.9+)
        res = super().__ior__(other)
        self._sync_back()
        return res

class _ListAttr(list):
    def __init__(self, name: str, value=None, ctx=None):
        # Convert None to an empty list as the default initial state
        list_val = [] if value is None else list(value)
        super().__init__(list_val)
        self.name = name
        self.set_name = f"_{name}"
        self.value = list_val
        self.ctx = ctx
    def __get__(self, instance, owner):
        if instance is None:
            return self
        # Read from internal variable, fallback to current value (empty list)
        val = getattr(instance, self.set_name, self.value)        
        # Ensure internal None is treated as an empty list
        val = [] if val is None else val
        return self.__class__(self.name, value=val, ctx=instance)
    def __set__(self, instance, value):
        if instance is not None:
            # Always store as list, convert None to empty list
            actual_val = [] if value is None else list(value)
            setattr(instance, self.set_name, actual_val)
    def _sync_back(self):
        """Keeps the internal raw list in sync with wrapper mutations."""
        if self.ctx is not None:
            setattr(self.ctx, self.set_name, list(self))
    def append(self, item):
        super().append(item)
        self._sync_back()
    def extend(self, iterable):
        super().extend(iterable)
        self._sync_back()
    def insert(self, index, item):
        super().insert(index, item)
        self._sync_back()
    def pop(self, index=-1):
        val = super().pop(index)
        self._sync_back()
        return val
    def remove(self, item):
        super().remove(item)
        self._sync_back()
    def clear(self):
        super().clear()
        self._sync_back()
    def sort(self, *args, **kwargs):
        super().sort(*args, **kwargs)
        self._sync_back()
    def reverse(self):
        super().reverse()
        self._sync_back()
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._sync_back()
    def __delitem__(self, key):
        super().__delitem__(key)
        self._sync_back()
    def __iadd__(self, other):
        res = super().__iadd__(other)
        self._sync_back()
        return res
    def __imul__(self, n):
        res = super().__imul__(n)
        self._sync_back()
        return res

class _Children(_ListAttr):
    def _extract_items(self, *args):
        items = _extract_callables_props(*args) 
        final_items = []
        for item in items:
            route = child._child_item(item)
            if route: final_items.append(route)
        return final_items
    def __call__(self, *callables):
        final_items = self._extract_items(*callables)
        if instance := self.ctx:
            setattr(instance, self.set_name, final_items)
            return instance
        else:
            return final_items
    def __set__(self, instance, value):
        if instance is not None:
            setattr(instance, self.set_name, self._extract_items(*value) if value is not None else [])
    def append(self, item):
        super().extend(self._extract_items(item))
    def extend(self, iterable):
        super().extend(self._extract_items(*iterable))
    def insert(self, index, item):
        for i, p_item in enumerate(self._extract_items(item)):
            super().insert(index + i, p_item)
    def __iadd__(self, other):
        return super().__iadd__(self._extract_items(*other))

class _FlyInsOuts(_ListAttr):
    def _extract_items(self, *args):    
        items = _extract_callables_props(*args)
        obj = fly_out if "out" in self.name else fly_in
        final_items = []
        
        for item in items:
            dic = obj._func_item(item)
            if dic: final_items.append(dic)
        return final_items
    def __call__(self, *callables, override=None):
        final_items = self._extract_items(*callables)
        if instance := self.ctx:
            setattr(instance, self.set_name, final_items)
            if override is not None:
                base_name = self.name[:-1] if self.name.endswith('s') else self.name
                override_attr = f"{base_name}_override"
                setattr(instance, override_attr, bool(override)) 
            return instance
        else:
            return final_items
    def __set__(self, instance, value):
        if instance is not None:
            setattr(instance, self.set_name, self._extract_items(*value) if value is not None else [])
    def append(self, item):
        super().extend(self._extract_items(item))
    def extend(self, iterable):
        super().extend(self._extract_items(*iterable))
    def insert(self, index, item):
        for i, p_item in enumerate(self._extract_items(item)):
            super().insert(index + i, p_item)
    def __iadd__(self, other):
        return super().__iadd__(self._extract_items(*other))

def _unwrap(arr, toList=False):
    if isinstance(arr, (list, tuple, set)):
        arr = list(arr)
    else:
        return arr
    while isinstance(arr, (list, tuple, set)) and len(arr) == 1:
        inner = arr[0]
        if isinstance(inner, (list,tuple, set)):
            arr=list(inner)
        elif toList:
            break
        else:
            arr=inner
    return arr  

def _extract_callables_props(*args):
    # items = [args]               # 1st case : len(args) > 1 and callable(args[0]) and not callable(args[1]) and not (isinstance(args[1],(list,tuple)) and args[1] and not callable(args[1][0]) )
    #01 (      f1, a2,           )

    # items = list(args[0])        # 2nd cases: len(args) == 1 and isinstance(args[0], (list, tuple)) and len(args[0])>1 and not (callable(args[0][1]) or (isinstance(args[0][1],(tuple,list)) and args[0][1] and callable(args[0][1][0])   ))
    #02 (      [f1, f2, f3]      )
    #03 (      [(f1), f2]        )
    #04 (      [f1, (f2), f2]    )
    
    # items = list(args)
    #05 (                        )
    #06 (      [f1]              )
    #07 (      [f1, a2]          )
    #08 (      f1                )
    #09 (      f1, f2            )
    #10 (      f1,(f2, a2)       )
    #11 (      (f1),(f2)         )
    #12 (      (f1), f2          )
    #13 (      [f1, a1], [f2, a2])
    #14 (      []                )
    args = _unwrap(args, True)
    items = []
    if len(args) > 1 and callable(args[0]) and not (callable(args[1]) or isinstance(args[1], (_FuncDict, Route))) and not (isinstance(args[1],(list,tuple)) and args[1] and (callable(args[1][0]) or isinstance(args[1][0], (_FuncDict, Route)))):
        items = [args]
    else:
        items = list(args)
    return [_unwrap(item) for item in items]

layout = _Layout()
view = _View()
index = _Index()
fly_in = _FlyIn()
fly_out = _FlyOut()
child = _Child()
loader = _Loader()
fly_ins = _FlyInsOuts("fly_ins")
fly_outs = _FlyInsOuts("fly_outs")

class Route():
    layout = _Layout()
    view = _View()
    fly_in = _FlyIn()
    fly_out = _FlyOut()
    child = _Child()
    index = _Index()
    loader = _Loader()
    path = _StrAttr("path")
    children = _Children("children")
    fly_ins = _FlyInsOuts("fly_ins")
    fly_outs = _FlyInsOuts("fly_outs")
    fly_to = _StrAttr("fly_to")
    layout_override = _BoolAttr("layout_override")
    fly_in_override = _BoolAttr("fly_in_override")
    fly_out_override = _BoolAttr("fly_out_override")
    is_zone = _BoolAttr("is_zone")
    view_hero = _HeroAttr("view_hero")
    layout_hero = _HeroAttr("layout_hero")
    title = _StrAttr("title")
    icon = _StrAttr("icon")
    props= _DictAttr("props")
    
    @overload
    def __init__(self, path:str=None, view=None, children:list[Route]=None, index:Route=None,
                 fly_to:str=None, layout = None, layout_override:bool=None,
                    fly_ins = None, fly_in_override:bool=None, 
                    fly_outs=None, fly_out_override:bool=None,
                    view_hero:bool=None, layout_hero:bool=None,
                    title=None, icon=None, loader=None, props:dict=None, is_zone:bool=None, **kwargs): ...
    def __init__(self, *args, **kwargs):
        self._layout=None
        self._view=None
        self._loader = None
        self._index = None
        self._layout_override = None
        self._path = None
        self._fly_to = None
        self._fly_in_override = None
        self._fly_out_override = None
        self._icon = None
        self._title = None
        self._view_hero = None
        self._layout_hero = None
        self._is_zone = None
        self._fly_ins = []
        self._fly_outs = []
        self._children = []
        self._props = {}
        self._class = None

        self._adjust_locals(args, kwargs)
        self.parent = None
        # Dynamic calling module detection
        frame = sys._getframe(1)
        while frame:
            module_name = frame.f_globals.get('__name__')
            if module_name and not module_name.startswith('fletfly'):
                self.__module__ = module_name
                break
            frame = frame.f_back
        General._pending_routes.add(self)
    
    def copy(self, *args, **kwargs):
        new_route = self.__class__()
        ignore_list = ["_fletfly_method_child", "_fletfly_potential_path"]
        for key, val in self.__dict__.items():
            if isinstance(val, (dict, list, set)):
                new_route.__dict__[key] = val.copy()
            elif key not in ignore_list:
                new_route.__dict__[key] = val
        
        new_route._adjust_locals(args, kwargs)
        return new_route
    _ordered_fields = [
        "path", "view", "children", "index", "fly_to", "layout", "layout_override",
        "fly_ins", "fly_in_override", "fly_outs", "fly_out_override",
        "view_hero", "layout_hero", "title", "icon", "loader", "is_zone", "props"
    ]
    def _adjust_locals(self, args, kwargs):
        params = dict(zip(self._ordered_fields, args))
        params.update(kwargs)
        for official_name, aliases_list in aliases.items():
            for alias in aliases_list:
                if alias in params:
                    setattr(self, official_name, params.pop(alias))
                    break
        
        new_props = params.pop("props", "fletfly")
        if not new_props: # None, {}, False
            self_props = {}
            new_props = {}
        else:
            self_props = getattr(self, "props", {}) or {}
            if new_props == "fletfly": new_props = {}
        self.props = self_props | new_props | params
 
    @overload
    def __call__(self, path:str=None, view=None, children:list[Route]=None, index:Route=None, 
                 fly_to:str=None, layout = None, layout_override:bool=None,
                    fly_ins = None, fly_in_override:bool=None, 
                    fly_outs=None, fly_out_override:bool=None,
                    view_hero:bool=None, layout_hero:bool=None,
                    title=None, icon=None, loader=None, is_zone:bool=None,
                    props:dict=None, **kwargs): ...
    
    def __call__(self, *args, **kwargs):
        first_arg = args[0] if args else None
        
        # @obj.layout() or @obj.layout(override=True, role=User)
        handled_as_waiting = False
        for item_name in ["view", "layout", "fly_in", "fly_out", "loader"]:
            waiting_attr = f"_fletfly_waiting_{item_name}"
            props = getattr(self, waiting_attr, None) 
            if props is not None:
                setattr(self, item_name, _FuncDict(func=first_arg, name=item_name, props=props))
                setattr(self, waiting_attr, None) 
                handled_as_waiting = True        
        if handled_as_waiting:
            return first_arg
        
        # @obj, @Route("string") first call, @obj("str", **kwargs) second call
        if isinstance(first_arg, type):
            # inject class ref into instance
            self._class = first_arg
            
            return first_arg
        
        elif callable(first_arg): # function
            new_view = first_arg
            old_view = self._view
            if isinstance(old_view, _FuncDict):
                old_view = old_view["func"]
            if isinstance(new_view, _FuncDict):
                new_view = new_view["func"]
            
            if old_view and old_view != new_view:
                raise ValueError(f"[fletfly] Route route already has a view")
            else:
                self.view = (first_arg, self._props)
            return first_arg
        # @obj("str", **kwargs) first call
        else:
            self._adjust_locals(args, kwargs)
            return self

    def __new__(cls, *args, **kwargs): # handling 1 condition only, @Route/class or Route(class)
        if len(args) == 1 and not kwargs and isinstance(args[0], type):
            a = Route()
            a._class = args[0]            
            return args[0]
        elif len(args) == 1 and not kwargs and callable(args[0]):
            a = Route()
            a.view = _FuncDict(func=args[0], name="view", props = a._props)
            return args[0]
        else:
            return super().__new__(cls)


    def __dir__(self):
        global aliases
        return [key[0] for key in aliases] + ["_class"] + list(aliases.keys()) 

    def __repr__(self):
        return f"path:'{self._path}' {Route._format_route_with_no_path(self)}"
    def __setattr__(self, name, value):
        if name in _rev_aliases:
            name = _rev_aliases[name]
        super().__setattr__(name, value)
    def __getattr__(self, name):
        if name in _rev_aliases:
            official_name = _rev_aliases[name]
            return getattr(self, official_name)

        if name in self.__dict__:
            return self.__dict__[name]

        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    
    @classmethod
    def _get_parent(cls, path, tree):
        path = path.strip().strip("/").replace("//", "/")
        if len(path) > 0 and not path.startswith("/"): path = "/" + path
        segments = [s for s in path.split("/")]
        current_path = ""
        current_parent = None
        for i, seg in enumerate(segments[:-1]):
            if current_path not in tree:
                existing_node = next((n for n in (current_parent.children if current_parent else []) if n._path == seg), None)
                new_node = existing_node
                if new_node is None:
                    new_node = Route(path=seg)
                    new_node._is_placeholder=True
                tree[current_path] = new_node
                if current_parent and not existing_node:
                    current_parent.children.append(new_node)
            current_parent = tree[current_path]
            current_path += "/" + segments[i+1]
        return current_parent

    @classmethod
    def _handle_index(cls, parent:Route, child:Route, children): # child._path = "" and parent

        if parent._path is None:
            raise ValueError(f"[fletfly] Can't add index with path = '' into a pathless parent route.")
        if parent._view:
            raise ValueError(f"[fletfly] Can't add index with path='' into parent: '{parent._path}'. Parent already has a view view")
        if parent._index:
            raise ValueError(f"[fletfly] Parent with path='{parent._path}', already has an index. Can't duplicate.")
        if child._view:
            parent.index = child
            if children:
                raise ValueError(f"[fletfly] index for path='{parent._path}' can't have subroutes.")
            return True
        else:
            raise ValueError(f"[fletfly] The index added to parent '{parent._path}' must have a view.")
        
    @classmethod
    def _inject_into_tree(cls, route_node, zone:Zone, parent_full_path:str = "", parent:Route = None):
        """
Command Bunker, injection, if there is a path, then create a node in the map.
        """
        copy_mode = len(General._zones) > 1
        route = None
        children = [] 
        if isinstance(route_node, Zone): # the problem is here, all of this tree is already handled
            route = route_node._create_tree()
        elif isinstance(route_node, Route):
            if copy_mode:
                route_node = route_node.copy()
            children.extend(route_node._children)
            if route_node._class and not getattr(route_node, "_fletfly_method_child", None):
                route, more_children = cls._route_from_class(route_node._class, route_node, zone)
                children.extend(more_children)
            else:
                route = route_node
            route.children = []
        elif isinstance(route_node, type):
            route, more_children = cls._route_from_class(route_node, None, zone)
            children.extend(more_children)
            route.children = []
        if not route: return None
        if route._index:
            route._index._path = ""
            children.append(route._index)
            route._index = None
        
        
        route = Route._handle_path(route)
        route = Route._adjust_view(route)
        
        path1 = parent_full_path if parent_full_path else ""
        path2 = route._path if route._path else "" 
        path = (path1 + "/" + path2) if path1 or path2 else ""
        path = path.strip().strip("/").replace(" ", "").replace("_","-")
        while "//" in path: path = path.replace("//", "/")
        if len(path) > 0 and not path.startswith("/"): path = "/" + path
        
        # handling Root
        if route._path in ("", "/") and path in ("", "/"):
            if not zone.tree.get(""): 
                zone.tree[""] = route
            else:
                root_node = zone.tree[""]
                if getattr(root_node, "_is_placeholder", False):
                    cls._update_tree_children(route.children, root_node.children)
                    zone.tree[""] = route
                else:
                    cls._check_similarity(route, root_node, "Router already has a root")
                    route = root_node
                
        # handling "" index
        elif parent and route._path == "" and cls._handle_index(parent, route, children):
            return route # handled and route returned.
        
        # handling path situation
        elif route._path not in (None, "", "/"):
            route._path = path.split("/")[-1] if "/" in path else path
            if path in zone.tree:
                old_node = zone.tree[path]
                if getattr(old_node, "_is_placeholder", False):
                    zone.tree[path] = route
                    cls._update_tree_children(route.children, old_node.children)
                    
                    parent_node = parent if parent else cls._get_parent(path, zone.tree)
                    for i, child in enumerate(parent_node.children):
                        if child is old_node:
                            parent_node.children[i] = route
                            break
                    else: # if not break happened
                        route = cls._update_tree_children(parent_node.children, route)
                else:
                    cls._check_similarity(route, old_node, f"Path '{path}' already defined")
                    route = old_node
            else:
                parent_node = parent if parent else cls._get_parent(path, zone.tree)
                zone.tree[path] = route
                route = cls._update_tree_children(parent_node.children, route)
                
        elif parent:
            route = cls._update_tree_children(parent.children, route)
        else:
            raise ValueError("[fletfly] can't inject pathless route into the tree")
        
        if children:
            if route._path == "*": raise ValueError(f"[fletfly] Fallback route can't have children")
            for item in children:
                cls._inject_into_tree(route_node=item, zone=zone,parent_full_path= path, parent = route)
        
        return route
    @classmethod
    def _handle_path(cls, route):
        if General.auto_path_naming and(
            route._path is None or\
            route._path.lower().startswith(tuple(aliases["child"]+aliases["index"]))
        ):
            name = None
            potential = getattr(route, "_fletfly_potential_path", None)
            if not name and potential:
                silly = False
                for ch in aliases["child"]:
                    if potential.lower().startswith(ch):
                        silly = True
                        break
                if not silly: name = potential
            if not name and route._class:
                name = getattr(route._class, "__name__", None)
            if not name and route._view:
                func = route._view.get("func", None)
                if func: name = getattr(func, "__name__", func)
            if not name and route._layout:
                func = route._layout.get("func", None)
                if func: name = getattr(func, "__name__", func)
            if not name and route.fly_ins:
                func = route.fly_ins[0].get("func", None)
                if func: name = getattr(func, "__name__", func)
            if not name and route.fly_outs:
                func = route.fly_outs[0].get("func", None)
                if func: name = getattr(func, "__name__", func)
            if name is not None: 
                route.path = name
        if route._path is not None:
            name = re.sub(r'(?<!^)(?=[A-Z])', '-', route.path) # CamelCase to kebab_case
            route.path = name.lower().replace("_", "-").replace("--", "-")
        return route
    
    @classmethod
    def _adjust_view(cls, route): 
        if route._class and route._view is None and route._index is None and route._layout is None and\
            _is_flet_instance(route._class, or_class=True):
            route._view = _FuncDict(func=route._class, name="view", props=route._props)
        return route
    
    @classmethod
    def _check_similarity(cls, a1:Route, a2:Route, err_msg=None)->Route:
        if (a1._path == a2._path) and (
            a1._class == a2._class) and (
            a1._view == a2._view):
            print(f"[fletfly]: Duplication Warning: Route route with path='{a1._path}' already added. second registration ignored.")
            return True
        else:
            if err_msg: raise ValueError(err_msg)
            return False
        
    @classmethod
    def _update_tree_children(cls, children, routes:Route|list[Route])->Route|list[Route]:
        is_single = isinstance(routes, Route)
        if is_single: routes = [routes]
        resolved = []
        
        for route in routes:
            add = True
            active_route = route
            for brother in children:
                if route._path == brother._path and (
                    cls._check_similarity(route, brother,f"[fletfly] Route route with path='{route._path}' already exists.")
                    ):
                    add = False
                    active_route = brother
                # Ensure both paths exist and contain dynamic parameters using regex
                if route._path and brother._path and re.search(r"[:{\[]", route.path) and re.search(r"[:{\[]", brother.path):
                    raise ValueError(
                        f"Parent route already has a dynamic sub-route '{brother._path}'. "
                        f"Cannot add another dynamic route '{route._path}' at the same level."
                    )
            
            if add: children.append(route)
            resolved.append(active_route)
        return resolved[0] if is_single else resolved
    
    # creates route object carrying a class
    @classmethod
    def _route_from_class(cls, _class:type, route:Route, zone:Zone):
        
        registered_kids = []
        flagged_attr = []
        class_kids = _class._fletfly_children if "_fletfly_children" in _class.__dict__ else [] # cls._unify_class_children_of_zone(_class)        # returning new Route, and potential kids of classes
        local_aliases = dict(_rev_aliases)
        def remove_aliases_of(del_key):
            for key in list(local_aliases.keys()): 
                if local_aliases[key] == del_key:
                    del local_aliases[key]
        
        if not route:
            route = Route()
            route._class = _class
        
        def create_index_child(att_name, clbl, props, index_child):
            sub = Route(props=props)
            if inspect.isfunction(clbl):
                sub.view=att_name
                sub._class=_class
                sub._fletfly_method_child = True
            elif inspect.isclass(clbl):
                if isinstance(clbl, type):
                    class_kids.discard(clbl)
                sub._class=attr_val
            if index_child == "index":
                sub.path == ""
                route.index = sub
            else:
                registered_kids.append(sub)
                if sub._path is None:
                    sub._fletfly_potential_path = attr_name
                    sub.path = att_name
            return sub

        # first loop for flagged functions
        for attr_name, attr_val in _class.__dict__.items():

            if attr_name.startswith("_"): continue

            # Unwrap the underlying function if wrapped in staticmethod or classmethod
            attr_val = getattr(attr_val, "__func__", attr_val)

            for item_name in ["view", "layout", "fly_in", "fly_out", "child", "index"]:
                if hasattr(attr_val, f"_fletfly_{item_name}"): # if function or class has decorator
                    
                    if isinstance(attr_val, type): class_kids.discard(attr_val) # used class, don't repeat
                    
                    flagged_attr.append(attr_name)
                    list_of_dicts = getattr(attr_val, f"_fletfly_{item_name}")
                    for kid_dict in list_of_dicts: # dic has kwargs, and single keys for expected.
                        kid_props = kid_dict.pop("props", {})

                        if item_name in ["view", "layout"]:
                            setattr(route, item_name, _FuncDict(func=attr_name, name=item_name, props=kid_props))
                            remove_aliases_of(item_name)
                            for item in kid_dict:
                                setattr(route, item, kid_dict[item])

                        elif item_name in ["fly_in", "fly_out"]:
                            dic = _FuncDict(func=attr_name, name=item_name, props=kid_props)
                            for item in kid_dict:
                                if "override" in item:
                                    setattr(route, item, kid_dict[item])
                                else:
                                    dic[item] = kid_dict[item]
                            getattr(route, f"{item_name}s").append(dic)

                        elif item_name in ["child", "index"]: # "child"
                            sub = create_index_child(attr_name, attr_val, kid_props, item_name)
                            for item in kid_dict:
                                setattr(sub, item, kid_dict[item])
        
        # second loop for any other attr
        for attr_name, attr_val in _class.__dict__.items():
            if attr_name.startswith("_") or attr_name in flagged_attr: continue
            # Unwrap the underlying function if wrapped in staticmethod or classmethod
            attr_val = getattr(attr_val, "__func__", attr_val)
            # attr = func, not func directly
            static = attr_name != getattr(attr_val, "__name__", attr_val)

            # Matching aliases by prefix
            matched_alias = next((k for k in local_aliases if attr_name.lower().startswith(k)), None)
            if matched_alias:
                official_name = local_aliases[matched_alias]
                if callable(attr_val):
                    _get_set_payload(attr_val)
                    if General.detect_method_ordinaries:
                        if official_name in ["view", "layout", "loader"]:
                            setattr(route, official_name, _FuncDict(func=attr_val if static else attr_name, name=official_name))
                        elif official_name in ("fly_in", "fly_out"):
                            getattr(route, f"{official_name}s", []).append(attr_val if static else attr_name)
                        elif official_name in ("index", "child"):
                            sub = create_index_child(attr_name, attr_val, {}, official_name)
                else:
                    if official_name == "path": # actual value
                        route.path = attr_val
                        remove_aliases_of(local_aliases[attr_name])
                    if official_name == "children":
                        remove_aliases_of(local_aliases[attr_name])
                    elif official_name in ["fly_ins", "fly_outs"]:
                        if isinstance(attr_val, (list, tuple, list)):
                            getattr(route, official_name).extend(attr_val)
                        else:
                            raise ValueError(f"[fletfly] {attr_name} value should be iterable (list | tuple).")
                    elif official_name in ["title", "icon"]:
                        setattr(route, official_name, General._attr_prefix+attr_name)
                        remove_aliases_of(local_aliases[attr_name])
                    elif official_name in ["fly_in", "fly_out"]:
                        getattr(route, f"{official_name}s", []).append(attr_val)
                    elif official_name !="path": # booleans
                        setattr(route, official_name, attr_name)
                        remove_aliases_of(local_aliases[attr_name])
            # inspect methods                        
            elif inspect.isfunction(attr_val) and General.detect_method_routes:
                _get_set_payload(attr_val)
                new_sub = Route(path=attr_name)
                new_sub.view=_FuncDict(func=attr_name, name="view")
                new_sub._class=_class
                new_sub._fletfly_method_child = True
                registered_kids.append(new_sub)
            # inspect route instances
            elif isinstance(attr_val, Route):
                sub = attr_val
                if sub._path is None:
                    if hasattr(sub, "_fletfly_potential_path"):
                        raise ValueError(f"f[fletfly] Route in attr'{attr_name}' any adjustment will affect original route, use copy() method")
                    else:
                        sub._fletfly_potential_path = attr_name
                        registered_kids.append(sub)
            elif isinstance(attr_val, _FuncDict):
                n = attr_val.get("name", None)
                if n:
                    setattr(route, n, attr_val)
        zone.registered_children.update(registered_kids)
        return route, list(class_kids) + registered_kids
    
    # get inner classes and children classes and register them all in registered_children
    @classmethod
    def _unify_class_children(cls, class_route_zone:type|Route, registered_children, routed_classes)->set:
        _get_set_payload(class_route_zone)
        children = set()
        clas = None
        if isinstance(class_route_zone, Route):
            children.update(class_route_zone.children)
            if class_route_zone._class:
                clas = class_route_zone._class
                routed_classes.add(clas)
        elif isinstance(class_route_zone, type):
            clas = class_route_zone
        elif isinstance(class_route_zone, Zone):
            General._zones.append(class_route_zone)
        if clas:
            for attr_name, attr_value in clas.__dict__.items():
                if attr_name.startswith("_"):
                    continue
                if isinstance(attr_value, Zone):
                    if attr_value.path in (None, "", "/"):
                        attr_value.path = attr_name
                    children.add(attr_value)
                elif isinstance(attr_value, type):
                    if General.detect_inner_classes or hasattr(attr_value, "_fletfly_child"):
                        children.add(attr_value)
                elif attr_name in aliases["children"]:
                    if not isinstance(attr_value, (list, tuple, set)):
                        raise ValueError(f"[fletfly] {attr_name} must be with type <list | tuple>")
                    else:
                        children.update(attr_value)
            _fletfly_children="_fletfly_children"
            
            if not hasattr(clas, _fletfly_children):
                setattr(clas, _fletfly_children, set())
            getattr(clas, _fletfly_children, set()).update(children)
        registered_children.update(children)
        for child in children:
            cls._unify_class_children(child, registered_children, routed_classes)
        return children




    @classmethod
    def _create_tree(cls, anchors:list=None):
        if General.detect_route_subclasses:
            General._inherited_classes = set(Route.__subclasses__())
            General._inherited_classes.discard(Shared)
            General._inherited_classes.discard(Zone)
        if not General.detect_created_routes:
            General._pending_routes = set()
        
        for unit in (General._inherited_classes | General._pending_routes):
            cls._unify_class_children(unit, General._registered_children, General._routed_classes)
        
        zone0 = Zone(anchors, path="")
        zone0.modules.add('__main__')
        General._zones.append(zone0)
        z_idx = 0
        while z_idx < len(General._zones):
            z = General._zones[z_idx]
            for unit in z.anchors:
                cls._unify_class_children(unit, z.registered_children, z.routed_classes)
            z_idx += 1
        
        _adjust_zones_modules(General._zones)
        zone0._create_tree()
        General._main_zone_tree = zone0.tree

        for unit in set(Shared.__subclasses__()) | General._pending_shared:
            if isinstance(unit, Shared):
                if unit._class:
                    shared, _ = Route._route_from_class(unit._class, unit)
                else:
                    shared = unit
                if not shared._name:
                    if shared._class:
                        shared.name = shared._class.__name__
                    else:
                        shared.name = getattr(shared._view["func"], "__name__", str(shared._view["func"]))
                shared = Route._adjust_view(shared)
                General._shared_routes[shared._name] = shared

    @classmethod
    def _check_root_fly_to(cls, tree):
        root = tree.get('')
        if root and root._view is None and root._index is None and root._fly_to is None:
            common_paths = ['/home', '/index', '/main', '/dashboard', '/start']
            found_target = None
            
            for p in common_paths:
                x = tree.get(p, None)
                if x and (x._view or x._layout or (x._index and (x._index._view or x._index._layout))):
                    found_target = p
                    break
            if not found_target:
                valid_paths = []
                for k, v in tree.items():
                    if ':' not in k and '[' not in k and '{' not in k and v and(
                        v._view or (v._index and v._index._view)):
                        valid_paths.append(k)
            
                if valid_paths:
                    valid_paths.sort(key=lambda x: (x.count('/'), len(x)))
                    found_target = valid_paths[0]
            if found_target:
                root.fly_to = found_target

    @classmethod
    def _validate_children(cls, child_ren):
        child_ren = _unwrap(child_ren)
        _validated_list = []

        if isinstance(child_ren, (tuple, list)):
            for obj in child_ren:
                _validated_list.extend(cls._validate_children(obj))
        elif isinstance(child_ren, type):
            _validated_list.append(Route._route_from_class(child_ren))  # convert class to Node directly
        elif isinstance(child_ren, Route):
            _validated_list.append(child_ren)
        elif isinstance(child_ren, dict):
            path = child_ren.get("path") or child_ren.get("name")
            children_data = child_ren.get("children") or child_ren.get("routes") or child_ren.get("screens")
            
            if isinstance(path, str) or isinstance(children_data, (list, tuple)):

                subs = child_ren.pop("children", child_ren.pop("routes", child_ren.pop("screens", [])))
                obj = Route(**child_ren)
                
                if subs: obj.children.extend(subs)
                
                _validated_list.append(obj)
            else:
                for k, v in child_ren.items():
                    if isinstance(v, Route):
                        v.route = k
                        _validated_list.append(v)
                    elif callable(v) or hasattr(v, "controls") or hasattr(v, "content"):
                        _validated_list.append(Route(path=k, view=v))

        return _validated_list
    
    @staticmethod
    def cut(st:str, num:int, just=False, fill=" "):
        if len(st) > num:
            st = st[:num-3]+"..."
        elif len(st) < num and just:
            st = st.ljust(num, fill)
        return st
    @classmethod
    def _format_route_with_no_path(cls, route):
        cls_ = '<'+Route.cut(route._class.__name__,14)+'>' if route._class else ''
        
        view = route._view["func"] if route._view and isinstance(route._view, _FuncDict) else route._view
        v = '<'+ Route.cut(view.__name__,12)+'>' if callable(view) else ('"'+ Route.cut(view,12)+'"' if isinstance(view,str) else '')

        load = route._loader["func"] if route._loader and isinstance(route._loader, _FuncDict) else route._loader
        ld = '<'+ Route.cut(load.__name__,12)+'>' if callable(load) else ('"'+ Route.cut(load,12)+'"' if isinstance(load,str) else '')
    
        if not isinstance(route, Shared):
            lay = route._layout["func"] if route._layout and isinstance(route._layout, _FuncDict) else route._layout
            ly = '<'+ Route.cut(lay.__name__,12)+'>' if callable(lay) else ('"'+ Route.cut(lay,12)+'"' if isinstance(lay,str) else '')

            to = "'"+Route.cut(route._fly_to, 12)+"'" if route._fly_to else ''

            ins = len(route.fly_ins)
            outs = len(route.fly_outs)

            if ld and not to:
                tail = f"ly:{ly:<14} ld:{ld:<14}  ins: {ins:<2} outs: {outs:<2}"
            elif ld and not ly:
                tail = f"ld:{ld:<14} to:{to:<14}  ins: {ins:<2} outs: {outs:<2}"
            elif ld and not ins and not outs:
                tail = f"ly:{ly:<14} to:{to:<14} ld:{ld:<14}"
            else:
                tail = f"ly:{ly:<14} to:{to:<14}  ins: {ins:<2} outs: {outs:<2}"
            
        else:
            hero = f"{str(route._hero)}" if route._hero else ''

            tail = f"load:{ld:<14} hero:{hero:<5} "

        return f"cls:{cls_:<14} view:{v:<14} {tail}"
    
    @classmethod
    def _format_route_tree(cls, current_path="", static_paths=None, dynamic_paths=None, 
                            route=None, prefix="", is_last=True):
        is_root = False
        if route is None:
            is_root = True
            search_path = "/" + current_path.strip("/")
            if search_path == "/": search_path = ""
            route = General._main_zone_tree.get(search_path, None)
            if route is None:
                print(f"[fletfly] branch {current_path} was not found in the route tree.")
                return
            search_path+='/'
            if len(search_path) > 15:
                path = "..." + search_path[-12:] + " "
            elif len(search_path) == 15:
                path = search_path+' '
            elif len(search_path) == 14:
                 ' '+search_path+' '
            else:
                path = '─ '+search_path+' '
        else:
            path = '─ '+route._path.rstrip("/")+'/ ' if route._path else ('─ [INDEX] ' if route._path == "" else '')
            
        current_path = "/" + current_path.strip("/")

        tag = ""
        if route._path is not None and route._index is None:
            if current_path in static_paths:
                tag += " [STC]"+current_path
            else:
                for pattern in dynamic_paths.keys():
                    match = pattern.match(current_path)
                    if match:
                        tag += " [DYN]"+current_path
        
        marker = "" if is_root else ("└─" if is_last else "├─")
        marker2 = " " if is_root else (" " if is_last else "│")
        dashes = " - " * 36 + "\n"
        output = f"{prefix}{marker}{Route.cut(path,17, True, "─")} {Route._format_route_with_no_path(route)}{tag}\n"
        output += f"{prefix}{marker2}"
        if not route.children:
            output += dashes
        else:
            output += "   │" + dashes
            child_prefix = prefix + ("    " if is_last else "│   ")
            child_list = ([route._index] if route._index else []) + route.children
            for i, child in enumerate(child_list):
                is_child_last = (i == len(child_list) - 1)
                child_path = current_path.strip("/")+"/"+ (child._path.strip("/") if child._path else "")
                output += cls._format_route_tree(current_path=child_path, static_paths=static_paths, dynamic_paths=dynamic_paths, route=child, prefix=child_prefix, is_last=is_child_last)
                
        return output
    
    def _vampire(self, victim):
        if not victim or self is victim:
            return self
        if victim.parent and not self.parent:
            return victim._vampire(self)
        
        if self.parent and victim.parent:
            raise ValueError(f"[fletfly] Union Error: Both routes have parents. Cannot merge '{self.path}' and '{victim.path}'.")
        
        if self._view and victim._view:
            raise ValueError(f"[fletfly] Union Error: Conflict in 'view'. Both routes provide content for path '{self.path}'.")
        
        if self._layout and victim._layout:
            raise ValueError(f"[fletfly] Union Error: Conflict in 'layout' (layout). Both routes define a layout.")

        for key, value in victim.__dict__.items():
            if key in ('children', 'fly_ins', 'fly_outs', 'parent'):
                continue
            
            if getattr(self, key, None) is None:
                setattr(self, key, value)
        
        for item in victim.fly_ins:
            if item not in self.fly_ins:
                self.fly_ins.append(item)
        
        for item in victim.fly_outs:
            if item not in self.fly_outs:
                self.fly_outs.append(item)

        if victim.children:
            for sub in list(victim.children):
                existing_sub = next((s for s in self.children if s._path == sub._path), None)
                if existing_sub:
                    existing_sub._vampire(sub)
                else:
                    self.children.append(sub)

        victim.__dict__.clear()
        return self

class _BlockedAttr:
    def __get__(self, instance, owner):
        raise AttributeError("[fletfly] Attribute not supported in Shared.")
    def __set__(self, instance, value):
        raise AttributeError("[fletfly] Attribute not supported in Shared.")

class Shared(Route):
    name = _StrAttr("name")
    hero = _HeroAttr("hero")
    
    _ordered_fields = ["name", "view", "hero", "loader", "props"]
    
    path = _BlockedAttr()
    layout = _BlockedAttr()
    child = _BlockedAttr()
    index = _BlockedAttr()
    fly_in = _BlockedAttr()
    fly_out = _BlockedAttr()
    children = _BlockedAttr()
    fly_ins = _BlockedAttr()
    fly_outs = _BlockedAttr()
    fly_to = _BlockedAttr()
    layout_override = _BlockedAttr()
    fly_in_override = _BlockedAttr()
    fly_out_override = _BlockedAttr()
    is_zone = _BlockedAttr()
    layout_hero = _BlockedAttr()
    view_hero = _BlockedAttr()
    title = _BlockedAttr()
    icon = _BlockedAttr()
    
    def __init__(self, name:str=None, view=None, hero:bool|int=None, loader=None, props:dict=None, **kwargs):
        super().__init__(name=name, view=view, hero=hero, loader=loader, props=props, **kwargs)
        General._pending_routes.discard(self)
        General._pending_shared.add(self)
    
   
    def __new__(cls, *args, **kwargs): # handling 1 condition only, @Shared/class or Shared(class)
        if len(args) == 1 and not kwargs and isinstance(args[0], type):
            a = Shared()
            a._class = args[0]            
            return args[0]
        elif len(args) == 1 and not kwargs and callable(args[0]):
            a = Shared()
            a.view = _FuncDict(func=args[0], name="view")
            return args[0]
        else:
            return super().__new__(cls) 
    def __repr__(self):
        return f"{Route._format_route_with_no_path(self)}  name:'{self._name}'"

class Zone:
    def __init__(self, route_class_module_or_list, path=None):
        self.path = path
        if not isinstance(route_class_module_or_list, (tuple, list, set)):
            route_class_module_or_list = [route_class_module_or_list]   
        self.anchors = []
        self.modules = set()
        for item in route_class_module_or_list:
            mod = None
            if isinstance(item, str) and item in sys.modules:
                mod = item
            elif isinstance(item, types.ModuleType):
                mod = item.__name__
            elif isinstance(item, (Route, type, types.FunctionType, types.MethodType)):
                mod = item.__module__
                self.anchors.append(item)
            elif isinstance(item, dict):
                self.anchors.append(item)
            if mod and mod in General._reserved_anchor_modules:
                raise ValueError(f"[fletfly] Module {mod} is used in different zones. Different zones can't have same original modules, but can have shared modules.")
            elif mod:
                self.modules.add(mod)
        General._reserved_anchor_modules.update(self.modules) 
        
        self.parents = []
        self.registered_children = set()
        self.routed_classes = set()
        self.tree = {}

    def _create_tree(self)->Route:
        inh = {c for c in General._inherited_classes if c.__module__ in self.modules}
        pnd = {c for c in General._pending_routes if c.__module__ in self.modules}
        reg = General._registered_children | self.registered_children
        rou = General._routed_classes | self.routed_classes
        pre_finals = ((inh | pnd)-(reg | rou))
        finals = [i for i in self.anchors if isinstance(i, dict) or i not in pre_finals] + list(pre_finals)

        for unit in finals:
            Route._inject_into_tree(route_node=unit, zone=self)
        
        Route._check_root_fly_to(self.tree)

        route = self.tree.get('', None)
        if route:
            route.path = self.path
            route.is_zone=True
            return route
        else:
            print(f"[fletfly] Failed to create Zone {self.path}")
            return None
import types

def _should_ignore_module(mod):        
    mod_name = getattr(mod, '__name__', '').split('.')[0]
    if mod_name == '__main__':
        return False  # Do not ignore the entry point
        
    # Ignore Python Standard Library modules
    if mod_name in sys.stdlib_module_names or mod_name == 'builtins':
        return True
        
    # Ignore Flet and fletfly itself to avoid circular deep inspection
    if mod_name in {'flet', 'fletfly'}:
        return True
        
    # Ignore built-in extensions without a __file__ attribute (e.g., built-in C modules)
    file_path = getattr(mod, '__file__', None)
    if not file_path:
        return True
        
    # Ignore external third-party libraries installed via pip
    file_path = os.path.abspath(file_path)
    if "site-packages" in file_path or "dist-packages" in file_path:
        return True
        
    return False

def _adjust_zones_modules(zones:list[Zone]): # [["__main__"], ["project1_a", "project1_b"]]
    """
    Builds an isolated routing hierarchy treating all inputs as uniform zones.
    Index 0 represents the Root Zone (Main Project).
    """
    ignored = set()
 
    for zone in zones:
        queue = list(zone.modules)
        while queue:
            mod_obj = sys.modules.get(queue.pop(0))
            if not mod_obj: continue
                
            for attr_name in dir(mod_obj):
                try:
                    attr = getattr(mod_obj, attr_name)
                except AttributeError:
                    continue
                    
                target_mod = None
                if isinstance(attr, types.ModuleType):
                    target_mod = attr.__name__
                elif isinstance(attr, (Route, type, types.FunctionType, types.MethodType)):
                    target_mod = attr.__module__

                if not target_mod or\
                        target_mod in General._reserved_anchor_modules or\
                        target_mod in ignored: continue
                if _should_ignore_module(target_mod):
                    ignored.add(target_mod)
                    continue
                    
                if target_mod not in zone.modules:
                    zone.modules.add(target_mod)
                    queue.append(target_mod)
    return zones