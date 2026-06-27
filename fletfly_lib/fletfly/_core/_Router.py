from __future__ import annotations
import flet as ft
import re, sys, inspect, asyncio, os, importlib.util, time, builtins
from ._route import Shared, Route, _is_flet_instance, _call_with_payload, _page_err_msg, General, UNSET
__all__=[]
class StackMode:
    all_views = "all_views" # all views are active and built
    root_target = "root_target" # main home only & target
    last_home_target = "last_home_target" # last sub home only & target
    root_last_home_target = "root_last_home_target" # home , last port & target
    root_homes_target = "root_homes_target" # main and all sub homes & target
    all_from_last_home = "all_from_last_home"
    root_all_from_last_home = "root_all_from_last_home" # default, which view all views from last port or home to the target
    target_only = "target_only"
# max_views when <= 0 then every view is allowed.
# max_views is a periority, and it saves target then main home then nearest parent to target then nearest view to target
_check_time_var = time.perf_counter()

def _check_time(msg):

    if General.print_debugs:
        global _check_time_var
        now = time.perf_counter()
        print(f"[fletfly Debug] Time taken during [ {msg} ]: {(now - _check_time_var) * 1000:.2f}ms")
        _check_time_var = now

class Router: # singleton only 1 instance
    static_map = {} 
    dynamic_map = {}
    shared_map = {}
    _signatures_map = {}
    def __new__(cls, *args, **kwargs):
        if General._router_instance is None:
            General._router_instance = super(Router, cls).__new__(cls)
        else:
            print(f"""
✈️{"="*65}
🚨 [FLETFLY HOLDING GROUP - ARCHITECTURAL NOTICE]
    Fletfly allows only ONE Router instance to manage your fleet!
✈️{"-" * 65}
1. This single Router can manage and merge all your Zones efficiently.
2. The main() function is a 'Travel Agent' that issues tickets to passengers.
3. You MUST NOT create a new Router for every travel agent; it's a resource leak!
✈️{"-" * 65}
💡 THE ENGINEERING SOLUTION:
   A. Define your Router instance OUTSIDE the main() scope (Global Scope).
   B. Only call (fly(page, 'path')) INSIDE main() for each new traveler.
✈️{"="*65}
""")
        return General._router_instance
    
    def __init__(self,
                 routes:Route|type|dict|list[type|Route|dict]|None = None,
                 shared:Shared|type|dict|list[Route|type|dict]|None = None,
                 initial_route = "",
                 error_path:str = "",
                 max_views:int = 5,
                 stack_mode:StackMode = StackMode.all_views,
                 every_level_fallback=True,
                 auto_path_naming=True,
                 detect_created_routes=True,
                 detect_shared=True,
                 detect_route_subclasses=True,
                 detect_inner_classes=True,
                 detect_method_ordinaries=True,
                 detect_method_routes=True,
                 detect_zone_modules=True,
                 print_path_zone='/', 
                 print_static_pages=True,
                 print_dynamic_pages=True,
                 print_shared_views=True,
                 print_debugs=True,):
        if hasattr(self, "_initialized"):
            return
        General.auto_path_naming = auto_path_naming
        General.detect_created_routes = detect_created_routes
        General.detect_route_subclasses = detect_route_subclasses
        General.detect_inner_classes = detect_inner_classes
        General.detect_method_routes = detect_method_routes
        General.detect_method_ordinaries = detect_method_ordinaries
        General.initial_route = initial_route
        General.print_debugs = print_debugs
        General.detect_shared = detect_shared
        General.detect_zone_modules = detect_zone_modules

        self.error_path = error_path
        self.every_level_fallback = every_level_fallback
        self.stack_mode = stack_mode
        self.max_views = max_views

        _check_time("importing all modules till start of router")
        Route._create_tree(routes, shared)
        _check_time("creating initial tree")

        final_route = General._main_zone_tree.get("", None)
        if not final_route:
            raise ValueError(f"[fletfly] There are no routes to handle...")

        self._parse_routes(final_route)
        self._parse_shared(General._zones)

        _check_time("parsing static, dynamic & shared nodes maps")
        
        if print_path_zone is not None:
            print("-------------------- fletfly -- tree branch ---------------------")
            print(Route._format_route_tree(print_path_zone, Router.static_map, Router.dynamic_map))

        if print_static_pages:
            print("--------------------- fletfly -- static map ---------------------")
            for k in Router.static_map.values(): print(k)
        
        if print_dynamic_pages:
            print("-------------------- fletfly -- dynamic map ---------------------")
            for k in Router.dynamic_map.values(): print(k)
        
        if print_shared_views:
            print("-------------------- fletfly -- shared map ----------------------")
            
            for zone in General._zones:
                for shared in zone.shared_map.values():
                    print(shared)
        if print_static_pages or print_dynamic_pages or print_dynamic_pages:
            print("-----------------------------------------------------------------")
        
        self._initialized = True
    
    class _FlightNode:
        __slots__ = [
            'seg', # ':id'
            'path', # '/segment1/zonesegment1/segment2/:id'
            'zone_root', # '/segment1/zonesegment1/'
            'lineage', # [flight_node, flight_node]
            'view_node',
            'fly_ins', # [{"func":func1, "args":args, "zone_root":'/'}]
            'fly_outs', # [{"func":func2, "args":args, "zone_root":'/'}]
            'fly_to', # redirect, redirectTo
            'layout_nodes', # list of layoutNodes
            'title', # title
            'icon', # icon
            'view_hero', 
            'layout_hero',
            'is_zone', # False as default
            '_class',
            'props',
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
            return ":" in self.path or "[" in self.path or "{" in self.path

        def __repr__(self):
            view = self.view_node.func["func"] if self.view_node else "N/A"
            if callable(view):
                view = '<'+view.__name__+'>'
            elif isinstance(view, str) and not view.endswith("()"):
                view = f'"{view}"'
            elif view is None:
                view = ""
            layout_nodes = f"[{len(self.layout_nodes)}]"
            
            
            return f"layouts={layout_nodes}  view={view} fly_to={self.fly_to}  path='{self.path}'"
         
    class FlyBox:
        def __init__(self, page):
            self.params = {}
            self.query = {}
            self.fly_ins_radar = "/"
            self.fly_ins_is_target = False
            self.zone_root = "/"
            self.last_success_path = "/"
            self.is_navigating = False
            self.closing_view = None
            self._slots_map = {}
            self._layout_actives = {}
            self._layout_news = {}
            self._layout_heros = {}
            self._shared_actives = {}
            self._shared_news = {}
            self._shared_heros = {}
            self._view_heros = {}
            self.page = page
            self._instance_actives = {}
            self._temp_data = [] 

        def __call__(self, path: str = "/", root=False):
            if root:
                target = path.strip('/')
            else:
                target = f"{self.zone_root}{path.strip('/')}".replace("//", "/")
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

        if General._router_instance is None:
            return Router(routes=scanned_zone)
        else:
            if scanned_zone:
                Route._validate_route_final(scanned_zone)
                
                static_map, dynamic_map = General._router_instance._parse_routes(scanned_zone,scanned_zone, 
                    current_full_path=base_path)
                General._router_instance._safe_merge(General._router_instance.static_map,
                                          General._router_instance.dynamic_map, static_map, dynamic_map, skip_conflicts)

            return General._router_instance
    
    def _scan_file(cls, file_path, file_or_folder_name, main_obj = None): # main_obj value for folders
        _orphans = []
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for name, obj in inspect.getmembers(module):
            if isinstance(obj, Route):
                if obj.parent is None:
                    if obj._path in (None, "", "/"):
                        if main_obj is None:
                            main_object = obj
                            main_object.path = file_or_folder_name
                        else:
                            if (obj._view is None or main_obj._view is None) and (obj._layout is None or main_obj.layout is None):
                                main_object._vampire(obj)
                            elif ((obj._view and main_object._view) or (obj._layout and main_object._layout)) and (
                                obj._path in ("", "/") or (obj._path is None and not cls.detect_methods_routes)):
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
            if main_object is None : main_object = Route(path = file_or_folder_name)
            main_object.children.extend(_orphans)
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
            main_obj = Route(path=folder_name) # full path is handled by parsing

        for remaining_file in files.values():
            file_name = os.path.splitext(os.path.basename(remaining_file))[0]
            sub_object = cls._scan_file(remaining_file, file_name, main_obj = None)
            if sub_object:
                main_obj.children.append(sub_object)

        for entry in os.scandir(folder_path):
            if entry.is_dir() and not entry.name.startswith(('_', '.')):
                sub_child = cls._scan_folder(entry.path)
                if sub_child:
                    main_obj.children.append(sub_child)
        return main_obj

    _first_run = True
    def _handle_route_change(self, e):
        global _check_time_var
        if Router._first_run:
            _check_time("triggering initial _handle_route_change by flet")
            Router._first_run = False 
        else:
            _check_time_var = time.perf_counter()
        if not e.page.views or (e.page and e.page.route and hasattr(e.page.views[-1],"route") and e.page.route != e.page.views[-1].route):
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
                Router._ViewObj._save_view_hero(e.page, e.view)
                e.page.views.remove(e.view)
                if e.page.views:
                    top_view = e.page.views[-1]
                    e.page.fly.zone_root = top_view.zone_root
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

    # start point
    # create node
    # chick if children for each go to start point
    def _parse_routes(self, route:Route, parent_lineage=None, 
                       current_full_path="/", current_zone_root="/",
                        p_fly_ins_nodes=[], p_fly_outs_nodes=[], p_layout_nodes=[]):
        true_node = route._view not in (None, UNSET) or route._layout not in (None, UNSET) or route._fly_to not in (None, UNSET)

        if true_node or route._index not in (None, UNSET) or  route._children:
            seg = route._path.strip("/") if route._path not in (None, UNSET) else ""
            raw_path = f"{current_full_path.rstrip('/')}{f"/{seg.strip('/')}" if seg else ""}"
            current_lineage = parent_lineage.copy() if parent_lineage else []
            if route._zone:
                zone_root = raw_path.rstrip("/") + "/"
                route._zone.zone_root = zone_root
            else:
                zone_root = current_zone_root
            # no view then absolutely no page to see
            view_node = None
            if route._view not in (None, UNSET):
                view_node = Router._ViewNode(path=raw_path,
                                                _class=route._class,
                                                props=route._props,
                                                func=route._view,
                                                hero=route._view_hero,
                                                loader_func=route._loader,
                                                zone_root=zone_root)
            layout_node = None
            if route._layout not in (None, UNSET) or route._layout_override not in (None, UNSET):
                layout_node = Router._LayoutNode(path=raw_path,
                                                _class=route._class,
                                                props=route._props,
                                                func=route._layout,
                                                hero=route._layout_hero,
                                                override=route._layout_override,
                                                loader_func=route._loader,
                                                zone_root=zone_root)
                
            layout_nodes = list(p_layout_nodes) + ([layout_node] if layout_node else [])

            fly_ins_node = None
            if route._fly_ins or route._fly_in_override not in (None, UNSET):
                fly_ins_node = Router._FlyInsOutsNode(path=raw_path,
                                                _class=route._class,
                                                props=route._props,
                                                funcs=route._fly_ins if route._fly_ins else [],
                                                override = route._fly_in_override,
                                                zone_root=zone_root)
                
            fly_ins_nodes = list(p_fly_ins_nodes) + ([fly_ins_node] if fly_ins_node else [])

            fly_outs_node = None
            if route._fly_outs or route._fly_out_override not in (None, UNSET):
                fly_outs_node = Router._FlyInsOutsNode(path=raw_path,
                                                _class=route._class,
                                                props=route._props,
                                                funcs=route._fly_outs if route._fly_outs else [],
                                                override = route._fly_out_override,
                                                zone_root=zone_root)
                
            fly_outs_nodes = list(p_fly_outs_nodes) + ([fly_outs_node] if fly_outs_node else [])
                        
            if true_node and route._path not in (None, UNSET):
                node = Router._FlightNode(
                    seg=route._path,
                    path=raw_path,
                    zone_root=zone_root,
                    title=route._title,
                    icon= route._icon,
                    view_node = view_node,
                    fly_to = route._fly_to,
                    is_zone= bool(route._zone),
                    layout_nodes=layout_nodes, 
                    lineage=current_lineage,
                    fly_ins=fly_ins_nodes,
                    fly_outs=fly_outs_nodes,
                    _class=route._class,
                    props = route._props
                )
                if node.is_dynamic:
                    node.regex = self._generate_regex(raw_path)
                    Router.dynamic_map[node.regex] = node
                else:
                    Router.static_map[raw_path] = node
                current_lineage = (current_lineage.copy() if current_lineage else []) + [node]

            if route._index not in (None, UNSET) or route._children:
                fly_ins_nodes = list(p_fly_ins_nodes) + ([
                                                Router._FlyInsOutsNode(path=raw_path,
                                                _class=route._class,
                                                props=route._props,
                                                funcs=[x for x in fly_ins_node.funcs if x["inheritable"] == True],
                                                override= route._fly_in_override,
                                                zone_root=zone_root)
                                                            ] if fly_ins_node else [])

                fly_outs_nodes = list(p_fly_outs_nodes) + ([
                                                Router._FlyInsOutsNode(path=raw_path,
                                                _class=route._class,
                                                props=route._props,
                                                funcs=[x for x in fly_outs_node.funcs if x["inheritable"] == True],
                                                override= route._fly_out_override,
                                                zone_root=zone_root)
                                                            ] if fly_outs_node else [])
                for child in ([route._index] if route._index else []) + route._children:
                    self._parse_routes(route=child,
                                        parent_lineage=current_lineage,
                                        current_full_path=raw_path,
                                        current_zone_root=zone_root,
                                        p_fly_ins_nodes=fly_ins_nodes,
                                        p_fly_outs_nodes=fly_outs_nodes,
                                        p_layout_nodes=layout_nodes)
                    #self._safe_merge(Router.static_map, Router.dynamic_map, child_static, child_dynamic)

    def _parse_shared(self, zones):
        for zone in zones:
            shared_map = zone.shared_map
            for shared in shared_map.values():
                if shared._view not in (None, UNSET) and shared._name not in (None, UNSET):
                    path = zone.zone_root + shared._name

                    node = Router._SharedNode(
                        path=path,
                        _class=shared._class,
                        props=shared._props,
                        func=shared._view,
                        hero=shared._hero,
                        loader_func=shared._loader,
                        zone_root=zone.zone_root)
                    
                    if Router.shared_map.get(path, None) is None:
                        Router.shared_map[path] = node
                    else:
                        raise ValueError(f"[fletfly] shared content of zone '{zone.zone_root}' and name {shared._name} is already registered")

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
    async def _navigate(self, page, path = None, fallback=False):
        node = None
        if not fallback:
            if path is None: path = page.route
            
            path, query = self._get_path_query(page, path)
            
            node, params = self.match_path(path)

            if self._check_fly_to(page, path, node): return None

        if not node:
            node, params = self._handle_fallback(page, path) 
        if not node:
            return None
        if self._check_fly_to(page, path, node): return None
        
        #await self._apply_animation(page, node)

        page.fly.params = params if params else {}
        page.fly.query = query if query else {}

        step1_nodes = self._apply_stack_mode(node) 
        
        step2_nodes = self._apply_max_views(step1_nodes)
        
        step3_nodes = await self._check_fly_ins(page, step2_nodes, node)

        if not step3_nodes: return
        
        _check_time("navigation preparation for reconciling")
        
        step4_result = await self._reconcile_views(page, step3_nodes)
        
        if not step4_result: return None

        _check_time("reconciling views")
        page.update()
        _check_time("page update")

        if General.print_debugs:
            v_segs = [r.strip('/').split('/')[-1] if (r := getattr(v, "route", None)) is not None else None for v in page.views]            
            print(f"[fletfly Debug] Active views:", len(page.views), v_segs if v_segs else '')

            l_segs = [k.strip('/').split('/')[-1] for k in page.fly._layout_actives]            
            print(f"[fletfly Debug] Active layouts:", len(page.fly._layout_actives), l_segs if l_segs else '')

            s_segs = [k.strip('/').split('/')[-1] for k in page.fly._shared_actives]
            print(f"[fletfly Debug] Active shared views:", len(page.fly._shared_actives), s_segs if s_segs else '')

            i_segs = [k.strip('/').split('/')[-1] for k in page.fly._instance_actives]
            print(f"[fletfly Debug] Active instances:", len(page.fly._instance_actives), i_segs if i_segs else '')

            vh_segs = [f"{k.strip('/').split('/')[-1]}{f'({len(v)})' if isinstance(v, dict) else ''}" for k, v in page.fly._view_heros.items()]
            view_heros_count = sum(len(v) if isinstance(v, dict) else 1 for v in page.fly._view_heros.values())
            print(f"[fletfly Debug] Hero views:", view_heros_count, vh_segs if vh_segs else '')

            lh_segs = [f"{k.strip('/').split('/')[-1]}{f'({len(v)})' if isinstance(v, dict) else ''}" for k, v in page.fly._layout_heros.items()]
            layout_heros_count = sum(len(v) if isinstance(v, dict) else 1 for v in page.fly._layout_heros.values())
            print(f"[fletfly Debug] Hero layouts:", layout_heros_count, lh_segs if lh_segs else '')
            
            sh_segs = [f"{k.strip('/').split('/')[-1]}{f'({len(v)})' if isinstance(v, dict) else ''}" for k, v in page.fly._shared_heros.items()]
            shared_heros_count = sum(len(v) if isinstance(v, dict) else 1 for v in page.fly._shared_heros.values())
            print(f"[fletfly Debug] Hero shared:", shared_heros_count, sh_segs if sh_segs else '')
    
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
        if path in Router.static_map:
            node:Router._FlightNode = Router.static_map[path]
            return node, {}

        for pattern in reversed(list(Router.dynamic_map.keys())):
            match = pattern.match(path)
            if match:
                node:Router._FlightNode = Router.dynamic_map[pattern]
                return node, match.groupdict()

        return None, {}

    def _check_fly_to(self, page, real_path, node:_FlightNode):
        if node:
            to = None
            if node.fly_to and isinstance(node.fly_to, str):
                if not node.fly_to.startswith(General._attr_prefix):
                    to = node.fly_to
                else:
                    instance = self._get_active_class_instance(page, node, real_path)
                    val = getattr(instance, node.fly_to.replace(General._attr_prefix, ""), "not there")
                    if val != "not there" and isinstance(val, str):
                        to = val
            if to is not None:
                to = node.zone_root.rstrip("/")+"/"+to.lstrip("/")
                print(f"[fletfly] Redirecting by <fly_to> to: path '{to}'")
                page.run_task(page.push_route, to)
                return True
        return False

    def _handle_fallback(self, page, path=None):
        params = {}
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
            current_zone_error = (page.fly.zone_root.rstrip("/") + "/" + self.error_path.strip("/"))
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
        
    def _apply_stack_mode(self, node:_FlightNode):
        if self.stack_mode == StackMode.target_only or node.path in ("", "/") or not node.lineage:
            return [node]
        
        home_node = node.lineage[0]

        if self.stack_mode == StackMode.root_target:
            ok_chain = [home_node]

        elif self.stack_mode == StackMode.last_home_target:
            last_port = next((n for n in reversed(node.lineage) if n.is_zone), None)
            ok_chain = [last_port] if last_port else [home_node]

        elif self.stack_mode == StackMode.root_last_home_target:
            last_port = next((n for n in reversed(node.lineage) if n.is_zone), None)
            if last_port:
                ok_chain = [home_node, last_port]
            else:
                ok_chain = [home_node]

        elif self.stack_mode == StackMode.root_homes_target:
            ok_chain = [n for n in node.lineage if n.is_zone]

        elif self.stack_mode == StackMode.all_from_last_home:
            last_port_idx = next((i for i, n in enumerate(reversed(node.lineage)) if n.is_zone), None)
            if last_port_idx is not None:
                actual_idx = len(node.lineage) - 1 - last_port_idx
                ok_chain = node.lineage[actual_idx:]
            else:
                ok_chain = node.lineage

        elif self.stack_mode == StackMode.root_all_from_last_home:
            last_port_idx = next((i for i, n in enumerate(reversed(node.lineage)) if n.is_zone), None)
            if last_port_idx is not None:
                actual_idx = len(node.lineage) - 1 - last_port_idx
                ok_chain = [home_node] + node.lineage[actual_idx:]
            else:
                ok_chain = [home_node] + node.lineage
        else:
            ok_chain = node.lineage
    
        final_chain = [node]
        insert_idx = 0
        for item in ok_chain:
            if item not in final_chain:
                final_chain.insert(insert_idx, item)
                insert_idx+=1
        return final_chain

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

        check = self._run_node_fly_ins_out(page, ins_outs="outs", view=view, node=node, is_viewing=True, excuted_fly_ins_out=set())

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

    async def _check_fly_ins(self, page, flight_nodes, target_node):
        filtered_chain = []
        excuted_fly_ins_out = set()
        for current_node in flight_nodes:
            is_final = (current_node == target_node)
            check, func_name = await self._run_node_fly_ins_out(page, "ins", None, current_node, is_final, excuted_fly_ins_out)

            if check is True:
                filtered_chain.append(current_node)
            
            elif isinstance(check, str) and is_final:
                print(f'🔀 [fletfly] Redirecting by fly_in <{func_name}> from "{page.route}" to "{check}"')
                page.run_task(page.push_route, check)
                return None
            elif is_final:
                if page.route != page.fly.last_success_path:
                    print(f"🚫 [fletfly] Access Denied by fly_in <{func_name}>. Rolling back to: {page.fly.last_success_path}")
                    page.on_route_change = None 
                    await page.push_route(page.fly.last_success_path)
                    page.on_route_change = self._handle_route_change
                return None
        return filtered_chain
    
    async def _run_node_fly_ins_out(self, page, ins_outs, view, node:_FlightNode, is_viewing, excuted_fly_ins_out:set)->tuple:# value, func_name

        fly_in_out_nodes = self._FlyInsOutsNode._get_not_overrided_fly_ins_nodes(page, getattr(node, f"fly_{ins_outs}", []))
        last_res = True
        page.fly.is_viewing = is_viewing
        page.fly.fly_ins_radar = node.path
        if view: page.fly.closing_view = view
        last_func_name = ""
        try:
            for fly_in_out_node in fly_in_out_nodes:
                for mw in fly_in_out_node.funcs:
                    if mw.get("apply_per_view", False) or id(mw) not in excuted_fly_ins_out:
                        sync_mw = self._get_sync_func_props_path_loader_loader_props(page, fly_in_out_node, mw)
                        if not sync_mw or not callable(sync_mw["func"]): continue
                        last_func_name = sync_mw["func"].__name__
                        last_res = _call_with_payload(sync_mw["func"], page, sync_mw["props"])
                        if inspect.isawaitable(last_res):
                            last_res = await last_res

                        if not isinstance(last_res, (bool, str)):
                            print(f"ℹ️ [fletfly] Fly_{ins_outs} at '{node.path}' returned {type(last_res).__name__} ('{last_res}').")
                            print(f"    We treated it as {'False for security' if ins_outs == 'ins' else 'True'}. (Expected: True, False, or Redirect String)")

                            last_res = False if ins_outs == "ins" else True

                        if isinstance(last_res, str):
                            last_res = mw.get("zone_root", node.zone_root if node.zone_root else "").rstrip("/") + "/" + last_res.lstrip("/")
                            print(f"🔀 [fletfly] Redirect by '{sync_mw["func"].__name__}' at '{node.path}':")

                        if last_res is not True:
                            return last_res, last_func_name
                        excuted_fly_ins_out.add(id(mw))
                    else:
                        continue
        except Exception as e:
            print(f"❌ [fletfly] Critical error in fly_in middleware func: <{last_func_name}> in path: '{node.path}': {e}")
            last_res = False if ins_outs == "ins" else True   

        return last_res, last_func_name

    def _apply_max_views(self, wishlist):
        if self.max_views <= 0 or len(wishlist) <= self.max_views:
            return wishlist

        target = wishlist[-1]
        home = wishlist[0]
        
        remaining_slots = self.max_views - 2 
        middle_candidates = wishlist[1:-1]
        survivors = middle_candidates[-remaining_slots:] if remaining_slots > 0 else []

        final_list = [home] + survivors + [target]
        
        if self.max_views == 1:
            return [target]
        return final_list
    
    async def _reconcile_views(self, page, final_nodes_list):

        page.fly._temp_data = []
        page.fly._layout_news = {}
        page.fly._shared_news = {}
        Router._LayoutObj._dismount_obj_s(list(page.fly._layout_actives.values())) # dismount existing layouts

        ##### where is the dismount of views and shared????

        final_paths = [Router._get_real_path(page.route, n.path) if n.is_dynamic else n.path for n in final_nodes_list]

        for i in range(len(page.views) - 1, -1, -1):
            vi = page.views[i]
            if vi.route not in final_paths and await self._apply_fly_outs_checks(page, vi):
                view_obj = getattr(vi, "_fletfly_view_obj", None)
                if view_obj: Router._save_hero(page, view_obj, "view")
                page.views.pop(i)

        for index, flight_node in enumerate(final_nodes_list):
            if not flight_node.view_node and not flight_node.layout_nodes: continue

            layout_objs = Router._LayoutObj._get_layout_objs(page, flight_node)

            existing_view = next((v for v in page.views if v.route == final_paths[index]), None)
            view_obj = None
            semi_final_view = None
            if existing_view:
                view_obj = getattr(existing_view, "_fletfly_view_obj", None)
                if view_obj: Router._save_hero(page, view_obj, "view")
                page.views.remove(existing_view)
            
            if not view_obj:
                view_obj = Router._ViewObj._get_view_obj(page, flight_node, final_paths[index])

            all_view_layouts_objs = ([view_obj] if view_obj else []) + (list(reversed(layout_objs)) if layout_objs else [])
            
            Router._SharedObj._inject_shared_objs(page, all_view_layouts_objs)
            final_obj = None
            for i, obj in enumerate(all_view_layouts_objs):
                final_obj = obj
                if final_obj and final_obj.objs_map.get("") and isinstance(final_obj.objs_map[""][0], ft.View):
                        semi_final_view = final_obj.objs_map[""][0]
                        if i < len(all_view_layouts_objs) - 1:
                            print("[fletfly] ft.View is a top most control, you can't inject in a layout, further layout/s will be ignored")
                        break 
                if i < len(all_view_layouts_objs) - 1:
                    Router._LayoutObj._inject_into_layout(page, final_obj, all_view_layouts_objs[i+1])
            if not semi_final_view and final_obj: # named content can't be in final view.
                nameless_content = final_obj.objs_map.get("", [])
                all_keys = [k for k in final_obj.objs_map.keys() if k != ""]
                
                if nameless_content:
                    if all_keys:
                        print(f"[fletfly] WARNING: Unused named slots detected {all_keys} in final Layout or View. These will be ignored.")                 
                    semi_final_view = ft.View(controls=nameless_content)
                elif all_keys:
                    if index< len(final_nodes_list) -1:
                        print(f"[fletfly] WARNING: No view nor unnamed controls in Final Layout, only named {all_keys}")
                        final_obj = None
                    else:
                        raise ValueError(f"[fletfly] Critical Error: The final layout has no nameless content to build the view, but contains orphaned named slots: {all_keys}.")
                else:
                    final_obj = None
            if not final_obj:
                print(f"[fletfly] failed to view view of path '{'/' + flight_node.path.strip('/')}'")                
                if index < len(final_nodes_list) - 1:
                    continue
                else:
                    print(f"[fletfly] Failed to create a view for route {flight_node.path}")
                    self._navigate(page=page, path=flight_node.path, fallback=True)      
                    return None
            #if not top-view
            if index < len(final_nodes_list)-1:
                #create a shallow clone copy of the view_final (layouts and views)
                final_view = Router._LayoutObj._clone_control(semi_final_view)
                Router._LayoutObj._dismount_obj_s(all_view_layouts_objs)

            else: # top view
                final_view = semi_final_view
            page.views.append(final_view)
            
            page.fly.zone_root = flight_node.zone_root
            final_view.zone_root = flight_node.zone_root
            final_view.route = Router._get_real_path(page.route, flight_node.path) if flight_node.is_dynamic else flight_node.path
            final_view.params = dict(page.fly.params) # to restore on back
            final_view.query = dict(page.fly.query) # to restore on back
            final_view.node = flight_node
            final_view._fletfly_view_obj = view_obj
        Router._LayoutObj._clean_layouts(page)

        for k, v in page.fly._shared_actives.items():
            if k not in page.fly._shared_news and v.hero:
                page.fly._shared_heros[k] = v
        page.fly._shared_actives = page.fly._shared_news
        page.fly._shared_news = {}
        self._clean_instances(page)
        page.fly.last_success_path = page.route
        return True

    def _clean_instances(self, page):
        used_instances_pathes = set()
        used_instances_pathes.update(page.fly._layout_actives.keys())
        used_instances_pathes.update(page.fly._shared_actives.keys())
        for view in page.views:
            if hasattr(view, "route"):
                used_instances_pathes.add(view.route)
        for v in page.fly._view_heros.values():
            if isinstance(v, dict):
                used_instances_pathes.update(v.keys())
            else:
                used_instances_pathes.add(v.path)
                
        for v in page.fly._layout_heros.values():
            if isinstance(v, dict):
                used_instances_pathes.update(v.keys())
            else:
                used_instances_pathes.add(v.path)
        for item in list(page.fly._instance_actives.keys()):
            if item not in used_instances_pathes:
                page.fly._instance_actives.pop(item, None)

    @staticmethod
    def _get_real_path(main_path, node_path):
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
    
    @staticmethod
    def _get_active_class_instance(page, level_node, partial_real_path = None):
        if partial_real_path is None:
            partial_real_path = Router._get_real_path(page.route, level_node.path)

        instance = page.fly._instance_actives.get(partial_real_path, None)
        if not isinstance(instance, level_node._class):  
            instance = _call_with_payload(level_node._class, page, level_node.props)
            page.fly._instance_actives[partial_real_path] = instance
        return instance
    
    @staticmethod
    def _get_sync_func_props_path_loader_loader_props(page, level_node, func_dict = None):
        if not level_node: return None
        if not func_dict: func_dict = getattr(level_node, "func", {})
        instance = None
        final_func = None
        func = func_dict.get("func", None)
        if not func:
            return None
        if isinstance(level_node, Router._SharedNode):
            partial_real_path = level_node.path
        else:
            partial_real_path = Router._get_real_path(page.route, level_node.path)
        if callable(func):
            final_func = func
        elif isinstance(func, str) and level_node._class:
            instance = Router._get_active_class_instance(page, level_node, partial_real_path)
            final_func = getattr(instance, func, None)
            if not final_func or not callable(final_func): return None
        final_func_dict = {"func":final_func, "props": func_dict.get("props", {}), "path":partial_real_path}
        
        loader_dict = getattr(level_node, "loader_func", {})
        if loader_dict:
            loader_func = loader_dict.get("func", None)
            
            if loader_func:
                final_loader_func = None
                if callable(loader_func):
                    final_loader_func = loader_func
                elif isinstance(loader_func, str) and instance:
                    final_loader_func = getattr(instance, loader_func, None)
                if final_loader_func and callable(final_loader_func):
                    final_func_dict["loader"] = final_loader_func if final_loader_func else None
                    final_func_dict["loader_props"] = loader_dict.get("props", None)

        if not final_func: return None
        return final_func_dict
    
    @classmethod
    def _save_hero(cls, page, obj, view_or_layout):
        node = obj.node
        final_hero = None
        hero = node.hero
        if hero:
            if isinstance(hero, (bool, int)):
                final_hero = hero
            elif isinstance(hero, str):
                instance = Router._get_active_class_instance(page, node, obj.path)
                hero = getattr(instance, hero, None)
                if hero is not None:
                    final_hero = hero
        if final_hero:
            if ":" in node.path or "[" in node.path or "{" in node.path:
                map = getattr(page.fly, f"_{view_or_layout}_heros", {}).get(node.path, {})
                map[obj.path]=obj
                final_hero = final_hero if type(final_hero) is int else 5
                while map and len(map) > final_hero:
                    map.pop(next(iter(map)))
            else:
                map = obj
            getattr(page.fly, f"_{view_or_layout}_heros", {})[node.path] = map
        else:
            getattr(page.fly, f"_{view_or_layout}_heros", {}).pop(node.path, None)
        
    @staticmethod
    def _create_slots_token(func):
        # 4-way inspection logic to extract the exact code object
        if isinstance(func, type):  # Full class component
            target_code = getattr(func.__init__, "__code__", None)
            if not target_code: raise TypeError(f"[fletfly] class <{func}> was set as a callable view or layout, but it has no __init__ function")
        elif hasattr(func, '__call__') and not hasattr(func, '__code__'):  # Callable instance
            target_code = getattr(func.__call__, "__code__", None)
            if not target_code: raise TypeError(f"[fletfly] instance <{func}> was set as a callable view or layout, but it has no __call__ function")
        else:
            func = getattr(func, "__func__", func)
            target_code = func.__code__  # Bound method (instance.method)


        # Generate the unified key matching the slot frame output
        return f"{target_code.co_filename}::{target_code.co_qualname}"

    class _SharedNode: # one node created for one view for all times
        def __init__(self,path,
                    _class,
                    props,
                    func,
                    hero,
                    loader_func,
                    zone_root):
            self.path = path
            self.func = func #function
            self._class = _class
            self.props = props #class
            self.hero = hero #function
            self.loader_func = loader_func
            self.zone_root = zone_root

        @classmethod
        def _get_node(cls, name):
            if not isinstance(name, str):
                print(f"[fletfly] shared expects string name as first argument, but got '{type(name)}'")
            elif name in Router.shared_map:
                return Router.shared_map[name]
            else:
                print(f"[fletfly] can't find shared shared component with name '{name}'")

    class _SharedObj:
        def __init__(self,
                    path:str,
                    obj,
                    shared_holders,
                    shared_nodes,
                    node:Router._ViewNode,
                    hero:bool):
            self.path = path
            self.obj = obj
            self.node = node
            self.shared_holders = shared_holders
            self.shared_nodes = shared_nodes
            self.hero = hero
            if hero is None:
                if node.hero:
                    if isinstance(node.hero, bool):
                        self.hero = True
                    elif isinstance(node.hero, str):
                        instance = Router._get_active_class_instance(page, node, obj.path)
                        val = getattr(instance, node.hero, "not there")
                        if val != "not there":
                            self.hero = val
        @classmethod
        def _create_shared_obj(cls, page, shared_node:Router._SharedNode):
            shared_loader_dict = Router._get_sync_func_props_path_loader_loader_props(page, shared_node)
            if not shared_loader_dict: return None
            
            func_key = Router._create_slots_token(shared_loader_dict['func'])

            page.fly._slots_map[func_key] = {} # pre-execution clearance
            page.fly._slots_token = func_key

            shared_return = Router._Loader._apply_loader(page, shared_loader_dict)
            
            page.fly._slots_token = None

            if not shared_return: return None

            slots = page.fly._slots_map.get(func_key, {})
            
            shared_str = "shared_"
            shared_holders = []
            shared_nodes = []
            for sl, control in slots.items():
                if control:
                    if isinstance(sl, str) and sl.startswith(shared_str):
                        sl = sl.replace(shared_str, "")
                        shared_node = Router.shared_map.get(shared_node.zone_root+sl, None)
                        if shared_node:
                            shared_holders.append(control)
                            shared_nodes.append(shared_node)
                        else:
                            print(f"[fletfly] WARNING: shared slot found with name '{sl}' but NO shared content is registered with this name!")
                    else:
                        print(f"[fletfly] WARNING: Only layouts (not views) can have free (not shared) slots. "
                            f"Free slot with the name '{sl}' will be ignored.")

            page.fly._slots_map.pop(func_key, None) # post-execution clearance
            shared_obj = Router._SharedObj(path=shared_node.path,
                                        obj=shared_return,
                                        shared_holders=shared_holders,
                                        shared_nodes=shared_nodes,
                                        node=shared_node,
                                        hero=shared_node.hero
                                    )
            return shared_obj
        @classmethod
        def _get_shared_obj(cls, page, shared_node:Router._SharedNode)->Router._SharedObj:
            path = shared_node.path
            shared_obj = page.fly._shared_actives.get(path, None) or\
                        page.fly._shared_news.get(path, None) or\
                        page.fly._shared_heros.get(path, None)
            if shared_obj is None:
                shared_obj = Router._SharedObj._create_shared_obj(page, shared_node)
            
            if shared_obj:
                page.fly._shared_news[shared_node.path] = shared_obj
                shared_obj.path = shared_node.path
                return shared_obj
            return None
        @classmethod
        def _inject_shared_objs(cls, page, objs:list[Router._LayoutObj|Router._ViewObj]):
            for obj in objs:
                if obj.shared_holders and obj.shared_nodes:
                    for holder, node in zip(obj.shared_holders, obj.shared_nodes):
                        if holder and node:
                            active_shared_obj = cls._get_shared_obj(page, node)
                            if active_shared_obj:
                                holder.content = active_shared_obj.obj
    class _ViewNode: # one node created for one view for all times
        def __init__(self,path,
                    _class,
                    props,
                    func,
                    hero,
                    loader_func,
                    zone_root):
            self.path = path
            self.func = func #function
            self._class = _class
            self.props = props #class
            self.hero = hero #function
            self.loader_func = loader_func
            self.zone_root = zone_root

    class _ViewObj:# carrying views (multiple) views info about the view
        def __init__(self,
                    path:str,
                    objs_map,
                    shared_holders,
                    shared_nodes,
                    node:Router._ViewNode,
                    hero:bool):
            self.path = path
            self.objs_map = objs_map # {"named1":controlorsharednode, "":[unnamed1, unnamed2]}
            self.node = node
            self.shared_holders = shared_holders
            self.shared_nodes = shared_nodes
            self.hero = hero
            if hero is None:
                if node.hero:
                    if isinstance(node.hero, bool):
                        self.hero = True
                    elif isinstance(node.hero, str):
                        instance = Router._get_active_class_instance(page, node, obj.path)
                        val = getattr(instance, node.hero, "not there")
                        if val != "not there":
                            self.hero = val
        @classmethod
        def _dismount_view(cls, view:Router._ViewObj):
            for holder in view.shared_holders:
                holder.content = None
            return view
        @classmethod
        def _get_view_obj(cls, page, flight_node, path):
            if flight_node.is_dynamic:
                view_obj = page.fly._view_heros.get(flight_node.path, {}).get(path, None)
            else:
                view_obj = page.fly._view_heros.get(flight_node.path, None)
            if not view_obj or not isinstance(view_obj, Router._ViewObj):
                view_obj = Router._ViewObj._create_view_obj(page, flight_node.view_node )
                if view_obj: view_obj.path=path
            return view_obj
        
        @classmethod
        def _create_view_obj(cls, page, view_node:Router._ViewNode)->Router._ViewObj:
            view_loader_dict = Router._get_sync_func_props_path_loader_loader_props(page, view_node)

            if not view_loader_dict: return None
            func_key = Router._create_slots_token(view_loader_dict['func'])
            
            page.fly._slots_map[func_key] = {} # pre-execution clearance
            page.fly._slots_token = func_key

            view_return = Router._Loader._apply_loader(page, view_loader_dict)
            
            page.fly._slots_token = None

            if not view_return: return None

            slots = page.fly._slots_map.get(func_key, {})
            
            shared_str = "shared_"
            shared_holders = []
            shared_nodes = []
            for sl, control in slots.items():
                if control:
                    if isinstance(sl, str) and sl.startswith(shared_str):
                        sl = sl.replace(shared_str, "")
                        shared_node = Router.shared_map.get(view_node.zone_root+sl, None)
                        if shared_node:
                            shared_holders.append(control)
                            shared_nodes.append(shared_node)
                        else:
                            print(f"[fletfly] WARNING: shared slot found with name '{sl}' but NO shared content is registered with this name!")
                    else:
                        print(f"[fletfly] WARNING: Only layouts (not views) can have free (not shared) slots. "
                            f"Free slot with the name '{sl}' will be ignored.")

            objs_map = Router._ViewObj._explore_return(page, view_return, view_node)
            
            page.fly._slots_map.pop(func_key, None) # post-execution clearance
            view_obj = Router._ViewObj(
                                    path=page.route,
                                    objs_map=objs_map,
                                    shared_holders=shared_holders,
                                    shared_nodes=shared_nodes,
                                    node=view_node,
                                    hero=view_node.hero
                                    )
            return view_obj
        
        @classmethod
        def _explore_return(cls, page, view_return, node):
            if not isinstance(view_return, (list, tuple)):
                view_return = [view_return]
            v_flag = None
            objs_map = {"":[]}        
            def check_val(value):
                nonlocal v_flag
                if isinstance(value, ft.View):
                    v_flag = ""
                elif isinstance(value, str):
                    shared_name = value
                    shared_node = Router.shared_map.get(node.zone_root+shared_name, None)
                    if shared_node:
                        value = Router._SharedObj._get_shared_obj(page, shared_node)
                        
                        if value:
                            value = value.obj
                        if value:
                            if isinstance(value, ft.View):
                                v_flag = shared_name
                        else:
                            return None
                    else:
                        print(f"[fletfly] WARNING: The view returned shared name '{value}', but NO shared content is registered with this name!")
                        return None
                if not _is_flet_instance(value) and not isinstance(value, Router._SharedObj):
                    print(f"[fletfly] Return of layout or view functions must be of ft.Control type (or string for shared views)")
                    print(f"[fletfly] Value of type {type(value)} is detected and ignored.")
                    return None
                if v_flag is not None and (len(objs_map[""]) > 0 or len(list(objs_map.keys())) > 1):
                    name_str = f'Shared view "{v_flag}" is ft.view. ' if v_flag else ''
                    raise ValueError(f"[fletfly] {name_str}View control is the topmost control, can't be associated with other controls")
                return value
            for item in view_return:
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
            # objs_map {"named1":controlorsharednode, "":[unnamed1, unnamed2]}
            return objs_map
            
    class _FlyInsOutsNode: # one node created for one layout for all times
        def __init__(self, path=None,
                    funcs=None,
                    _class=None,
                    props=None,
                    override=None, 
                    zone_root=None):
            self.path = path
            self.funcs = funcs #function
            self._class = _class #class
            self.props = props
            self.override = override
            self.zone_root=zone_root
        @classmethod
        def _get_not_overrided_fly_ins_nodes(cls, page, fly_in_node_list: list[Router._FlyInsOutsNode]):
            slice_idx = 0
            for i in range(len(fly_in_node_list) - 1, -1, -1):
                n = fly_in_node_list[i]
                override = False
                if n.override:
                    if isinstance(n.override, bool):
                        override = True
                    elif isinstance(n.override, str):
                        
                        instance = Router._get_active_class_instance(page, n)
                        val = getattr(instance, n.override, "not there")
                        if val != "not there":
                            override = val
                if override:
                    if n.funcs: # has fly_ins, not override only
                        slice_idx = i
                    else:
                        slice_idx = i + 1  # has override only, exclude it.
                    break

            return fly_in_node_list[slice_idx:]

    class _LayoutNode: # one node created for one layout for all times
        def __init__(self, path,
                    _class,
                    props,
                    func,
                    hero,
                    override,  
                    loader_func,
                    zone_root):
            self.path = path
            self.func = func #function
            self.override = override
            self._class = _class #class
            self.props = props
            self.hero = hero
            self.loader_func = loader_func
            self.zone_root = zone_root

        @classmethod
        def _get_not_overrided_layout_nodes(cls, page, node_list: list[Router._LayoutNode]):
            slice_idx = 0
            for i in range(len(node_list) - 1, -1, -1):
                n = node_list[i]
                override = False
                if n.override:
                    if isinstance(n.override, bool):
                        override = True
                    elif isinstance(n.override, str):
                        instance = Router._get_active_class_instance(page, n)
                        val = getattr(instance, n.override, "not there")
                        if val != "not there":
                            override = val
                if override:
                    if n.func: # has layout, not override only
                        slice_idx = i
                    else:
                        slice_idx = i + 1  # has override only, exclude it.
                    break
            return node_list[slice_idx:]
        
    class _LayoutObj:# objects for same or different layout
        def __init__(self,
                    path:str,
                    objs_map:dict,
                    holders:list[ft.Control],
                    shared_holders:list[ft.Control],
                    shared_nodes: list[Router._SharedNode],
                    node:Router._LayoutNode,
                    hero:bool
                    ):
            self.path = path
            self.objs_map = objs_map # {"named1":control_or_shared_node, "":[unnamed1, unnamed2]}
            self.holders = holders if holders else []
            self.shared_holders = shared_holders if shared_holders else []
            self.shared_nodes = shared_nodes if shared_nodes else []
            self.node = node
            self.hero = None
            if hero is None and node.hero:
                if isinstance(node.hero, bool):
                    self.hero = True
                elif isinstance(node.hero, str):
                    instance = Router._get_active_class_instance(page, node, obj.path)
                    val = getattr(instance, node.hero, "not there")
                    if val != "not there":
                        self.hero = val
        
        @classmethod
        def _inject_into_layout(cls, page, son_obj:Router._ViewObj|Router._LayoutObj, layout_obj:Router._LayoutObj):
            if not son_obj.objs_map and not layout_obj.holders: return None
            if son_obj.objs_map and not layout_obj.holders: return son_obj
            if layout_obj.holders and not son_obj.objs_map: return layout_obj

            nameless_list = list(son_obj.objs_map.get("",[]))
            
            for key, ctrl in son_obj.objs_map.items():
                if key == "": continue
                inserted = False
                for holder in layout_obj.holders:
                    if getattr(holder, "_slot_name", None) == key:
                        holder.content = ctrl
                        inserted = True
                        break
                if not inserted:
                    print(f"[fletfly] view part with name '{key}' didn't find a slot match, ... Ignored.")
            
            nameless_holders = [x for x in layout_obj.holders if isinstance(getattr(x, "_slot_name", None), int) and x._slot_name > 10000000]
            extra_views = 0
            holder_index = 0
            extra_shared_views = 0
            num_nameless_holders = len(nameless_holders)
            for ctrl in nameless_list:
                if holder_index < num_nameless_holders:
                    nameless_holders[holder_index].content = ctrl
                    holder_index += 1
                else:
                    extra_views += 1
            if extra_views:
                print(f"[fletfly] {extra_views} nameless view part/s have no slot including {extra_shared_views} shared views.")
                
            remaining_nameless_holders = num_nameless_holders - holder_index
            if remaining_nameless_holders > 0:
                print(f"[fletfly] {remaining_nameless_holders} nameless holders have got no views")
            return layout_obj

        @classmethod
        def _dismount_obj_s(cls, obj_s: Router._LayoutObj | Router._ViewObj):
            objs = obj_s if isinstance(obj_s, (set, list)) else {obj_s}
            
            for obj in objs:
                holders = obj.shared_holders + getattr(obj, "holders", [])
                for holder in holders:
                    holder.content = None
        @classmethod
        def _clean_layouts(cls, page):
            # Remove successfully built active layouts from heros
            for obj in page.fly._layout_news.values():
                node = obj.node
                if ":" in node.path or "[" in node.path or "{" in node.path:
                    page.fly._layout_heros.get(node.path, {}).pop(obj.path, None)
                else:
                    page.fly._layout_heros.pop(node.path, None)

            deleted_keys = page.fly._layout_actives.keys() - page.fly._layout_news.keys()
            for key in deleted_keys:
                Router._save_hero(page, page.fly._layout_actives[key], "layout")

            page.fly._layout_actives = page.fly._layout_news
            page.fly._layout_news = {}

        @classmethod
        def _get_layout_objs(cls, page, flight_node):
            
            nodes = Router._LayoutNode._get_not_overrided_layout_nodes(page, flight_node.layout_nodes)            
            layout_objs:list[Router._LayoutObj] = []
            for lay_node in nodes:
                if not lay_node: continue
                layout_obj = None
                
                path=Router._get_real_path(page.route, lay_node.path)

                layout_obj = page.fly._layout_news.get(path, None) or\
                            page.fly._layout_actives.get(path, None)

                if not layout_obj:
                    if ":" in lay_node.path or "[" in lay_node.path or "{" in lay_node.path: # أو lay_node.is_dynamic()
                        layout_obj = page.fly._layout_heros.get(lay_node.path, {}).get(path, None)
                    else:
                        layout_obj = page.fly._layout_heros.get(lay_node.path, None)
                
                if not layout_obj or not isinstance(layout_obj, Router._LayoutObj):
                    layout_obj = Router._LayoutObj._create_layout_obj(page, lay_node)
                if layout_obj:
                    page.fly._layout_news[path] = layout_obj
                    layout_obj.path = path
                    layout_objs.append(layout_obj)
            return layout_objs

        @classmethod
        def _create_layout_obj(cls, page, layout_node:Router._LayoutNode)->Router._LayoutObj:
            
            layout_loader_dict = Router._get_sync_func_props_path_loader_loader_props(page, layout_node) 
            if not layout_loader_dict: return None
            
            func_key = Router._create_slots_token(layout_loader_dict['func'])
            
            page.fly._slots_map[func_key] = {} # pre-execution clearance
            page.fly._slots_token = func_key
            
            layout_return = Router._Loader._apply_loader(page, layout_loader_dict)

            page.fly._slots_token = None
            if not layout_return: return None
            slots = page.fly._slots_map.get(func_key, {})
            
            shared_str = "shared_"
            shared_holders = []
            shared_nodes = []
            holders = []
            for sl, control in slots.items():
                if control:
                    if isinstance(sl, str) and sl.startswith(shared_str):
                        sl = sl.replace(shared_str, "")
                        shared_node = Router.shared_map.get(layout_node.zone_root+sl, None)
                        if shared_node:
                            shared_holders.append(control)
                            shared_nodes.append(shared_node)
                        else:
                            print(f"[fletfly] WARNING: shared slot found with name '{sl}' but NO shared content is registered with this name!")
                    else:
                        control._slot_name = sl
                        holders.append(control)
            objs_map = Router._ViewObj._explore_return(page, layout_return, layout_node)
            
            page.fly._slots_map.pop(func_key, None) # post-execution clearance
            layout_obj = Router._LayoutObj(path=layout_loader_dict["path"],
                                           objs_map=objs_map,
                                           holders=holders,
                                           shared_holders=shared_holders,
                                           shared_nodes=shared_nodes,
                                           node=layout_node,
                                           hero=layout_node.hero
                                           )
            return layout_obj

        @classmethod
        def _clone_control(cls, control):
            if control is None: return None
            if not _is_flet_instance(control):
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
            ignore_list = ["parent", "content", "controls", "page", "uid",
                            "animate", "animate_size", "animate_position", 
                            "animate_opacity", "animate_scale", "animate_rotation"
                            ]
            #for attr in type(control).__init__.__code__.co_varnames:
            for attr in dir(control):
                if not attr.startswith("_") and not attr in ignore_list :
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
            signature = Router._signatures_map.get(control_class, None)
            if not signature:
                signature = inspect.signature(control_class).parameters.keys()
                Router._signatures_map[control_class] = signature
            start_props = {k: v for k, v in start_props.items() if k in signature}
            try:
                new_control = control_class(**start_props)
            except Exception as e:
                print(f"[fletfly] Error: {e}")
                new_control = control_class()
            return new_control

    class _Loader:
        @classmethod
        def _apply_loader(cls, page:ft.Page, func_loader_dict):
            
            controls_s = _call_with_payload(func_loader_dict["func"], page, func_loader_dict["props"])
            
            loader_func = func_loader_dict.get("loader", None)
            if not loader_func: return controls_s
            
            captured = page.fly._temp_data.copy()

            if captured:

                async def loader_worker(registry_snapshot):
                    
                    result = _call_with_payload(loader_func, page, func_loader_dict.get("loader_props", {}))
                    
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
                page.run_task(loader_worker, captured)
                
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
                            print(f"⚠️  [fletfly Data]: {current_path} index is out of range!")
                            return None
                    else:
                        print(f"⚠️  [fletfly Data]: {current_path} expected an integer index, but got string!")
                        return None
                        
                elif isinstance(current, dict):
                    if is_numeric:                   # requested data = "0" | "users_dict.0"
                        int_key = int(key)
                        if int_key in current:          
                            current = current[int_key]  # data = {0:"name"} | {"users_dict":{0:"name"}}
                        elif key in current:
                            current = current[key]   # data = {"0":"name"} | {"users_dict":{"0":"name"}}
                        else:
                            print(f"⚠️  [fletfly Data]: Inside data, key '{current_path}' (int or str) was not found!")
                            return None
                    else:
                        if key in current:
                            current = current[key]
                        else:
                            print(f"⚠️  [fletfly Data]: Inside data, key '{current_path}' was not found!")
                            return None
                            
                else:
                    print(f"⚠️  [fletfly Warning]: Inside data, the path '{accumulated_path}' is not a valid dictionary or list to look up '{key}'!")
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
Hint: you can use flet auto complete first for the control properties, then move the ) up to separate the control
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

