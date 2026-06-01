from __future__ import annotations
import flet as ft
import re, sys, inspect, asyncio, os, importlib.util, time, builtins
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

__all__ = ['Airway', 'airway', 'route', 'Route', 'Airline', 'Router', 'fly_ins', 'fly_outs', 'Airzone', 'slot', 'data', 'fly', 'fly_around']

_page_err_msg = f"""

🚨 [Core Concept] Why the (page) argument is mandatory:
Flet executes the main(page) function from scratch for every single web user, handing over their exclusive page session. Therefore, you must create a session-related instance for any user-interactive, changeable content.
If you ignore the page argument, User A's actions will affect User B on all levels.
To fix this, you must add your control instances to that specific page or a view on that page. Additionally, any user-level state or variables must be stored within that page session.

fletfly.Airline router, depends completely on page sessions to securely support high-level multi-slots in layouts and builds with automatic or manual naming.

💡 How we handle sessions together perfectly:
We will pass the (page) argument to your functions, and we expect you to pass it back inside slot(page). This ensures every user gets an isolated instance. Example:
def layout(page):
    return ...your design... slot(page, 'slot_name') ... slot(page, 3)  ...your design...
           ...your design... slot(page) ...slot(page, 'shared_1', ft.Card(), True)...your design...
              (auto-named to 10000001)^                                    ^ (True=Stick to 'shared_1')
"""
aliases = {
    "path": ["path", "url", "route"],
    "build": [ "build", "view", "builder", "component", "element", "contents", "controls",],
    # build_hero takes True or 1 for static pathes, and True or int for dynamic pathes (True means 5)
    "build_hero": [ "build_hero", "hero_view", "build_heroer", "hero_component", "hero_element", "hero_contents", "hero_controls",],
    "fly_ins": ["fly_ins", "loader", "canActivate", "beforeEnter", "middleware", "beforeLoad",],
    "fly_ins_override": ["fly_ins_override", "loader_override", "canActivate_override", "beforeEnter_override", "middleware_override", "beforeLoad_override",],
    "fly_outs": ["fly_outs", "canDeactivate", "beforeUnload",],
    "fly_outs_override": ["fly_outs_override", "canDeactivate_override", "beforeUnload_override",],
    "layout": ["layout", "frame",],
    "layout_override": ["layout_override", "frame_override",],
    "layout_hero": ["layout_hero", "hero_frame",],
    "fly_to": ["fly_to", "redirect", "redirectTo",],
    "title": ["title", ],
    "icon": ["icon", "logo",],
    "subway": ["subway", "child", "sub"],
    "subways": ["subways", "children", "routes", "screens", "subs"],
    "fly_around": ["fly_around", "shared", "shared_build"],
    "post_fly": ["post_fly", "binder", "hydrator"],
}
_rev_aliases = {val:k for k in aliases.keys() for val in aliases.get(k)}

class _MethodHandler:
    def __init__(self, ctx=None):
        self.ctx = ctx
        
    def __get__(self, instance, owner):
        return self.__class__(instance if instance is not None else owner)

    def __set__(self, instance, value):
        if instance is not None:
            if self.set_type == "list":
                alist = getattr(instance, self.set_name)
                if isinstance(value, (list, tuple, set)):
                    alist.extend(value)
                else:
                    alist.append(value)
            else:
                setattr(instance, self.set_name, value)

    def _process_core(self, first_arg, config_args: dict):
        _clsattr = "_clsattr"
        _fletfly_= "_fletfly_"

        instance = None if self.ctx is None or isinstance(self.ctx, type) else self.ctx
        def class_inject(clas, kwargs=None):
            if kwargs is None: kwargs = {}
            parents = list(kwargs.get("parents") or [])
            if self.name == "subway":
                if instance or parents:
                    parents += [instance] if instance else []
                    for parent in parents:
                        cl = None
                        if isinstance(parent, Airway): 
                            parent.subways.append(clas)   # append the class to the airway instance
                            cl = parent._class            # get his class to append to it too
                        elif isinstance(parent, type):
                            cl = parent
                        if cl:
                            parent_class_subways = getattr(cl, "subways", None)
                            if parent_class_subways is not None:
                                if isinstance(parent_class_subways, list):
                                    parent_class_subways.append(clas)
                                elif isinstance(parent_class_subways, set):
                                    parent_class_subways.add(clas)
                            else:
                                setattr(cl, "subways", [clas])
            elif instance:
                raise ValueError(f"[fletfly] Can't use @airway.{self.name} method decorating a class, use @{self.name} or @Airway.{self.name} instead.")
            
            setattr(clas, _fletfly_+self.name, True)
            kwargs.pop('parents', None)
            for key, val in kwargs.items():
                if key in ["override", "hero"]: key = f"{self.name}_{key}"
                if val is not None:
                    setattr(clas, key, val)  # class.layout_hero = True & 
                    if not callable(val):
                        setattr(clas, key+_clsattr, key)
                    else:
                        setattr(val, _fletfly_+"static", True)
                        print(f"[fletfly] Callable function {key}=<{val.__name__}> handed in decorator will be static, can't be changed on runtime, and won't recieve 'self' argument.")
            return clas

        def func_inject(func, kwargs=None):
            if kwargs is None: kwargs = {}          
            if instance:                    # @route.layout or @Airway().layout
                if self.set_type == "list":
                    getattr(instance, self.set_name).append(func)               # add function to airway list
                else:
                    setattr(instance, self.set_name, func)                                # method to excute
                for key, val in kwargs.items():
                    if key in ["override", "hero"]: key = f"{self.name}_{key}"
                    if val is not None:
                        setattr(instance, key, val)

            setattr(func, _fletfly_+self.name, True)                        # inject it maybe it is a method
            for key, val in kwargs.items():
                if key in ["override", "hero"]: key = f"{self.name}_{key}"
                if val is not None:
                    setattr(func, f"{_fletfly_}{key}", val)
            return func
        
        
        # decorating a class without calling @layout | @Airway.layout | @route.layout:
        if isinstance(first_arg, type):
            return class_inject(first_arg)
        # decorating a func or method without calling @layout | @Airway.layout | @route.layout:
        elif callable(first_arg):
            return func_inject(first_arg)
        else:                                       # Decorating with calling ()
            def wrapper(func_or_class):
                # decorating a class with calling @layout() | @Airway.layout() | @route.layout():
                if isinstance(func_or_class, type):
                    return class_inject(func_or_class, config_args)
                # decorating a method or func with calling @layout() | @Airway.layout() | @route.layout():
                else:
                    return func_inject(func_or_class, config_args)
            return wrapper

class _Layout(_MethodHandler):
    name = "layout"
    set_name = "_layout"
    set_type = "_"
    def __call__(self, 
                 hero:bool=None,
                 override:bool=None
                 ):
        return self._process_core(hero, {
            "hero": hero,
            "override": override
            })
class _Build(_MethodHandler):
    name = "build"
    set_name = "_build"
    set_type = "_"
    def __call__(self, 
                    hero:bool=None
                    ):
        return self._process_core(hero, {
            "hero": hero
            })
class _FlyIn(_MethodHandler):
    name = "fly_in"
    set_name = "fly_ins"
    set_type = "list"
    def __call__(self, 
                 override:bool=None
                 ):
        return self._process_core(override, {
            "override": override
            })
class _FlyOut(_MethodHandler):
    name = "fly_out"
    set_name = "fly_outs"
    set_type = "list"
    def __call__(self, 
                 override:bool=None
                 ):
        return self._process_core(override, {
            "override": override
            })
class _Subway(_MethodHandler):
    name = "subway"
    set_name = "subways"
    set_type = "list"
    def __call__(self,
                 path:str=None,
                 parents:list[Airway|type]=None,
                 build=None, subways:list[Airway]=None,
                 fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_ins_override:bool=None, 
                 fly_outs=None, fly_outs_override:bool=None,
                 is_zone:bool=None, build_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, post_fly=None, 
                 ):
        config = locals()
        config.pop("self")
        config.pop("config", None)
        return self._process_core(path, config)

layout = _Layout()
build = _Build()
fly_in = _FlyIn()
fly_out = _FlyOut()
subway = _Subway()

