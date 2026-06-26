from ._route import Route as Route, Shared as Shared
import flet as ft
from typing import Any
__all__=[]

class StackMode:
    all_views:str = ...
    root_target:str = ...
    last_home_target:str = ...
    root_last_home_target:str = ...
    root_homes_target:str = ...
    all_from_last_home:str = ...
    root_all_from_last_home:str = ...
    target_only:str = ...

class Router:
    def __init__(self,
                routes:Route|type|dict|list[type|Route|dict]|None = None,
                shared:Shared|type|dict|list[Route|type|dict]|None = None,
                initial_route:str = "",
                error_path:str = "",
                max_views:int = 5,
                stack_mode:str = StackMode.root_all_from_last_home,
                every_level_fallback:bool=True,
                auto_path_naming:bool=True,
                detect_created_routes:bool=True,
                detect_shared:bool=True,
                detect_route_subclasses:bool=True,
                detect_inner_classes:bool=True,
                detect_method_ordinaries:bool=True,
                detect_method_routes:bool=True,
                detect_zone_modules:bool=True,
                print_path_zone:str='/', 
                print_static_pages:bool=True,
                print_dynamic_pages:bool=True,
                print_shared_views:bool=True,
                print_debugs:bool=True
                )-> None: ...


    class FlyBox:
        params:dict
        query:dict
        page:ft.Page
        zone_root:str
        
def fly(page:ft.Page, path:str|None=None, root:bool=False)->Router.FlyBox:
    """
    Initiates Router with defaults if not initiated.

    Navigates to specific path, related to the current zone.

    If root=True, navigates to absolute path from root.
    """
    ...

def data(page:ft.Page, control:ft.Control, **kwargs: str | tuple[str, Any])->ft.Control:
    """
    Records and returns The control to be injected with data.
    
    Records The properties of the control to be injected and the data map keys to get the corresponding values.
    
    Used as: data(page, ft.Text(), value="name.0")
    
    or as: data(page, ft.Text(value="default"), value="name.0")
    
    or as: data(page, ft.Text(), value=("name.0", "default"))
    """
    ...

def slot(page:ft.Page, name:str|int|None=None, control:ft.Control=ft.Column(expand=True), shared:bool=False)->ft.Control:
    """
    Records the Control to be used as a slot(outlet) for other layouts or views.

    Could be marked by name for targeted slot injection.

    Could be preserved for special shared view if shared=True.
    """
    ...