def slot(page:ft.Page=None,
         name:str|int=None,
         control=None,
         shared:bool = None):
    if not isinstance(page, ft.Page):
        raise ValueError(_page_err_msg)
    if not hasattr(page, "fly"):
        raise TypeError(f"[fletfly] Only 1 page is per user, please provide the same page of that user.")
    if shared and not name:
        print(f"""
[fletfly] WARNING: Slot marked as shared=True but NO name was provided!
Converting to a standard auto numeric named slot to prevent engine locking.
              """)
        shared = False 
    if control is None:
        control = ft.Container(expand=True)

    allowed_token = getattr(page.fly, "_slots_token", None)
    
    fr = sys._getframe(1)
    func_key = f"{fr.f_code.co_filename}::{fr.f_code.co_qualname}"

    if not allowed_token or func_key != allowed_token:
        raise RuntimeError(
            f"[fletfly] Unauthorized Slot Call! The function '{func_key}' is trying to call slot() "
            f"outside the allowed active Layout/View execution cycle."
        )

    if func_key not in page.fly._slots_map:
        page.fly._slots_map[func_key] = {}
    my_map = page.fly._slots_map[func_key]

    shared_str = "shared_"
    
    k = None
    if isinstance(name,int):
        k = shared_str + str(name) if shared else name
    elif isinstance(name, str):
        if name.startswith(shared_str): # "shared_sidebar"
            k = name 
        elif shared:
            k = shared_str + name
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

def fly(page, path=None, root= False):
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

    router = General._router_instance
    if router is None:
        print(f"""
✈️{"="*65}
[fletfly] Router Router is automatically initialized with default values,
and automated scan based on decorators and inheritance of Route class.
if you want to assign routes, adjust options for the router,
You better do it in the global scope outside main function like this:
Router(<class_or_dict_or_routeObj_or_list>, **options...)
        """)
        router = Router()

    if not hasattr(page, "fly"): # new user
        page.fly = Router.FlyBox(page)
        page.on_route_change = router._handle_route_change 
        page.on_view_pop = router._handle_view_pop
        page.views.clear()
        # initial going, he doesn't need to tell me
        if path is None: # get page route
            path = page.route if page.route not in ("", "/", None) else None
        if path is None: # get initial route
            path = General.initial_route

    if path is not None:
        if root:
            target = path.strip('/')
        else:
            target = f"{page.fly.zone_root}{path.strip('/')}".replace("//", "/")
        if target == "/": target = ""
        page.run_task(page.push_route, target)
    
    return page.fly