class Airway():
    layout = _Layout()
    build = _Build()
    fly_in = _FlyIn()
    fly_out = _FlyOut()
    subway = _Subway()

    path:str=None
    subways:list[Airway]=[]
    fly_to:str=None
    layout_override:bool=None
    fly_ins = None
    fly_ins_override:bool=None 
    fly_outs=None
    fly_outs_override:bool=None,
    is_zone:bool=None,
    build_hero:bool=None
    layout_hero:bool=None
    title=None
    icon=None
    post_fly=None
    
    _airways_all = set() # every created or cloned airway
    _airways_wild = set() # original but never adopted
    _registered_children_classes = set()
    _pending_classes = set()

    
    def __init__(self, path:str=None, build=None, subways:list[Airway]=None,
                 fly_to:str=None, layout = None, layout_override:bool=None,
                    fly_ins = None, fly_ins_override:bool=None, 
                    fly_outs=None, fly_outs_override:bool=None,
                    is_zone:bool=None, build_hero:bool=None, layout_hero:bool=None,
                    title=None, icon=None, post_fly=None, **kwargs):

        self._layout=None
        self._build=None
        self.layout_override = None
        self.path = None
        self.fly_to = None
        self.fly_outs = None
        self.fly_ins_override = None
        self.fly_outs_override = None
        self.icon = None
        self.title = None
        self.build_hero = None
        self.layout_hero = None
        self.post_fly = None
        self.subways = None
        self.fly_ins = None
        self.fly_outs = None

        self._class = None

        self.path_clsattr = None
        self.build_clsattr = None
        self.fly_to_clsattr = None
        self.layout_clsattr = None
        self.layout_override_clsattr = None
        self.fly_ins_clsattr = None
        self.fly_outs_clsattr = None
        self.fly_ins_override_clsattr = None
        self.fly_outs_override_clsattr = None
        self.title_clsattr = None
        self.icon_clsattr = None
        self.build_hero_clsattr = None
        self.layout_hero_clsattr = None
        self.post_fly_clsattr = None

        self._adjust_locals(locals())
        #initiating lists
        if not self.subways: self.subways = []
        if not self.fly_ins: self.fly_ins = []
        if not self.fly_outs: self.fly_outs = []
        if not self.fly_ins_clsattr: self.fly_ins_clsattr = []
        if not self.fly_outs_clsattr: self.fly_outs_clsattr = []

        self.parent = None
        Airway._airways_all.add(self)
        Airway._airways_wild.add(self)

    def _adjust_locals(self, params):
        del params['self']
        for val_list in aliases.values():
            for alias in val_list:
                original = val_list[0]
                if params.get(original) is None: # if local self.layout = None
                    if params['kwargs'].get(alias, None) is not None: # if not frame = None
                        params[original] = params['kwargs'].get(alias, None)              
                if alias in params['kwargs']: 
                    params['kwargs'].pop(alias, None)

        # initiating private
        for item in ("build", "layout"):
            params["_"+item] = params[item]
            del params[item]
        
        for k, v in params.items():
            if v is not None and k != "kwargs":
                self.__dict__[k] = v
        for k, v in params.get("kwargs", {}).items():
            if v is not None:
                self.__dict__[k] = v
        if self.path: self.path = self.path.lower()
        
    def __new__(cls, *args, **kwargs):
        if len(args)==1 and isinstance(args[0], type): # @Airway
            cls._pending_classes.add(args[0]) # register class
            return args[0]
        return super().__new__(cls)

    def __call__(self, path:str=None, build=None, subways:list[Airway]=None,
                 fly_to:str=None, layout = None, layout_override:bool=None,
                    fly_ins = None, fly_ins_override:bool=None, 
                    fly_outs=None, fly_outs_override:bool=None,
                    is_zone:bool=None, build_hero:bool=None, layout_hero:bool=None,
                    title=None, icon=None, post_fly=None, **kwargs):
        # @obj, @Airway("string") first call, @obj("str", **kwargs) second call
        if isinstance(path, type):
            cl = path
            for name, value in self.__dict__.items():     # inject values into class
                if name in ("_build", "_layout"):
                    setattr(cl, name.lstrip("_"), value)
                elif name.startswith('_'):
                    continue
                elif value is not None and not isinstance(value, _MethodHandler):
                    setattr(cl, name, value)
            self.__class__._pending_classes.add(cl)

            self._class = cl                              # inject class ref into instance
            return cl
        # @obj("str", **kwargs) first call
        else:
            self._adjust_locals(locals())
            return self

    def __dir__(self):
        global aliases
        return [key[0] for key in aliases] + ["_class"] + list(aliases.keys()) 

    def __repr__(self):
        subways_count = len(self.subways) if self.subways is not None else None
        _class = self._class.__name__ if self._class else 'None'
        fly_to = self.fly_to if self.fly_to else 'None'
        bld = self._build if self._build else 'None'
        bld_clsattr = self.build_clsattr if self.build_clsattr else 'None'
        return f'<Airway Obj {("'"+self.path+"'"):<10} build={("'"+bld+"'"):<10} build_clsattr={("'"+bld_clsattr+"'"):<10} subways=[{subways_count:2}] _class={_class:<10}>'

    def __setattr__(self, name, value):
        if name in _rev_aliases:
            name = _rev_aliases[name]
        if name == "path" and isinstance(value, str):
            value = value.lower()
        super().__setattr__(name, value)

    def __getattr__(self, name):
        if name in _rev_aliases:
            official_name = _rev_aliases[name]
            if official_name in ("build", "layout") and f"_{official_name}" in self.__dict__:
                return self.__dict__[f"_{official_name}"]
            if official_name in self.__dict__:
                return self.__dict__[official_name]

        if name in self.__dict__:
            return self.__dict__[name]

        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    
    _map = {}
    @classmethod
    def _get_parent(cls, path):
        path = path.strip().strip("/").replace("//", "/")
        if len(path) > 0 and not path.startswith("/"): path = "/" + path
        segments = [s for s in path.split("/")]
        current_path = ""
        current_parent = None
        for i, seg in enumerate(segments[:-1]):
            if current_path not in cls._map:
                existing_node = next((n for n in (current_parent.subways if current_parent else []) if n.path == seg), None)
                new_node = existing_node or Airway(path=seg, is_placeholder=True)    
                cls._map[current_path] = new_node
                if current_parent and not existing_node:
                    current_parent.subways.append(new_node)
            current_parent = cls._map[current_path]
            current_path += "/" + segments[i+1]
        return current_parent

    @classmethod
    def _handle_index(cls, parent:Airway, child:Airway, subways): # child.path = "" and parent

        if parent.path is None:
            raise ValueError(f"[fletfly] Can't add index with path = '' into a pathless parent route.")
        if parent._build or (parent.build_clsattr and parent._class):
            raise ValueError(f"[fletfly] Can't add index with path='' into parent with path='{parent.path}'. Parent already has a view build")
        if getattr(parent, "index", None):
            raise ValueError(f"[fletfly] Parent with path='{parent.path}', already has index. Can't duplicate.")        
        if child._build or (child.build_clsattr and child._class):
            parent.index = child
            if subways:
                print(f"[fletfly] WARNING: index for path='{parent.path}' can't have subroutes. All are ignored.")
            return True
        else:
            raise ValueError(f"[fletfly] Parent with path='{parent.path}' can't have index with no build")
    
    @classmethod
    def _inject_into_tree(cls, route_node, parent_full_path:str = "", parent:Airway = None):
        """
Command Bunker, injection, if there is a path, then create a node in the map.
        """
        airway = None
        subways = []
        if isinstance(route_node, Airway):
            airway = route_node
            subways = airway.subways
            airway.subways = []
        if isinstance(route_node, type):
            airway, subways = cls._airway_from_class(route_node)
        if not airway: return None

        path1 = parent_full_path if parent_full_path else ""
        path2 = airway.path if airway.path else "" 
        path = (path1 + "/" + path2) if path1 or path2 else ""
        path = path.strip().strip("/").replace(" ", "").replace("_","-")
        while "//" in path: path = path.replace("//", "/")
        if len(path) > 0 and not path.startswith("/"): path = "/" + path

        # handling Root
        if airway.path in ("", "/") and path in ("", "/"):
            if not cls._map.get(""): 
                cls._map[""] = airway
            else:
                root_node = cls._map[""]
                if getattr(root_node, "is_placeholder", False):
                    cls._update_tree_subways(airway.subways, root_node.subways)
                    cls._map[""] = airway
                else:
                    cls._check_similarity(airway, root_node, "Router already has a root")
                    airway = root_node
                
        # handling "" index
        elif parent and airway.path == "" and cls._handle_index(parent, airway, subways):
            return airway # handled and airway returned.
        
        # handling path situation
        elif airway.path not in (None, "", "/"):
            airway.path = path.split("/")[-1] if "/" in path else path
            if path in cls._map:
                old_node = cls._map[path]
                if getattr(old_node, "is_placeholder", False):
                    cls._map[path] = airway
                    cls._update_tree_subways(airway.subways, old_node.subways)
                    
                    parent_node = cls._get_parent(path)
                    for i, child in enumerate(parent_node.subways):
                        if child is old_node:
                            parent_node.subways[i] = airway
                            break
                    else: # if not break happened
                        airway = cls._update_tree_subways(parent_node.subways, airway)
                else:
                    cls._check_similarity(airway, old_node, f"Path '{path}' already defined")
                    airway = old_node
            else:
                parent_node = cls._get_parent(path)
                cls._map[path] = airway
                airway = cls._update_tree_subways(parent_node.subways, airway)
        elif parent:
            airway = cls._update_tree_subways(parent.subways, airway)
        else:
            raise ValueError("[fletfly] can't inject pathless airway into the tree")

        if subways:
            for item in subways:
                cls._inject_into_tree(item, path, parent = airway)

        return airway   
    @classmethod
    def _check_similarity(cls, a1:Airway, a2:Airway, err_msg=None)->Airway:
        if (a1.path == a2.path) and (
            a1._class == a2._class) and (( # even if _class = None
            a1.build_clsattr and a2.build_clsattr and a1.build_clsattr == a2.build_clsattr)or(
            a1._build and a2._build and a1._build == a2._build)):
            print(f"[fletfly]: Duplication Warning: Airway route with path='{a1.path}' already added. second registration ignored.")
            return True
        else:
            if err_msg: raise ValueError(err_msg)
            return False
    @classmethod
    def _update_tree_subways(cls, subways, airways:Airway|list[Airway])->Airway|list[Airway]:
        is_single = isinstance(airways, Airway)
        if is_single: airways = [airways]
        resolved = []
        
        for airway in airways:
            add = True
            active_airway = airway
            for brother in subways:
                if airway.path == brother.path and (
                    cls._check_similarity(airway, brother,f"[fletfly] Airway route with path='{airway.path}' already exists.")
                    ):
                    add = False
                    active_airway = brother
                # Ensure both paths exist and contain dynamic parameters using regex
                if airway.path and brother.path and re.search(r"[:{\[]", airway.path) and re.search(r"[:{\[]", brother.path):
                    raise ValueError(
                        f"Parent route already has a dynamic sub-route '{brother.path}'. "
                        f"Cannot add another dynamic route '{airway.path}' at the same level."
                    )
            
            if add: subways.append(airway)
            resolved.append(active_airway)
        return resolved[0] if is_single else resolved
    
    @classmethod
    def _unify_class_subways(cls, _class:type)->list:
        subways = set()
        for attr_name, attr_value in _class.__dict__.items():
            if attr_name.startswith("_"): continue
            if isinstance(attr_value, type):
                if Airline.detect_inner_classes or hasattr(attr_value, "_fletfly_subway"):
                    subways.add(attr_value)
            elif attr_name in aliases["subways"]:
                if attr_value and isinstance(attr_value, (list, tuple)):
                    subways.update(attr_value)
        cls._registered_children_classes.update(subways)

        _class._unified_subways = list(subways)
        for subway in subways:
            cls._unify_class_subways(subway)
        return list(subways)
    
    # creates airway object carrying a 
    @classmethod
    def _airway_from_class(cls, _class:type):
        local_aliases = dict(_rev_aliases)
        def remove_aliases_of(del_key):
            for key in list(local_aliases.keys()): 
                if local_aliases[key] == del_key:
                    del local_aliases[key]

        def inject_attr(airway:Airway, kid_dict:dict):
            for other_name, other_val in kid_dict.items():
                if other_name in _rev_aliases:
                    setattr(airway, other_name, other_val) # keep its name as he called it
                    setattr(airway, _rev_aliases[other_name]+"_clsattr", other_name)
            return airway

        airway_kids = []
        airway = Airway(_class = _class)
        normal_airway = _class.__dict__.keys().isdisjoint(["_fletfly_build","_fletfly_layout", "_fletfly_fly_in", "_fletfly_fly_out"])  

        flagged_attr = []
        # first loop for flagged functions
        for attr_name, attr_val in _class.__dict__.items():
            if isinstance(attr_val, type) or attr_name.startswith("_"): continue

            # Unwrap the underlying function if wrapped in staticmethod or classmethod
            attr_func = attr_val.__func__ if isinstance(attr_val, (staticmethod, classmethod)) else attr_val

            for item_name in ["build", "layout", "fly_in", "fly_out", "subway"]:
                if hasattr(attr_func, f"_fletfly_{item_name}"): # if function has decorator
                    flagged_attr.append(attr_name)
                    kid_dict = {k.replace("_fletfly_", ""):v for k, v in attr_func.__dict__.items() if k.startswith("_fletfly_")}
                    kid_dict.pop(item_name, None)
                    if item_name in ["build", "layout"]:
                        old_clsattr = getattr(airway, f"{item_name}_clsattr", None)
                        if (old_clsattr and old_clsattr != attr_name):
                            raise ValueError(f"[fletfly] class {_class.__name__} already has a {item_name} function named '{old_clsattr}'")
                        else:
                            setattr(airway, f"{item_name}_clsattr", attr_name)
                            remove_aliases_of(item_name)
                        inject_attr(airway, kid_dict)

                    elif item_name in ["fly_in", "fly_out"]:
                        if not hasattr(airway, item_name+"s_clsattr"):
                            setattr(airway, f"{item_name}s_clsattr", [])
                        getattr(airway, f"{item_name}s_clsattr").append(attr_name)
                        inject_attr(airway, kid_dict)

                    elif item_name in ["subway"]: # "subway"
                        sub = Airway(build_clsattr=attr_name, _class=_class)
                        sub = inject_attr(sub, kid_dict)
                        if hasattr(sub, "path_clsattr") and sub.path_clsattr is not None:
                            sub.path = getattr(sub, sub.path_clsattr, None)
                        if sub.path is None and Airline.auto_path_naming:
                            sub.path = attr_name
                        airway_kids.append(sub)
            
            if hasattr(attr_func, "_fletfly_static") and attr_name in local_aliases: # if function has decorator
                flagged_attr.append(attr_name)
                setattr(airway, local_aliases[attr_name], attr_val)
                remove_aliases_of(local_aliases[attr_name])  

        # second loop for any other attr
        for attr_name, attr_val in _class.__dict__.items():
            if isinstance(attr_val, type) or attr_name.startswith("_") or attr_name in flagged_attr: continue
            
            # Unwrap the underlying function if wrapped in staticmethod or classmethod
            attr_func = attr_val.__func__ if isinstance(attr_val, (staticmethod, classmethod)) else attr_val
            
            if attr_name in local_aliases:
                official_name = local_aliases[attr_name]
                if official_name in ["fly_ins", "fly_outs"]:
                    if not hasattr(airway, official_name+"_clsattr"):
                        setattr(airway, official_name+"_clsattr", [])
                    getattr(airway, official_name+"_clsattr").append(attr_name)
                else:
                    # For non-accumulative attributes like path
                    setattr(airway, official_name+"_clsattr", attr_name)
                    remove_aliases_of(local_aliases[attr_name])

            elif callable(attr_val) and(normal_airway and Airline.detect_method_routes ):
                airway_kids.append(Airway(path=attr_name, build_clsattr=attr_name, _class=_class))
    
        # self.path_clsattr = "path" # now
        if getattr(airway, "path_clsattr", None):
            airway.path = getattr(airway._class, airway.path_clsattr) # path = "/something" # now
        
        if airway.path is None and Airline.auto_path_naming and normal_airway:
            name = airway._class.__name__
            name = re.sub(r'(?<!^)(?=[A-Z])', '-', name)
            airway.path = name.lower().replace("_", "-").replace("--", "-")

        class_kids = _class._unified_subways if "_unified_subways" in _class.__dict__ else cls._unify_class_subways(_class)        # returning new Airway, and potential kids of classes
        return airway, class_kids + airway_kids

    @classmethod
    def _append_classes(cls, handed_classes=None):
        if handed_classes is None:
            handed_classes = []
        pending = cls._pending_classes if Airline.detect_decorated_classes else set()
        inherited = set(Airway.__subclasses__()) if Airline.detect_airway_subclasses else set()
        all_classes = set(handed_classes) | pending | inherited
    
        for pot_cls in all_classes:
            cls._unify_class_subways(pot_cls)
        
        for pot_cls in all_classes:
            if pot_cls not in cls._registered_children_classes:
                Airway._inject_into_tree(pot_cls)

    @classmethod
    def _auto_unwrap(cls, zone):
        while isinstance(zone, (list, tuple, set)) and len(zone) == 1:
            collection_type = type(zone).__name__

            print(
                f"\n[fletfly] Optimization Notice: A {collection_type} with only one element was detected. "
                f"Fletfly automatically unpacked it to its core Airway object. ")
            zone = zone[0]
        
        return zone
    
    @classmethod
    def _validate_children(cls, child_ren):
        child_ren = Airway._auto_unwrap(child_ren)
        _validated_list = []

        if isinstance(child_ren, (tuple, list)):
            for obj in child_ren:
                _validated_list.extend(cls._validate_children(obj))
        elif isinstance(child_ren, type):
            _validated_list.append(Airway._airway_from_class(child_ren))  # convert class to Node directly
        elif isinstance(child_ren, Airway):
            _validated_list.append(child_ren)
        elif isinstance(child_ren, dict):
            path = child_ren.get("path") or child_ren.get("name")
            subways_data = child_ren.get("children") or child_ren.get("routes") or child_ren.get("screens")
            
            if isinstance(path, str) or isinstance(subways_data, (list, tuple)):

                subs = child_ren.pop("children", child_ren.pop("routes", child_ren.pop("screens", [])))
                obj = Airway(**child_ren)
                
                if subs: obj.subways.extend(subs)
                
                _validated_list.append(obj)
            else:
                for k, v in child_ren.items():
                    if isinstance(v, Airway):
                        v.route = k
                        _validated_list.append(v)
                    elif callable(v) or hasattr(v, "controls") or hasattr(v, "content"):
                        _validated_list.append(Airway(path=k, build=v))

        return _validated_list

    @classmethod
    def _format_airway_tree(cls, airway, prefix="", is_last=True, is_root=True):
        cls_ = airway._class.__name__ if airway._class else "None"
        path = airway.path if airway.path else "/"
        subways_count = len(airway.subways) if airway.subways else 0
        bld = airway._build.__name__ if airway._build else 'None'
        bld_clsattr = airway.build_clsattr if airway.build_clsattr else 'None'

        marker = "└── " if is_last else "├── "
        output = f"{prefix}{marker}Obj: '{path}' | Class: <{cls_}> | Subways: [{subways_count}] | Build: <{bld}> | Build_clsattr: <{bld_clsattr}>\n"
        
        if airway.subways:
            child_prefix = prefix + ("    " if is_last else "│   ")
            
            output += f"{child_prefix}│\n"
            
            for i, subway in enumerate(airway.subways):
                is_subway_last = (i == len(airway.subways) - 1)
                output += cls._format_airway_tree(subway, child_prefix, is_subway_last, is_root=False)
            
            output += f"{child_prefix}│\n"
        if is_root and output.endswith("│\n"):
            output = output.rstrip("│\n") + "\n"
            
        return output

    def _vampire(self, victim):
        if not victim or self is victim:
            return self
        if victim.parent and not self.parent:
            return victim._vampire(self)
        
        if self.parent and victim.parent:
            raise ValueError(f"[fletfly] Union Error: Both airways have parents. Cannot merge '{self.path}' and '{victim.path}'.")
        
        if self._build and victim._build:
            raise ValueError(f"[fletfly] Union Error: Conflict in 'build'. Both airways provide content for path '{self.path}'.")
        
        if self._layout and victim._layout:
            raise ValueError(f"[fletfly] Union Error: Conflict in 'layout' (layout). Both airways define a layout.")

        for key, value in victim.__dict__.items():
            if key in ('subways', 'fly_ins', 'fly_outs', 'parent'):
                continue
            
            if getattr(self, key, None) is None:
                setattr(self, key, value)
        
        for item in victim.fly_ins:
            if item not in self.fly_ins:
                self.fly_ins.append(item)
        
        for item in victim.fly_outs:
            if item not in self.fly_outs:
                self.fly_outs.append(item)

        if victim.subways:
            for sub in list(victim.subways):
                existing_sub = next((s for s in self.subways if s.path == sub.path), None)
                if existing_sub:
                    existing_sub._vampire(sub)
                else:
                    self.subways.append(sub)

        victim.__dict__.clear()
        return self

def Airzone(zone, path=None):

    if isinstance(zone, dict):
        zone["$air_zone"] = True
    elif isinstance(zone, Airway):
        if path is None or path in ("", "/"):
            raise ValueError("[fletfly] Airway type airzone must have a distinct path path.")
        else:
            zone.path = path
            zone.is_zone = True
    return zone

class FlyPad:
    all_views = "all_views" # all views are active and built
    home_target = "home_target" # main home only & target
    home_ports_target = "home_ports_target" # main and all sub homes & target
    last_port_target = "last_port_target" # last sub home only & target
    all_from_last_port = "all_from_last_port"
    home_last_port_target = "home_last_port_target" # home , last port & target
    home_all_from_last_port = "home_all_from_last_port" # default, which build all views from last port or home to the target
    target_only = "target_only"
# max_pads when <= 0 then every view is allowed.
# max_pads is a periority, and it saves target then main home then nearest parent to target then nearest view to target

class Airline: # singleton only 1 instance
    initial_route = ""
    auto_path_naming = True
    detect_method_routes = True
    detect_airway_subclasses = True
    detect_decorated_classes = True
    detect_inner_classes = True
    _instance = None
    _shared_map = {}
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Airline, cls).__new__(cls)
        else:
            print(f"""
✈️{"="*65}
🚨 [FLETFLY HOLDING GROUP - ARCHITECTURAL NOTICE]
    Fletfly allows only ONE Airline instance to manage your fleet!
✈️{"-" * 65}
1. This single Airline can manage and merge all your Airzones efficiently.
2. The main() function is a 'Travel Agent' that issues tickets to passengers.
3. You MUST NOT create a new Airline for every travel agent; it's a resource leak!
✈️{"-" * 65}
💡 THE ENGINEERING SOLUTION:
   A. Define your Airline instance OUTSIDE the main() scope (Global Scope).
   B. Only call (fly(page, 'path')) INSIDE main() for each new traveler.
✈️{"="*65}
""")
        return cls._instance
    
    def __init__(self, zone_or_class_or_list = [], initial_route = "", error_path:str = "", every_level_fallback=True,
                 fly_pads:FlyPad = FlyPad.home_all_from_last_port, max_pads:int = 5,
                 auto_path_naming=True,
                 detect_decorated_classes=True,
                 detect_airway_subclasses=True,
                 detect_method_routes=True):
        if hasattr(self, "_initialized"):
            return
        Airline.detect_decorated_classes = detect_decorated_classes
        Airline.detect_airway_subclasses = detect_airway_subclasses
        Airline.auto_path_naming = auto_path_naming
        Airline.detect_method_routes = detect_method_routes
        Airline.initial_route = initial_route
        self.error_path = error_path
        self.every_level_fallback = every_level_fallback
        self.fly_pads = fly_pads
        self.max_pads = max_pads
        if isinstance(zone_or_class_or_list, (list, tuple, set)):
            zone_or_class_or_list = list(zone_or_class_or_list)
        else:
            zone_or_class_or_list = [zone_or_class_or_list]
        
        Airway._append_classes(zone_or_class_or_list)
        self.static_map = {} 
        self.dynamic_map = {}

        for key, val in Airway._map.items():
            print (val, "path:", key)
        final_airway = Airway._map.get("", None)
        if not final_airway:
            raise ValueError(f"[fletfly] There are no routes to handle...")
        self._parse_airways(final_airway)

        print("----------------------- static map ---------------------")
        for item in self.static_map.values(): print(item)
        print("----------------------- dynamic map ---------------------")
        for item in self.dynamic_map.values(): print(item)
        self._initialized = True
    
    class _FlightNode:
        __slots__ = [
            'seg', # ':id'
            'path', # '/segment1/zonesegment1/segment2/:id'
            'take_off_zone', # '/segment1/zonesegment1/'
            'lineage', # [flight_node, flight_node]
            'build_node',
            'fly_ins', # [{"func":func1, "args":args, "takeoff":'/'}]
            'fly_outs', # [{"func":func2, "args":args, "takeoff":'/'}]
            'fly_to', 'fly_to_clsattr', # redirect, redirectTo
            'layout_nodes', # list of layoutNodes
            'title','title_clsattr', # title
            'icon','icon_clsattr', # icon
            'build_hero', 'build_hero_clsattr',
            'layout_hero', 'layout_hero_clsattr',
            'is_zone', # False as default
            '_class',
            'regex', # None as default for dynamic nodes
            ]

        def __init__(self, **kwargs):
            for slot in self.__slots__:
                setattr(self, slot, kwargs.get(slot, None))
            
            if self.is_zone is None: self.is_zone = False
            if self.lineage is None: self.lineage = []
            if self.fly_ins is None: self.fly_ins = []
            if self.fly_outs is None: self.fly_outs = []
            if self.layout_nodes is None: self.layout_nodes = []

        @property
        def is_dynamic(self):
            return ":" in self.path or ("[" in self.path and "]" in self.path)

        def __repr__(self):
            builds = self.build_node.func if self.build_node else "N/A"
            if isinstance(builds, str) and not builds.endswith("()"):
                builds = f'"{builds}"'
            elif builds is None:
                builds = ""
            layout_nodes = f"[{len(self.layout_nodes)}]"
            
            
            return f"layouts={layout_nodes}  build={builds} fly_to={self.fly_to}  {self.path}"
         
    class FlyBox:
        def __init__(self, page):
            self.params = {}        # المعاملات (مثل :id)
            self.query = {}       # معاملات الاستعلام
            self.fly_ins_radar = "/"        # المسار اللحظي للميدل وير
            self.fly_ins_is_target = False # هل وصلنا للمحطة النهائية؟
            self.take_off_zone = "/"     # نقطة انطلاق اليوزر
            self.last_success_path = "/" # لعمل Rollback عند الخطأ
            self.is_navigating = False
            self.closing_view = None    # the view which is closing for fly_outs
            self._slots_map = {}
            self._layouts = set()
            self._new_layouts = set()
            self._arounds = set()
            self._new_arounds = set()
            self._build_heros = {}
            self.page = page
            self._temp_data = [] # list of controls to update

        def __call__(self, path: str = "/"):
            target = f"{self.take_off_zone}{path.strip('/')}".replace("//", "/")
            if target == "/": target = ""
            self.page.run_task(self.page.push_route, target)
    
    @classmethod
    def radar(self_or_cls, root_dir=None, base_path = "/", skip_conflicts = True, auto_naming=False):
        cls = self_or_cls if isinstance(self_or_cls, type) else self_or_cls.__class__
        
        if not root_dir: root_dir = os.getcwd()
        cls.detect_method_routes = auto_naming
        
        base_path = "/" + base_path.strip("/")
        if base_path == "/": base_path = ""
        
        scanned_zone = cls._scan_folder(root_dir)

        if cls._instance is None:
            return Airline(zone_or_class_or_list=scanned_zone)
        else:
            if scanned_zone:
                Airway._validate_airway_final(scanned_zone)
                
                static_map, dynamic_map = cls._instance._parse_airways(scanned_zone,scanned_zone, 
                    current_full_path=base_path)
                cls._instance._safe_merge(cls._instance.static_map,
                                          cls._instance.dynamic_map, static_map, dynamic_map, skip_conflicts)

            return cls._instance
    
    def _scan_file(cls, file_path, file_or_folder_name, main_obj = None): # main_obj value for folders
        _orphans = []
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for name, obj in inspect.getmembers(module):
            if isinstance(obj, Airway):
                if obj.parent is None:
                    if obj.path in (None, "", "/"):
                        if main_obj is None:
                            main_object = obj
                            main_object.path = file_or_folder_name
                        else:
                            if (obj._build is None or main_obj._build is None) and (obj._layout is None or main_obj.layout is None):
                                main_object._vampire(obj)
                            elif ((obj._build and main_object._build) or (obj._layout and main_object._layout)) and (
                                obj.path in ("", "/") or (obj.path is None and not cls.detect_methods_routes)):
                                    raise ValueError(f"[fletfly] Double pathless routes in {file_or_folder_name}.py"
                                                    f"           pathless route in page.py, index.py or main.py is a folder master route")
                            else:
                                obj.path = name.strip("_").lower().replace("_","-")
                                _orphans.append(obj)
                                pass
                    else:
                        # no father but with path
                        _orphans.append(obj)
        if _orphans:
            if main_object is None : main_object = Airway(route = file_or_folder_name)
            main_object.subways.extend(_orphans)
        return main_object
    
    @classmethod
    def _scan_folder(cls, folder_path):
        folder_name = os.path.basename(folder_path)
        main_obj = None
        #dict for .py files in the folder
        files = {f: os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.py')}
        for page_file in ['page.py', 'index.py', 'main.py', 'layout.py', 'layout.py', 'fly_ins.py', 'fly_outs.py', 'middlewares.py']:
            if page_file in files:
                main_obj = cls._scan_file(files[page_file], folder_name, main_obj)
                del files[page_file]
        if not main_obj:
            main_obj = Airway(path=folder_name) # full path is handled by parsing

        for remaining_file in files.values():
            file_name = os.path.splitext(os.path.basename(remaining_file))[0]
            sub_object = cls._scan_file(remaining_file, file_name, main_obj = None)
            if sub_object:
                main_obj.subways.append(sub_object)

        for entry in os.scandir(folder_path):
            if entry.is_dir() and not entry.name.startswith(('_', '.')):
                sub_child = cls._scan_folder(entry.path)
                if sub_child:
                    main_obj.subways.append(sub_child)
        return main_obj

    def _handle_route_change(self, e):
        
        if not e.page.views or (e.page and e.page.route and e.page.views[-1].route and e.page.route != e.page.views[-1].route):
            e.page.run_task(self._navigate, e.page)

    async def _handle_view_pop(self, e):
        
        if len(e.page.views)>1:
            v2 = e.page.views[-2]
            params = getattr(v2, "params", {})
            query = getattr(v2, "query", {}) 
        await self._reconcile_views(e.page, [v.node for v in e.page.views[:-1]])
        e.page.fly.params = getattr(v2, "params", {})
        e.page.fly.query = getattr(v2, "query", {})
        await e.page.push_route(v2.route)
        """
        
        try:
            fly_outs_check = True
            if e.view is not None and not getattr(e.page, "_is_navigating", False):
                e.page.fly._is_navigating = True
                fly_outs_check = await self._apply_fly_outs_checks(e.page, e.view)
                Airline._BuildObj._save_build_hero(e.page, e.view)
                e.page.views.remove(e.view)
                if e.page.views:
                    top_view = e.page.views[-1]
                    e.page.fly.take_off_zone = top_view.take_off_zone
                    e.page.fly.params = getattr(top_view, "params", {})
                    e.page.fly.query = getattr(top_view, "query", {})
                    await e.page.push_route(top_view.route)
            if fly_outs_check != True:
                await asyncio.sleep(0.2)
                e.page.views.append(e.view)
                await e.page.push_route(e.page.fly.last_success_path)
        finally:
            await asyncio.sleep(0.2)
            e.page.fly._is_navigating = False 
"""

    def _get_path_fingerprint(self, path): # for matching dynamics :id == [user-id]
        f_path = re.sub(r':[a-zA-Z0-9_]+', '<?>', path)
        f_path = re.sub(r'\[[a-zA-Z0-9_]+\]', '<?>', f_path)
        f_path = re.sub(r'\{[a-zA-Z0-9_]+\}', '<?>', f_path)
        return f_path

# region Parse
    def _get_sync_layout_chain(self, in_out_build_list:list[Airline._LayoutNode], in_out_lay="lay"):
        if not in_out_build_list: return []
        current_class = getattr(in_out_build_list[-1], "_class", None)
        final_list = []
        if in_out_lay == "lay":
            temp_list = list(in_out_build_list)
        else: 
            temp_list = []
            for item in in_out_build_list:
                temp_list.append(item)
        # get 
        for i in range(len(temp_list)-1,-1,-1):
            layout_node = temp_list[i]
            if layout_node.func and callable(layout_node.func): # func method saved
                final_list.insert(0, layout_node.func)
            if layout_node._class:
                if layout_node.method_name:
                    func = getattr(layout_node._class, layout_node.method_name)
                    if func and callable(func):
                        final_list.insert(0, func)
                if layout_node.override_clsattr:
                    if getattr(layout_node._class, layout_node.override_clsattr, True if in_out_lay == "out" else False):
                        break
        return final_list
        
    # start point
    # create node
    # chick if children for each go to start point
    def _parse_airways(self, airway:Airway, parent_lineage=None, 
                       current_full_path="/", current_take_off_zone="/",
                        p_fly_ins=[], p_fly_outs=[], p_layout_nodes=[]):
        true_node = airway._build or airway.build_clsattr or airway.fly_to or airway.fly_to_clsattr
        if true_node or airway.subways:
            seg = airway.path.strip("/") if airway.path else ""
            raw_path = f"{current_full_path.rstrip('/')}/{seg.strip('/')}"
            current_lineage = parent_lineage.copy() if parent_lineage else []
            take_off_zone = raw_path.rstrip("/") + "/" if airway.is_zone else current_take_off_zone
            # no build then absolutely no page to see
            if airway._class:
                over = {"_class":airway._class, "over":airway.fly_ins_override}
                attr = {"_class":airway._class, "attr":airway.fly_ins_override}
                local_fly_ins = [over, attr]
                for dic in local_fly_ins: dic["take_off_zone"] = current_take_off_zone
                fly_ins = p_fly_ins + local_fly_ins
                over = {"_class":airway._class, "over":airway.fly_outs_override}
                attr = {"_class":airway._class, "attr":airway.fly_outs_override}
                local_fly_outs = [over, attr]
                for dic in local_fly_outs: dic["take_off_zone"] = current_take_off_zone
                fly_outs = p_fly_outs + local_fly_outs
            else:
                fly_ins = _FlyList([d for d in p_fly_ins if d.get("inheritable", True) or d.get("apply_per_view", False)])
                fly_outs = _FlyList([d for d in p_fly_outs if (d.get("inheritable", False) or d.get("apply_per_view", False))])#must inherit if apply per view
                local_fly_ins = _list_middlewares(airway.fly_ins)
                local_fly_outs = _list_middlewares(airway.fly_outs)
                for dic in local_fly_ins: dic["take_off_zone"] = current_take_off_zone
                for dic in local_fly_outs: dic["take_off_zone"] = current_take_off_zone
                fly_ins = _FlyList(local_fly_ins) if airway.fly_ins_override else _FlyList(fly_ins + list(local_fly_ins))
                fly_outs = _FlyList(local_fly_outs) if airway.fly_outs_override else _FlyList(list(local_fly_outs) + fly_outs)
            
            build_node = None
            layout_node = None
            if airway._class:
                if airway.build_clsattr and getattr(airway._class, airway.build_clsattr):
                    build_node = Airline._BuildNode(func=None, _class=airway._class, method_name=airway.build_clsattr,
                                                    hero_clsattr=airway.build_hero_clsattr, 
                                                    post_fly_clsattr=airway.post_fly_clsattr)
                if (airway.layout_clsattr and getattr(airway._class, airway.layout_clsattr)) or(
                    airway.layout_override_clsattr and getattr(airway._class, airway.layout_override_clsattr)):
                    layout_node = Airline._LayoutNode(func=None, _class=airway._class, method_name=airway.layout_clsattr,
                                                      override_clsattr=airway.layout_override_clsattr,
                                                      hero_clsattr=airway.layout_hero_clsattr, 
                                                    post_fly_clsattr=airway.post_fly_clsattr)
            else:
                if airway._build:
                    build_node = Airline._BuildNode(func=airway._build, hero_var=airway.build_hero,
                                                    post_fly_func=airway.post_fly)
                if airway._layout:
                    layout_node = Airline._LayoutNode(func=airway._layout, hero_var=airway.layout_hero,
                                                      post_fly_func=airway.post_fly, override_var = airway.layout_override)
                
            layout_nodes = list(p_layout_nodes) + ([layout_node] if layout_node else [])

            if true_node:
                node = Airline._FlightNode(
                    seg=airway.path,
                    path=raw_path,
                    take_off_zone=take_off_zone,
                    title=airway.title,
                    title_clsattr = airway.title_clsattr,
                    icon= airway.icon,
                    icon_clsattr= airway.icon_clsattr,
                    build_node = build_node,
                    fly_to = airway.fly_to,
                    fly_to_clsattr = airway.fly_to_clsattr,
                    is_zone=airway.is_zone,
                    layout_nodes=layout_nodes, 
                    lineage=current_lineage,
                    fly_ins=fly_ins,
                    fly_outs=fly_outs,
                    _class=airway._class
                )
                
                if node.is_dynamic:
                    node.regex = self._generate_regex(raw_path)
                    self.dynamic_map[node.regex] = node
                else:
                    self.static_map[raw_path] = node
                current_lineage = (current_lineage.copy() if current_lineage else []) + [node]

                

            if airway.subways:
                for subway in airway.subways:
                    self._parse_airways(subway, current_lineage, raw_path, take_off_zone, fly_ins, fly_outs, layout_nodes)
                    #self._safe_merge(self.static_map, self.dynamic_map, child_static, child_dynamic)

    def _safe_merge(self, main_static, main_dynamic, static, dynamic, skip_conflicts = False):
        
        for path, node_obj in static.items():
            if path in main_static:
                if not skip_conflicts:
                    raise ValueError(f"🚨 Static Pattern Collision: '{path}' is repeated.")
            else:
                main_static[path] = node_obj

        for regex_obj, node_obj in dynamic.items():
            new_fp = self._get_path_fingerprint(node_obj.path)
            collision_found = False
            
            for existing_node in main_dynamic.values():
                existing_fp = self._get_path_fingerprint(existing_node.path)
                
                if new_fp == existing_fp:
                    collision_found = True
                    if not skip_conflicts:
                        raise ValueError(f"🚨 Dynamic Collision: '{node_obj.path}' matches structure of '{existing_node.path}'")
                    break 
            
            if not collision_found:
                main_dynamic[regex_obj] = node_obj
      
        return main_static, main_dynamic

    def _generate_regex(self, path_pattern):
        pattern = "/" + path_pattern.strip("/")

        pattern = re.sub(r'\[([a-zA-Z0-9_]+)\]', r'(?P<\1>[^/]+)', pattern)

        regex_pattern = re.sub(r':([a-zA-Z0-9_]+)', r'(?P<\1>[^/]+)', pattern)  

        regex_pattern = re.sub(r'\{([a-zA-Z0-9_]+)\}', r'(?P<\1>[^/]+)', regex_pattern)
        return re.compile(f"^{regex_pattern}$")
# endregion

# region Navigate
    async def _navigate(self, page, fullpath = None):
        print(1111111111111111111)
        start = time.perf_counter()
        print(f"Time taken: {(time.perf_counter() - start) * 1000:.2f}ms")
        
        path, query = self._get_path_query(page, fullpath)
        
        node, params = self.match_path(path)
        if self._check_fly_to(page, node): return None

        if not node:
            node, params = self._handle_fallback(page, node, path) 
        if not node:
            return None

        if self._check_fly_to(page, node): return None
        
        #await self._apply_animation(page, node)

        page.fly.params = params if params else {}
        page.fly.query = query if query else {}

        step1 = self._apply_fly_pads(node) 
        
        step2 = await self._apply_fly_ins_checks(page, step1, node)

        if not step2: return
        
        step3 = self._apply_max_pads(step2)
        
        await self._reconcile_views(page, step3)

        print(f"Time taken: to end of _navigate before page.update {(time.perf_counter() - start) * 1000:.2f}ms")
        page.update()

    def _get_path_query(self, page, fullpath = None):

        query = {}
        if fullpath is None: fullpath = page.route
        #Query
        path_query = fullpath.split("?")
        path = "/" + path_query[0].lower().strip("/")
        query_str = path_query[1] if len(path_query) > 1 else ""
        if query_str:
            for pair in query_str.split("&"):
                if "=" in pair:
                    k, v = pair.split("=", 1)
                    query[k] = v # inject query in page
        return path, query

    def match_path(self, path):
        print(f"---------- match path = {path} ----------")
        
        path = path.rstrip("/")
        if not path: path = "/"
        if path in self.static_map:
            
            node:Airline._FlightNode = self.static_map[path]
            return node, {}

        for pattern in reversed(list(self.dynamic_map.keys())):
            match = pattern.match(path)
            if match:
                node:Airline._FlightNode = self.dynamic_map[pattern]
                return node, match.groupdict()

        return None, {}

    def _check_fly_to(self, page, node):
        if node:
            to = node.fly_to
            if to is None and node.fly_to_clsattr and node._class and isinstance(node._class, type):
                 to = getattr(node._class, node.fly_to_clsattr, None)
            if to is not None:
                page.run_task(page.push_route, node.fly_to)
                return True
        return False

    def _handle_fallback(self, page, node=None, path=None, build_failed=False):
        params = {}
        if not node or build_failed:
            if build_failed: print(f"[fletfly] Failed to create a build for route {path}")
            if self.every_level_fallback:
                temp_path = path.rstrip("/")
                while True:
                    if "/" in temp_path:
                        temp_path = temp_path.rsplit("/", 1)[0]
                    else:
                        temp_path = ""
                    
                    fallback_path = (temp_path + "/*") if temp_path else "/*"
                    node, params = self.match_path(fallback_path)
                    
                    if node or not temp_path:
                        break
            if not node and self.error_path:
                current_zone_error = (page.fly.take_off_zone.rstrip("/") + "/" + self.error_path.strip("/"))
                node, params = self.match_path(current_zone_error)
                if not node:
                    node, params = self.match_path("/" + self.error_path.strip("/"))
            if not node:
                self._default_error_view(page)
                return None, None
        return node, params
    
    async def _apply_animation(self, page, node:_FlightNode):
        theme = "zoom"
        if node.path.strip("/") == "resizer":
            theme = "cupertino"
        elif node.path.strip("/") == "resizer/about":
            theme = "fade_upwards"
        if isinstance(theme, ft.PageTransitionsTheme):
            page_transitions = theme
        else:
            if not isinstance(theme, str):
                theme = "none"
            t = getattr(ft.PageTransitionTheme, theme.upper(), ft.PageTransitionTheme.NONE)
            page_transitions = ft.PageTransitionsTheme(android=t, ios=t, macos=t, linux=t, windows=t)
        
        new_theme = page.theme if page.theme else ft.Theme()
        new_theme.page_transitions = page_transitions
        page.theme = new_theme
        await asyncio.sleep(1)
        """
        page.theme = ft.Theme(
            page_transitions=ft.PageTransitionsTheme(
            android=ft.PageTransitionTheme.FADE_UPWARDS,
            ios=ft.PageTransitionTheme.FADE_UPWARDS,
            macos=ft.PageTransitionTheme.FADE_UPWARDS,
            linux=ft.PageTransitionTheme.FADE_UPWARDS,
            windows=ft.PageTransitionTheme.FADE_UPWARDS,
        ))

        """
        

    def _apply_fly_pads(self, node:_FlightNode):
        if self.fly_pads == FlyPad.target_only or node.path == "/":
            return [node]
        
        full_chain = node.lineage + [node]
        home_node = full_chain[0]

        if self.fly_pads == FlyPad.home_target:
            return [home_node, node]

        if self.fly_pads == FlyPad.last_port_target:
            last_port = next((n for n in reversed(node.lineage) if n.is_zone), None)
            return [last_port, node] if last_port else [home_node, node]

        if self.fly_pads == FlyPad.home_last_port_target:
            last_port = next((n for n in reversed(node.lineage) if n.is_zone), None)
            if last_port and last_port != home_node:
                return [home_node, last_port, node]
            return [home_node, node]

        if self.fly_pads == FlyPad.home_ports_target:
            wishlist = [n for n in full_chain if n.is_zone]
            if node not in wishlist: wishlist.append(node)
            return wishlist

        if self.fly_pads == FlyPad.all_from_last_port:
            last_port_idx = next((i for i, n in enumerate(reversed(full_chain)) if n.is_zone), None)
            if last_port_idx is not None:
                actual_idx = len(full_chain) - 1 - last_port_idx
                return full_chain[actual_idx:]
            return full_chain

        if self.fly_pads == FlyPad.home_all_from_last_port:
            last_port_idx = next((i for i, n in enumerate(reversed(full_chain)) if n.is_zone), None)
            if last_port_idx is not None:
                actual_idx = len(full_chain) - 1 - last_port_idx
                if actual_idx == 0: return full_chain
                return [home_node] + full_chain[actual_idx:]
            return full_chain

        return full_chain
    
    async def _apply_fly_ins_checks(self, page, nodes_chain, target_node):
        return nodes_chain
        filtered_chain = []
        excuted_fly_ins_out = set()
        for current_node in nodes_chain:
            is_final = (current_node == target_node)
            check = self._run_node_fly_ins_out(page, "in", None, current_node, is_final, excuted_fly_ins_out)
            
            if inspect.isawaitable(check):
                check = await check

            if check is True:
                filtered_chain.append(current_node)
            
            elif isinstance(check, str):
                print(f'🔀 [fletfly] Redirecting from "{page.route}" to "{check}"')
                page.run_task(page.push_route, check)
                return None
            else:
                if page.route != page.fly.last_success_path:
                    print(f"🚫 [fletfly] Access Denied. Rolling back to: {page.fly.last_success_path}")
                    page.on_route_change = None 
                    page.go(page.fly.last_success_path)
                    page.on_route_change = self._handle_route_change
                return None
        return filtered_chain
    
    async def _artificial_back(self,page, response, view):
        result = await response
        if result is True:
            view.fly_outs_approved = True
            if page.views and len(page.views) > 1:
                if page.views[-1] == view:
                    for i in range(len(page.views)-1, -1, -1):
                        if page.views[i] != view:
                            print("[_artificial_back] views count:", len(page.views))
                            print("[_artificial_back] page.views[i].route:", page.views[i].route)
                            await page.push_route(page.views[i].route)
                            page.update()
                            return

    async def _apply_fly_outs_checks(self, page, view):
        return True
        if getattr(view, "fly_outs_approved", False): # already checked
            return True
        
        node = getattr(view, "node", None)
        
        if not node: return True # its ok to leave, can't stop you

        check = self._run_node_fly_ins_out(page, in_out="out", view=view, node=node, is_building=True, excuted_fly_ins_out=set())

        if inspect.isawaitable(check):
            await page.push_route(view.route)
            page.run_task(self._artificial_back, check, view)
            return False
        if isinstance(check, str):
            print(f'🔀 [fletfly] Redirecting to "{page.route}" to "{check}"')
            page.run_task(page.push_route, check)
            return False
        elif check == False:
            print(f'🚫 [fletfly] Leaving is Cancelled. Staying at: "{page.fly.last_success_path}"')
            await page.push_route(page.fly.last_success_path)
            return False
        
        return True #any other case scenario

    def _run_node_fly_ins_out(self, page, in_out, view, node:_FlightNode, is_building, excuted_fly_ins_out:set):

        if node._class:
            attr = getattr(node, f"fly_{in_out}", None)
            if attr :
                chain = self._get_sync_layout_chain(getattr(node , f"fly_{in_out}"), in_out)
                fly_ins_out = _list_middlewares(chain)
        else:
            fly_ins_out = getattr(node, f"fly_{in_out}", [])
        last_res = True
        page.fly.is_building = is_building
        page.fly.fly_ins_radar = node.path
        if view: page.fly.closing_view = view
        
        try:
            for mw in fly_ins_out:
                if mw.get("apply_per_view", False) or id(mw) not in excuted_fly_ins_out:
                    func = mw["func"]
                    last_res = func(page, *mw["args"], **mw["kwargs"])
                    if inspect.isawaitable(last_res):
                        print(f"ℹ️ [fletfly] Fly_{in_out} at '{node.path}' returned awaitable response.")
                        print(f"ℹ️ Only 1 awaitable response is allowed per View, all remaining fly_{in_out} will be ignored.")
                        return last_res

                    # --- [ الحركة الشياكة المحدثة ] ---
                    if not isinstance(last_res, (bool, str)):
                        print(f"ℹ️ [fletfly] Fly_{in_out} at '{node.path}' returned {type(last_res).__name__} ('{last_res}').")
                        print(f"    We treated it as {'False for security' if in_out == "in" else 'True'}. (Expected: True, False, or Redirect String)")
                        # بنحولها لـ False عشان الـ Logic اللي بعد كدة يفهم إنها مرفوضة
                        last_res = False if in_out == "in" else True

                    if isinstance(last_res, str):
                        last_res = mw.get("take_off_zone", node.take_off_zone if node.take_off_zone else "/").rstrip("/") + "/" + last_res.lstrip("/")
                        print(f"🔀 [fletfly] Redirect by '{mw["func"].__name__}' at '{node.path}':")

                    if last_res is not True:
                        break # هيخرج فوراً بالـ False أو الـ String
                    excuted_fly_ins_out.add(id(mw))
                else:
                    continue
        except Exception as e:
            # لو الميدل وير نفسه فيه خطأ برمجيا
            print(f"❌ [fletfly] Critical error in middleware at '{node.path}': {e}")
            last_res = False # نمنع الدخول للأمان    
        finally:
            pass
        return last_res

    def _apply_max_pads(self, wishlist):

        if self.max_pads <= 0 or len(wishlist) <= self.max_pads:
            return wishlist

        target = wishlist[-1]
        home = wishlist[0]
        
        remaining_slots = self.max_pads - 2 
        middle_candidates = wishlist[1:-1]
        survivors = middle_candidates[-remaining_slots:] if remaining_slots > 0 else []

        final_list = [home] + survivors + [target]
        
        if self.max_pads == 1:
            return [target]

        return final_list
    
    async def _reconcile_views(self, page, final_nodes_list):
        #if page.views: print("start of reconcile in view value:", page.views[-1].controls[0].content.controls[0].value)
        #if page.views: print("start of reconcile in view value:", id(page.views[-1].controls[0].content.controls[0]))
        page.fly._temp_data = []
        page.fly._new_layouts = set()
        page.fly._new_arounds = set()
        
        existing_layouts = page.fly._layouts
        #if existing_layouts: print("start of reconcile existing_layouts value:", existing_layouts[0].objs_map[''][0].content.controls[0].value)#.content.controls[0].value)
        #if existing_layouts: print("start of reconcile existing_layouts value:", id(existing_layouts[0].objs_map[''][0].content.controls[0]))#.content.controls[0].value)
        
        Airline._LayoutObj._dismount_obj_s(existing_layouts)

        final_paths = [self._get_real_path(page.route, n.path) if n.is_dynamic else n.path for n in final_nodes_list]

        for i in range(len(page.views) - 1, -1, -1):
            vi = page.views[i]
            if vi.route not in final_paths and await self._apply_fly_outs_checks(page, vi):
                Airline._BuildObj._save_build_hero(page, vi)
                page.views.pop(i)
        
        for index, flight_node in enumerate(final_nodes_list):
        
            layout_objs = Airline._LayoutObj._get_layout_objs(page, flight_node)

            existing_view = next((v for v in page.views if v.route == final_paths[index]), None)
            build_obj = None
            pre_view = None
            if existing_view:
                build_obj = existing_view._fly_build_obj if hasattr(existing_view, "_fly_build_obj") else None
                Airline._BuildObj._save_build_hero(page, existing_view)
                page.views.remove(existing_view)
            
            if not build_obj:
                if flight_node.is_dynamic:
                    build_obj = page.fly._build_heros.get(flight_node.path, {}).get(final_paths[index], None)
                else:
                    build_obj = page.fly._build_heros.get(flight_node.path, None)
            if not build_obj or not isinstance(build_obj, Airline._BuildObj):
                build_obj = Airline._BuildObj._create_build_obj(page, flight_node.build_node )

            all_objs = ([build_obj] if build_obj else []) + (list(reversed(layout_objs)) if layout_objs else [])
            #inject fly_arounds and record them
            active_arounds = Airline._AroundObj._inject_around_objs(page, all_objs)            

            final_obj = None
            for i, obj in enumerate(all_objs):
                final_obj = obj
                if final_obj and final_obj.objs_map.get("") and isinstance(final_obj.objs_map[""][0], ft.View):
                        pre_view = final_obj.objs_map[""][0]
                        if i < len(all_objs) - 1:
                            print("[fletfly] ft.View is a top most control, you can't inject in a layout, further layout/s will be ignored")
                        break 
                if i < len(all_objs) - 1:
                    Airline._LayoutObj._inject_into_layout(page, final_obj, all_objs[i+1])

            if not pre_view and final_obj:
                nameless_content = final_obj.objs_map.get("", [])
                all_keys = [k for k in final_obj.objs_map.keys() if k != ""]
                
                if nameless_content:
                    if all_keys:
                        print(f"[fletfly] WARNING: Unused named slots detected {all_keys} in final Layout. These will be ignored.")                 
                    pre_view = ft.View(controls=nameless_content)
                elif all_keys:
                    if index< len(final_nodes_list) -1:
                        print(f"[fletfly] WARNING: No view nor unnamed controls in Final Layout, only named {all_keys}")
                        final_obj = None
                    else:
                        raise ValueError(f"[fletfly] Critical Error: The final layout has no nameless content to build the view, but contains orphaned named slots: {all_keys}.")
                else:
                    final_obj = None
            if not final_obj:
                print(f"[fletfly] failed to build view of path '{'/' + flight_node.path.strip('/')}'")                
                if index < len(final_nodes_list) - 1:
                    print(f"passing to the next view in the final list")
                    continue
                else:
                    self._handle_fallback(page, None, flight_node.path, True)             
                    return None
                
            #if not top-view
            if index < len(final_nodes_list)-1:
                #create a shallow clone copy of the view_final (layouts and builds)
                final_view = Airline._LayoutObj._clone_control(pre_view)
                Airline._LayoutObj._dismount_obj_s(all_objs)

            else: # top view
                final_view = pre_view

            page.views.append(final_view)
            
            page.fly.take_off_zone = flight_node.take_off_zone
            final_view.take_off_zone = flight_node.take_off_zone
            final_view.route = self._get_real_path(page.route, flight_node.path) if flight_node.is_dynamic else flight_node.path
            final_view.params = dict(page.fly.params) # to restore on back
            final_view.query = dict(page.fly.query) # to restore on back
            final_view.node = flight_node
            final_view._fly_build_obj = build_obj
        page.fly._layouts = page.fly._new_layouts | {x for x in page.fly._layouts if x.hero}
        page.fly._arounds = page.fly._new_arounds | {x for x in page.fly._arounds if x.hero}
        page.fly.last_success_path = page.route
        
    def _get_real_path(self, main_path, node_path):
        main_segments = main_path.split("?")[0].strip("/").split("/")
        node_segments = node_path.strip("/").split("/")

        if not node_segments or node_segments == [""]:
            return "/"
        
        result_path = []
        
        for i in range(len(node_segments)):
            if i < len(main_segments):
                result_path.append(main_segments[i])
            else:
                break
        return "/" + "/".join(result_path)

    @classmethod
    def _get_sync_func(cls, node):
        if node is None:
            return None
        if node._class and node.method_name: # dynamic func
            return getattr(node._class, node.method_name)
        elif node.func: #
            return node.func
        return None    
    @classmethod
    def _get_sync_hero(cls, node)->int|bool:
        if node is None:
            return None
        if node._class and node.hero_clsattr: # dynamic func
            return getattr(node._class, node.hero_clsattr)
        elif node.hero_var:
            return node.hero_var
        return None    
    class _AroundNode: # one node created for one build for all times
        def __init__(self, func=None, _class=None, method_name=None, name=None,
                     hero_var=None, hero_clsattr=None,
                     post_fly_func=None, post_fly_clsattr=None):
            self.func = func #function
            self.method_name = method_name
            self._class = _class #class
            self.hero_var = hero_var #function
            self.hero_clsattr = hero_clsattr
            self.post_fly_func = post_fly_func
            self.post_fly_clsattr = post_fly_clsattr
            if name:
                self.name = name
            else: 
                if not Airline.detect_methods_routes:
                    raise ValueError("[fletfly] shared build must have a name, or you can turn on auto_func_naming")
                else:
                    if func and callable(func):
                        self.name = func.__name__
                    elif _class and method_name:
                        self.name = _class.__name__ + "_" + method_name
                    else:
                        raise ValueError("[fletfly] shared build must have a name")
                    print(f"[fletfly] fly_around shared function auto named to {self.name}")
            if self.name in Airline._shared_map:
                raise ValueError(f"[fletfly] shared content with name {self.name} is already registered")
            else:
                Airline._shared_map[self.name] = self   
        @classmethod
        def _get_node(cls, name):
            if not isinstance(name, str):
                print(f"[fletfly] fly_around expects string name as first argument, but got '{type(name)}'")
            elif name in Airline._shared_map:
                return Airline._shared_map[name]
            else:
                print(f"[fletfly] can't find fly_around shared component with name '{name}'")

    class _AroundObj:# carrying views (multiple) views info about the build
        def __init__(self, obj:ft.Control, around_node:Airline._AroundNode=None, hero:bool=None):
            self.obj = obj
            self.around_node = around_node
            if hero is None:
                if around_node._class and around_node.hero_clsattr:
                    self.hero = getattr(around_node._class, around_node.method_name)
                else:
                    self.hero = around_node.hero_var
            if self.hero is None:
                self.hero = True
        @classmethod
        def _create_around(cls, page, around_node:Airline._AroundNode):
            func = Airline._get_sync_func(around_node)
            
            if not func: return None
            if not callable(func):
                raise ValueError(_page_err_msg)
            obj = func(page)
            if not isinstance(obj, ft.Control):
                print(f"[fletfly] A fly_around shared build must be a function taking page argument and returning ft.Control")
                return None
            return Airline._AroundObj(obj, around_node)
        @classmethod
        def _get_active_around(cls, page, around_node):
            
            around_obj = None
            for ar in page.fly._arounds | page.fly._new_arounds:

                if ar.around_node == around_node:
                    around_obj = ar
                    break                   
            if around_obj is None:
                around_obj = Airline._AroundObj._create_around(page, around_node)
            if around_obj:
                page.fly._new_arounds.add(around_obj)
                return around_obj
            return None
        @classmethod
        def _inject_around_objs(cls, page, objs:list[Airline._LayoutObj|Airline._BuildObj]):
            active_around_objs = []
            for obj in objs:
                if obj.around_holders and obj.around_nodes:
                    for holder, node in zip(obj.around_holders, obj.around_nodes):
                        if holder and node:
                            active_around_obj = cls._get_active_around(page, node)
                                                        
                            if active_around_obj:
                                holder.content = active_around_obj.obj
                                if active_around_obj not in active_around_objs:
                                    active_around_objs.append(active_around_obj)
            return active_around_objs
        
    class _BuildNode: # one node created for one build for all times
        def __init__(self, func=None, _class=None,
                    method_name=None, 
                     hero_var=None, hero_clsattr=None,
                     post_fly_func=None, post_fly_clsattr=None,):
            self.func = func #function
            self.method_name = method_name
            self._class = _class #class
            self.hero_var = hero_var #function
            self.hero_clsattr = hero_clsattr
            self.post_fly_func = post_fly_func
            self.post_fly_clsattr = post_fly_clsattr

    class _BuildObj:# carrying views (multiple) views info about the build
        def __init__(self, objs_map=None, around_holders = None, around_nodes = None,
                      build_node:Airline._BuildNode=None, hero:bool=None):
            self.objs_map = objs_map # {"named1":controloraroundnode, "":[unnamed1, unnamed2]}
            self.build_node = build_node
            self.around_holders = around_holders
            self.around_nodes = around_nodes
            if hero is None:
                if build_node._class and build_node.hero_clsattr:
                    self.hero = getattr(build_node._class, build_node.method_name)
                else:
                    self.hero = build_node.hero_var
            if self.hero is None:
                self.hero = False
        @classmethod
        def _dismount_build(cls, build:Airline._BuildObj):
            for holder in build.around_holders:
                holder.content = None
            return build
        
        @classmethod
        def _create_build_obj(cls, page, build_node)->Airline._BuildObj:
            build_func = Airline._get_sync_func(build_node)

            if not build_func: return None

            func_key = f"{build_func.__code__.co_filename}::{build_func.__name__}"
            
            page.fly._slots_map[func_key] = {} # pre-execution clearance
            page.fly._slots_token = func_key

            build_return = Airline._PostFly._apply_post_fly(page, build_func, build_node)
            
            page.fly._slots_token = None

            if not build_return: return None

            slots = page.fly._slots_map.get(func_key, {})
            
            fly_around_str = "fly_around_"
            around_holders = []
            around_nodes = []
            for sl in slots:
                control = slots.get(sl)
                if control:
                    if isinstance(sl, str) and sl.startswith(fly_around_str):
                        sl = sl.replace(fly_around_str, "")
                        node = Airline._shared_map.get(sl, None)
                        if node:
                            around_holders.append(control)
                            around_nodes.append(node)
                        else:
                            print(f"[fletfly] WARNING: fly_around slot found with name '{sl}' but NO shared content is registered with this name!")
                    else:
                        print(f"[fletfly] WARNING: Only layouts (not builds) can have free (not fly_around) slots. "
                            f"Free slot with the name '{sl}' will be ignored.")

            objs_map = Airline._BuildObj._explore_return(build_return)
            
            page.fly._slots_map.pop(func_key, None) # post-execution clearance
            
            build_obj = Airline._BuildObj(objs_map, around_holders, around_nodes, build_node)
            
            return build_obj
        
        @classmethod
        def _explore_return(cls, build_return):
            if not isinstance(build_return, (list, tuple)):
                build_return = [build_return]
            view_flag = False
            view_err_msg = f"[fletfly] View control is the topmost control, can't be associated with other controls"
            objs_map = {"":[]}        
            def check_val(value):
                nonlocal view_flag
                if view_flag:
                    raise ValueError(view_err_msg)
                if callable(value) and getattr(value, "_is_fletfly_wrapper", False) == True:
                    return value()
                elif isinstance(value, ft.View):
                    view_flag = True
                    if len(objs_map[""]) > 0 or len(list(objs_map.keys())) > 1:
                        raise ValueError(view_err_msg)
                    return value
                elif isinstance(value, ft.Control):
                    return value
                elif hasattr(value, "__module__") and "flet_charts" in value.__module__:
                    return value
                else:
                    print(f"[fletfly] Return of layout or build functions must be of ft.Control type or flet_charts type or fly_around shared control")
                    print(f"Value of type {type(value)} is detected and ignored.")
                    return None
            for item in build_return:
                if isinstance(item, dict):
                    for k, v in item.items():
                        v = check_val(v)
                        if v:
                            if k == "":
                                objs_map[""].append(v)
                            elif k in objs_map:
                                print(f"[fletfly] Double key with name '{k}' it will be considered nameless")
                                objs_map[""].append(v) # nameless view sections
                            elif isinstance(v, ft.View):
                                print(f"[fletfly] ft.View can't be name '{k}' it will be considered nameless")
                                objs_map[""].append(v)
                            else:
                                objs_map[k] = v
                else:
                    item = check_val(item)
                    if item: objs_map[""].append(item)
            # objs_map {"named1":controloraroundnode, "":[unnamed1, unnamed2]}
            return objs_map

        @classmethod
        def _save_build_hero(cls, page, view):
            if not hasattr(view, "_fly_build_obj"):
                return
            
            build_node = view._fly_build_obj.build_node
            hero_val = Airline._get_sync_hero(build_node)
            if hero_val:
                if build_node.is_dynamic():
                    map = page.fly._build_heros.get(build_node.path, {})
                    map[view.route]=view._fly_build_obj
                    hero_val = hero_val if isinstance(hero_val, int) else 5
                    while map and len(map) > hero_val:
                        map.pop(next(iter(map)))
                else:
                    map = view._fly_build_obj
            else:
                map = None
            page.fly._build_heros[view.route] = map

    class _LayoutNode: # one node created for one layout for all times
        def __init__(self, func=None, override_var=None, _class=None, 
                     method_name=None, override_clsattr=None,
                     hero_var=None, hero_clsattr=None,
                     post_fly_func=None, post_fly_clsattr=None):
            self.func = func #function
            self.override_var = override_var
            self._class = _class #class
            self.method_name = method_name
            self.override_clsattr = override_clsattr
            self.hero_var = hero_var
            self.hero_clsattr = hero_clsattr
            self.post_fly_func = post_fly_func
            self.post_fly_clsattr = post_fly_clsattr

        @classmethod
        def _get_not_overrided_layout_nodes(cls, layout_node_list: list[Airline._LayoutNode]):
            slice_idx = 0
            for i in range(len(layout_node_list) - 1, -1, -1):
                n = layout_node_list[i]
                dynamic_over = False
                if n._class and n.override_clsattr:
                    dynamic_over = bool(getattr(n._class, n.override_clsattr, False))
                
                override_var = getattr(n, 'override_var', False)
                if dynamic_over or override_var:
                    has_dynamic_layout = bool(getattr(n._class, n.method_name, None)) if (n._class and getattr(n, 'method_name', None)) else False
                    has_func_layout = bool(getattr(n, "func", None))
                    
                    if has_dynamic_layout or has_func_layout:
                        slice_idx = i
                    else:
                        slice_idx = i + 1  # حجب المسارات السابقة واستبعاد العقدة الحالية الفارغة
                    break
            returning = layout_node_list[slice_idx:]
            return returning


        
    class _LayoutObj:# objects for same or different layout
        def __init__(self, objs_map:dict=None, holders:list[ft.Control]=None,
                     around_holders:list[ft.Control] = None, around_nodes: list[Airline._AroundNode] = None,
                     layout_node:Airline._LayoutNode=None, hero:bool = None):
            self.objs_map = objs_map # {"named1":control_or_around_node, "":[unnamed1, unnamed2]}
            self.holders = holders if holders else []
            self.around_holders = around_holders if around_holders else []
            self.around_nodes = around_nodes if around_nodes else []
            self.layout_node = layout_node
            if hero is None:
                if layout_node._class and layout_node.hero_clsattr:
                    self.hero = getattr(layout_node._class, layout_node.method_name)
                else:
                    self.hero = layout_node.hero_var
            if self.hero is None:
                self.hero = True

        @classmethod
        def _inject_into_layout(cls, page, son_obj:Airline._BuildObj|Airline._LayoutObj, layout_obj:Airline._LayoutObj):
            if not son_obj.objs_map and not layout_obj.holders: return None
            if son_obj.objs_map and not layout_obj.holders: return son_obj
            if layout_obj.holders and not son_obj.objs_map: return layout_obj

            nameless_list = list(son_obj.objs_map.get("",[]))
            
            for key, ctrl in son_obj.objs_map.items():
                if key == "": continue # these are nameles list
                inserted = False
                for holder in layout_obj.holders:
                    if getattr(holder, "_slot_name", None) == key:
                        if isinstance(ctrl, ft.Control):
                            holder.content = ctrl
                        elif isinstance(ctrl, Airline._AroundNode):
                            active_around_obj = Airline._AroundObj._get_active_around(page, ctrl)
                            if active_around_obj:
                                holder.content = active_around_obj.obj
                        inserted = True
                        break
                if not inserted:
                    print(f"[fletfly] view part with name '{key}' didn't find a slot match, ... Ignored.")
            
            nameless_holders = [x for x in layout_obj.holders if isinstance(getattr(x, "_slot_name", None), int) and x._slot_name > 10000000]
            extra_views = 0
            holder_index = 0
            extra_shared_views = 0
            num_holders = len(nameless_holders)
            
            for ctrl in nameless_list:
                if isinstance(ctrl, ft.Control):
                    if holder_index < num_holders:
                        nameless_holders[holder_index].content = ctrl
                        holder_index += 1
                    else:
                        extra_views += 1
                elif isinstance(ctrl, Airline._AroundNode):
                    if holder_index < num_holders:
                        active_around_obj = Airline._AroundObj._get_active_around(page, ctrl)
                        if active_around_obj:
                            nameless_holders[holder_index].content = active_around_obj.obj
                            holder_index += 1
                    else:
                        extra_shared_views += 1
            if extra_views or extra_shared_views:
                print(f"[fletfly] {extra_views + extra_shared_views} nameless view part/s have no slot including {extra_shared_views} shared views.")
                
            remaining_holders = num_holders - holder_index
            if remaining_holders > 0:
                print(f"[fletfly] {remaining_holders} nameless holders have got no views")
            return layout_obj

        @classmethod
        def _dismount_obj_s(cls, obj_s: Airline._LayoutObj | Airline._BuildObj):
            objs = obj_s if isinstance(obj_s, (set, list)) else {obj_s}
            
            for obj in objs:
                holders = obj.around_holders + getattr(obj, "holders", [])
                for holder in holders:
                    holder.content = None
        
        @classmethod
        def _get_layout_objs(cls, page, flight_node):
            
            view_layout_nodes = Airline._LayoutNode._get_not_overrided_layout_nodes(flight_node.layout_nodes)            
            layout_objs:list[Airline._LayoutObj] = []
            for current_node in view_layout_nodes:
                layout_obj = None
                for lay in page.fly._layouts | page.fly._new_layouts:
                    if lay.layout_node == current_node:
                        layout_obj = lay
                        break                     
                if layout_obj is None:
                    layout_obj = Airline._LayoutObj._create_layout_obj(page, current_node)
                if layout_obj:
                    page.fly._new_layouts.add(layout_obj)
                    layout_objs.append(layout_obj)
                
            return layout_objs

        @classmethod
        def _create_layout_obj(cls, page, layout_node)->Airline._LayoutObj:
            layout_func = Airline._get_sync_func(layout_node)
            if not layout_func: return None
            func_key = f"{layout_func.__code__.co_filename}::{layout_func.__name__}"
            page.fly._slots_map[func_key] = {} # pre-execution clearance
            page.fly._slots_token = func_key
            
            layout_return = Airline._PostFly._apply_post_fly(page, layout_func, layout_node)

            page.fly._slots_token = None
            if not layout_return: return None
            slots = page.fly._slots_map.get(func_key, {})
            
            fly_around_str = "fly_around_"
            around_holders = []
            around_nodes = []
            holders = []
            for sl in slots:
                control = slots.get(sl)
                if control:
                    if isinstance(sl, str) and sl.startswith(fly_around_str):
                        sl = sl.replace(fly_around_str, "")
                        node = Airline._shared_map.get(sl, None)
                        if node:
                            around_holders.append(control)
                            around_nodes.append(node)
                        else:
                            print(f"[fletfly] WARNING: fly_around slot found with name '{sl}' but NO shared content is registered with this name!")
                    else:
                        control._slot_name = sl
                        holders.append(control)
            objs_map = Airline._BuildObj._explore_return(layout_return)
            
            page.fly._slots_map.pop(func_key, None) # post-execution clearance
            
            layout_obj = Airline._LayoutObj(objs_map, holders, around_holders, around_nodes, layout_node)
            
            return layout_obj

        @classmethod
        def _clone_control(cls, control):
            if control is None: return None
            if not isinstance(control, ft.Control) and not (
                hasattr(control, "__module__") and "flet_charts" in control.__module__):
                return control
            
            #if not hasattr(control, "page"): # RuntimeError: View(15) Control must be added to the page first
            #    return control    
            control_class = type(control)
            cloned_controls = []
            if hasattr(control, "controls") and control.controls:
                for child in control.controls:
                    cloned_controls.append(cls._clone_control(child))
            cloned_content = None
            if hasattr(control, "content") and control.content:
                cloned_content = cls._clone_control(control.content)
            start_props = {}
            if cloned_content: 
                start_props["content"] = cloned_content
            if cloned_controls:
                start_props["controls"] = cloned_controls
            ignore_list = ["parent", "content", "controls", "page", "uid"]
            for attr in type(control).__init__.__code__.co_varnames:
                if not attr.startswith("_") and not attr in ignore_list:
                    try:
                        val = getattr(control, attr, None)
                        if val is not None and not callable(val):
                            if isinstance(val, list):
                                start_props[attr] = [cls._clone_control(i) for i in val]
                            elif isinstance(val, dict):
                                start_props[attr] = {k: cls._clone_control(v) for k, v in val.items()}
                            elif hasattr(val, "name") and hasattr(val, "value") and not hasattr(val, "page"):
                                start_props[attr] = val.value
                            else:
                                start_props[attr] = cls._clone_control(val)
                    except:
                        continue
            try:
                new_control = control_class(**start_props)
            except Exception as e :
                print(e)
                new_control = control_class()
            return new_control

    class _PostFly:
        @classmethod
        def _get_sync_post_fly(cls, node)->int|bool:
            if node is None:
                return None
            if node._class and node.post_fly_clsattr: # dynamic func
                return getattr(node._class, node.post_fly_clsattr)
            elif node.post_fly_func:
                return node.post_fly_func
            return None    
        @classmethod
        def _apply_post_fly(cls, page:ft.Page, layout_build_func, layout_build_node):

            post_fly_func = cls._get_sync_post_fly(layout_build_node)
            
            controls_s = layout_build_func(page)
            if post_fly_func is None or not callable(post_fly_func):
                return controls_s

            captured = page.fly._temp_data.copy()

            if post_fly_func and captured:

                async def post_fly_worker(registry_snapshot):    
                    result = post_fly_func()
                    
                    if inspect.isawaitable(result):
                        data = await result
                    else:
                        data = result
                    
                    for item in registry_snapshot:
                        attrs = item['map']
                        control = item["control"]
                        
                        for attr, data_path in attrs.items():                    
                            raw_value = cls._get_nested_value(data, data_path)
                            final_value = cls.validate_and_rescue(control, attr, raw_value)
                            if final_value is not None:
                                setattr(control, attr, final_value)
                        
                    page.update()
                page.run_task(post_fly_worker, captured)
                
            return controls_s

        @classmethod
        def _get_nested_value(cls, data, path_str):
            if not path_str or path_str.strip() == "": # requested data = "" | None
                return data

            keys = path_str.split(".")
            current = data
            
            accumulated_path = ""
            
            for key in keys:
                is_numeric = key.isdigit()
                
                current_path = f"{accumulated_path}.{key}" if accumulated_path else key
                
                if isinstance(current, (list, tuple)):
                    if is_numeric:
                        try:
                            current = current[int(key)]  # requested data = "0" | "users_list.0"
                        except IndexError:
                            print(f"⚠️  [FletFly Data]: {current_path} index is out of range!")
                            return None
                    else:
                        print(f"⚠️  [FletFly Data]: {current_path} expected an integer index, but got string!")
                        return None
                        
                elif isinstance(current, dict):
                    if is_numeric:                   # requested data = "0" | "users_dict.0"
                        int_key = int(key)
                        if int_key in current:          
                            current = current[int_key]  # data = {0:"name"} | {"users_dict":{0:"name"}}
                        elif key in current:
                            current = current[key]   # data = {"0":"name"} | {"users_dict":{"0":"name"}}
                        else:
                            print(f"⚠️  [FletFly Data]: Inside data, key '{current_path}' (int or str) was not found!")
                            return None
                    else:
                        if key in current:
                            current = current[key]
                        else:
                            print(f"⚠️  [FletFly Data]: Inside data, key '{current_path}' was not found!")
                            return None
                            
                else:
                    print(f"⚠️  [FletFly Warning]: Inside data, the path '{accumulated_path}' is not a valid dictionary or list to look up '{key}'!")
                    return None
                
                accumulated_path = accumulated_path + "." + key if accumulated_path else key
                    
            return current
        @classmethod
        def validate_and_rescue(cls, control, attr: str, new_value) -> any:
            """
            Validates and casts incoming data based on Flet 0.86 strict hierarchy,
            returning the clean value directly to be injected into the control attribute.
            """
            annotation = type(control).__annotations__.get(attr)
            allowed_types = annotation.__args__ if hasattr(annotation, "__args__") else (annotation,)
            
            actual_type = type(new_value)

            # 1. Initial Check: Is it perfectly valid as-is?
            if actual_type == annotation or actual_type in allowed_types:
                return new_value

            # 2. Float Casting Check
            elif float in allowed_types and type(new_value) in (int, str):
                try:
                    return float(new_value)
                except (ValueError, TypeError):
                    pass

            # 3. Integer Casting Check
            elif int in allowed_types and type(new_value) in (float, str):
                try:
                    return int(float(new_value))
                except (ValueError, TypeError):
                    pass

            # 4. String Casting Check
            elif str in allowed_types:
                try:
                    return str(new_value)
                except (ValueError, TypeError, AttributeError):
                    pass

            # 5. Final Line of Defense: UI Rescue fallback values
            if bool in allowed_types:
                return False
            print(f"⚠️ [fletfly data]: The value passed to '{attr}' doesn't match attr type and can't be casted")
            return None



    def _default_error_view(self, page):
        page.views.append(
            ft.View(
                route=page.route, 
                controls=[
                    ft.Text("404", size=50, weight="bold", color="red"),
                    ft.Text(f"Oops! This path is not on our map."),
                    ft.Button("Fly Home", on_click=lambda _: page.fly("/"))
                ],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        page.update()
# endregion
    
    


def data(page: ft.Page, control, **kwargs):
    data_msg=f"""
[fletfly data] you must apply a lazy_loader function returning the lazy data, and use data() as following:
fty.data(page,
    ft.Text(size=24, weight="bold"),   # your ft.Control
    value=("user.name", "loading..."), # with default, extracted from data {"{'user':{'name':'your_name'}}"}  
    color=("user.0")                   # without default, extracted from data {"{'user':['red']}"}
)
Hint: you can use flet auto complete first for the **kwargs, then move the ) up to separate the control
"""
    if not control or not kwargs:
        print(data_msg)
        return control
        
    attr_map = {}
    for attr, config in kwargs.items():
        val = None  
        default_val = None
        if isinstance(config, (tuple,list)):
            config_len = len(config)
            if config_len < 1:
                print(data_msg)
                continue
            elif config_len < 2:
                val = config[0]
            elif config_len == 2:
                val, default_val = config
            else:
                print(data_msg)
        elif isinstance(config, str):
            val = config
        elif isinstance(config, (int, float)):
            val = str(config)
        else:
            print(data_msg)   
        if val is not None:
            attr_map[attr] = val
            if default_val is not None:
                try:           
                    setattr(control, attr, default_val)
                except: # flet will aready send an attr error
                    print(data_msg)
    if attr_map:
        page.fly._temp_data.append({"control": control, "map":attr_map})
    return control


    """
    عندي مشكلة عويصة
    لما اليوزر بيدوس الباك بتاع الابليكيشن كذا مرة بسرعة وانا مش بلحق اتابعه الدنيا بتبوظ في الترتيب
    محتاجة ضبط من نار، واعادة تفكير هنعمل ايه
    سواءا كان فيه fly_outs or not
    """

class _FlyList(list):
    """Special list to mark prepared middlewares and avoid double processing."""
    pass

def _list_middlewares(*args):
    
    # already handled
    if len(args) == 1 and isinstance(args[0], _FlyList):
        return args[0]
    
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
    items = []
    if len(args) > 1 and callable(args[0]) and not callable(args[1]) and not (isinstance(args[1],(list,tuple)) and args[1] and not callable(args[1][0]) ):
        items = [args]
    elif len(args) == 1 and isinstance(args[0], (list, tuple)) and len(args[0])>1 and (callable(args[0][1]) or (isinstance(args[0][1],(tuple,list)) and args[0][1] and callable(args[0][1][0])   )):
        items = list(args[0])
    else:
        items = list(args) 
    #adjust
    final_items = []

    for i in range(0, len(items)):
        if items[i] is None:
            pass
        elif callable(items[i]):
            final_items.append({"func": items[i], "args": [], "kwargs": {}})
        elif isinstance(items[i], (tuple, list)):
            if len(items[i])>0:
                if callable(items[i][0]):
                    final_items.append({"func": items[i][0], "args": items[i][1:], "kwargs": {}})
                else:
                    raise TypeError(
                    f"❌ [fletfly] Middleware unit at index {i} must start with a callable function. "
                    f"Found '{type(items[i][0]).__name__}' instead."
                )
        else:
            raise TypeError(f"❌ [fletfly] Expected a function or a list of functions, but got '{type(items[i]).__name__}'")
    #return
    return _FlyList(final_items)


def fly_around(name:str = None, method_name:str = None):
    class_or_func = name
    def go_class(clas, attr_name=None, inner_name=None):
        if not attr_name: # must be a method name to register
            for attr_name in dir(clas):
                if attr_name in aliases["fly_around_clsattr"]:
                    break
        if attr_name:
            Airline._AroundNode(None, clas, attr_name, inner_name)
        else:
            print(f"""
[fletfly] No attribute in class {clas.__name__} with shared or fly_around name
Shared build can't be created, please use one of the following:
@fly_around(name='my_shared', method='func1') \nclass my_class:\ndef func1(page):...
#or 
@fly_around(name='my_shared')\nclass my_class:\ndef my_shared(page):...
#or
@fly_around\nclass my_class:\ndef fly_around(page):...
#in the last case it will be renamed to 'my_class_fly_around'
""") 
        return clas # for next decorator

    # case 1 @fly_around class
    if isinstance(class_or_func, type):
        return go_class(class_or_func)
    # case 2 @fly_around def (function or method)
    elif callable(class_or_func):
        Airline._AroundNode(class_or_func) # the engine will call the function with alive page
        return class_or_func
    else: # cases 3, 4, 5: placeholder, and @fly_around() and @fly_around('name')   
        pass # Am i a decorator or function in layout return?
    
    #cls or func by user, page by engine (live version)
    def fly_around_wrapper(cls_or_func=None):
        # case 3 @fly_around() class
        if isinstance(cls_or_func, type):
            return go_class(cls_or_func, method_name, name)
        
        # case 4 @fly_around() def (function or method)
        elif callable(cls_or_func):
            Airline._AroundNode(func= cls_or_func, name=name)
            return cls_or_func # for next decorator

        # case 5 a layout or build return
        # will be used as: if the return is callable then engine calls it & return the node
        elif not cls_or_func: 
            if not name:
                print(f"[fletfly] Can't get a fly_around shared content without a name")
            return Airline._AroundNode._get_node(name)
    fly_around_wrapper._is_fletfly_wrapper = True
    return fly_around_wrapper    


def slot(page:ft.Page=None, name:str|int=None, control:ft.Control=None, fly_around:bool = None):
    if not page or not isinstance(page, ft.Page):
        raise ValueError(_page_err_msg)
    if not hasattr(page, "fly"):
        raise TypeError(f"[fletfly] Only 1 page is per user, please provide the same page")
    if not control:
        control = ft.Container(expand=True)
    if fly_around and not name:
        print(f"""
[fletfly] WARNING: Slot marked as fly_around=True but NO name was provided!
Converting to a standard auto numeric named slot to prevent engine locking.
              """)
        fly_around = False 



    allowed_token = getattr(page.fly, "_slots_token", None)
    
    fr = sys._getframe(1)
    func_key = f"{fr.f_code.co_filename}::{fr.f_code.co_name}"

    if not allowed_token or func_key != allowed_token:
        raise RuntimeError(
            f"[fletfly] Unauthorized Slot Call! The function '{func_key}' is trying to call slot() "
            f"outside the allowed active Layout/Build execution cycle."
        )

    if func_key not in page.fly._slots_map:
        page.fly._slots_map[func_key] = {}
    my_map = page.fly._slots_map[func_key]

    fly_around_str = "fly_around_"
    
    k = None
    if isinstance(name,int):
        k = fly_around_str + str(name) if fly_around else name
    elif isinstance(name, str):
        if name.startswith(fly_around_str): # "fly_around_sidebar"
            k = name 
        elif fly_around:
            k = fly_around_str + name
        elif name.isdigit():
            k = int(name)
        elif name: # not empty
            k = name
    elif name is not None:
        raise TypeError(f"[fletfly] Slot name must be, int | str, digital strings will convert to int")

    if k is None or k == "":  
        k = 10000000
        for key in reversed(list(my_map)):
            if isinstance(key, int) and key > 10000000:
                k=key
                break
        k +=1
    my_map[k] = control

    return control

holder = slot
outlet = slot
shared = fly_around


def fly_ins(*args, override=False, inheritable=True, apply_per_view=False, **kwargs):
    return _fly_ins_out("in", *args, override=override, inheritable=inheritable, apply_per_view=apply_per_view, **kwargs)

def fly_outs(*args, override=False, inheritable=False, apply_per_view=False, **kwargs):
    return _fly_ins_out("out", *args, override=override, inheritable=inheritable, apply_per_view=apply_per_view, **kwargs)
   
def _fly_ins_out(in_out, *args, override, inheritable, apply_per_view, **kwargs):
        
    if not args and not override:
        raise ValueError(f"❌ [fletfly] fly_{in_out}() cannot be empty unless fly_{in_out}_override is True.")
    
    prepared = _list_middlewares(*args)
    for dic in prepared:
        dic["inheritable"] = inheritable
        dic["apply_per_view"] = apply_per_view

    if kwargs:
        for mw in prepared:
            mw["kwargs"].update(kwargs)

    inject = {
        f"$fly_{in_out}_override": override,
        f"$fly_{in_out}": prepared
    }

    def wrapper(target):
        if isinstance(target, dict) and f"$fly_{in_out}" in target:
            existing_mws = target[f"$fly_{in_out}"]
            combined = list(existing_mws) + list(prepared)
            
            res = {**target, f"$fly_{in_out}": _FlyList(combined)}
            
            if override:
                res[f"$fly_{in_out}_override"] = True
            return res
        
        elif isinstance(target, dict):
            res = {**inject, **target}
        else:
            res = {**inject, "": target}
        return res
    return wrapper

def fly(page, path=None, *args, **kwargs):
    if not isinstance(page, ft.Page): # fly(ft.Page,)
        raise RuntimeError(f"""
✈️{"="*65}
[fletfly] Page argument is mandatory
You must pass page argument as the first argument to fly() function like this:
def main(page):
    fly(page)
ft.run(main)
# or you can easily do just this:
ft.run(fly)
            """)        
    else:
        airline = Airline._instance
        if airline is None:
            print(f"""
✈️{"="*65}
[fletfly] Airline Router is automatically initialized with default values,
and automated scan based on decorators and inheritance of Airway class.
if you want to assign routes, adjust options for the router,
You better do it in the global scope outside main function like this:
Airline(<class_or_dict_or_airwayObj_or_list>, **options...)
            """)
            airline = Airline()

        if path is None:
            path = page.route if page.route not in ("", "/", None) else ""
        if not path and Airline.initial_route:
            path = Airline.initial_route
        if not hasattr(page, "fly"):
            page.fly = Airline.FlyBox(page)
            page.on_route_change = airline._handle_route_change 
            page.on_view_pop = airline._handle_view_pop
            page.views.clear()
        print(path)
        page.fly(path)

airway = Airway
route = Airway
Route = Airway
Router = Airline
