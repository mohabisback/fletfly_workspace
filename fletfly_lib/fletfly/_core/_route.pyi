# fletfly.pyi
__all__=[Route]
from typing import Any, Callable, TypeVar, Union, overload

T = TypeVar("T", bound=Callable[..., Any])

UNSET: Any = ...
class FuncDict: pass
class _MethodHandler:
    pass

class UseProxy:
    @overload
    def __get__(self, instance: None, owner: type) -> UseProxy: ...
    @overload
    def __get__(self, instance: object, owner: type) -> ObjUseProxy: ...
    
    @property
    def layout(self) -> CallableLayout: ...
    @property
    def view(self) -> CallableView: ...
    @property
    def loader(self) -> CallableLoader: ...
    @property
    def fly_in(self) -> CallableFlyIn: ...
    @property
    def fly_out(self) -> CallableFlyOut: ...
    @property
    def child(self) -> CallableChild: ...
    @property
    def index(self) -> CallableIndex: ...

class ObjUseProxy:   
    @property
    def layout(self) -> ObjDecorativeLayout: ...
    @property
    def view(self) -> ObjDecorativeView: ...
    @property
    def loader(self) -> ObjDecorativeLoader: ...
    @property
    def fly_in(self) -> ObjDecorativeFlyIn: ...
    @property
    def fly_out(self) -> ObjDecorativeFlyOut: ...
    @property
    def child(self) -> ObjDecorativeChild: ...
    @property
    def index(self) -> ObjDecorativeIndex: ...

class ObjDecorativeLayout: # Case: @obj.use.layout(hero=True) -> returns the decorator wrapper
    def __call__(self,
                 hero: bool | int | None = UNSET,
                 override: bool | None = UNSET,
                 props: dict[str, Any] | None = UNSET,
                 **kwargs: Any) -> Callable[[T], T]:
        """
        Decorates a callable to set it as the layout for the Route instance.

        Applies 'layout_hero' and 'layout_override' properties to the Route instance.

        Accepts additional layout configurations via the 'props' dictionary or arbitrary keyword arguments (**kwargs).
        """
        ...
class CallableLayout:  # Case: use.layout(func) -> returns payload dict 
    def __call__(self,
                 func: Callable[..., Any] = UNSET,
                 hero: bool | int | None = UNSET,
                 override: bool | None = UNSET,
                 props: dict[str, Any] | None = UNSET,
                 **kwargs: Any) -> FuncDict:
        """
        Creates a layout configuration dictionary (FuncDict) for the Route instance.

        Capsules the layout function along with 'layout_hero', 'layout_override'.

        Capsules custom configurations passed via 'props' or arbitrary keyword arguments (**kwargs)."""
        ...
class DecorativeLayout:
    @overload
    def __get__(self, instance: None, owner: type) -> DecorativeLayout: ...
    @overload
    def __get__(self, instance: object, owner: type) -> FuncDict | ObjCallableLayout: ...
    def __call__(self,
                 hero: bool | int | None = UNSET,
                 override: bool | None = UNSET,
                 props: dict[str, Any] | None = UNSET,
                 **kwargs: Any) -> Callable[[T], T]:
        """
        Decorates a callable to mark it as the layout for the containing class.

        Sets 'layout_hero' and 'layout_override' attributes for the containing class.

        Accepts additional layout configurations via the 'props' dictionary or arbitrary keyword arguments (**kwargs).
        """
        ...
class ObjCallableLayout:
    def __call__(self,
                 func: Callable[..., Any] = UNSET,
                 hero: bool | int | None = UNSET,
                 override: bool | None = UNSET,
                 props: dict[str, Any] | None = UNSET,
                 **kwargs: Any) -> Route:
        """
        Assigns the callable as the layout of the Route instance.
        
        Sets 'layout_hero', 'layout_override' properties of the Route instance.
        
        Applies custom layout configuration via 'props' or **kwargs.
        """
        ...

class ObjDecorativeView: # Case: @obj.use.view(hero=True) -> returns the decorator wrapper
    def __call__(self,
                 hero: bool | int | None = UNSET,
                 props: dict[str, Any] | None = UNSET,
                 **kwargs: Any) -> Callable[[T], T]:
        """
        Decorates a callable to set it as the view for the Route instance.

        Applies 'view_hero' property to the Route instance.

        Accepts additional view configurations via the 'props' dictionary or arbitrary keyword arguments (**kwargs).
        """
        ...
class CallableView:  # Case: use.view(func) -> returns payload dict 
    def __call__(self,
                 func: Callable[..., Any] = UNSET,
                 hero: bool | int | None = UNSET,
                 props: dict[str, Any] | None = UNSET,
                 **kwargs: Any) -> FuncDict:
        """
        Creates a view configuration dictionary (FuncDict) for the Route instance.

        Capsules the view function along with 'view_hero'.

        Capsules custom configurations passed via 'props' or arbitrary keyword arguments (**kwargs)."""
        ...
class DecorativeView:
    @overload
    def __get__(self, instance: None, owner: type) -> DecorativeView: ...
    @overload
    def __get__(self, instance: object, owner: type) -> FuncDict | ObjCallableView: ...

    def __call__(self,
                 hero: bool | int | None = UNSET,
                 props: dict[str, Any] | None = UNSET,
                 **kwargs: Any) -> Callable[[T], T]:
        """
        Decorates a callable to mark it as the view for the containing class.

        Sets 'view_hero' attribute for the containing class.

        Accepts additional view configurations via the 'props' dictionary or arbitrary keyword arguments (**kwargs).
        """
        ...
class ObjCallableView:
    def __call__(self,
                 func: Callable[..., Any] = UNSET,
                 hero: bool | int | None = UNSET,
                 props: dict[str, Any] | None = UNSET,
                 **kwargs: Any) -> Route:
        """
        Assigns the callable as the view of the Route instance.
        
        Sets 'view_hero' property of the Route instance.
        
        Applies custom view configuration via 'props' or **kwargs.
        """
        ...




    @overload # Decorator on a function
    def __call__(self,
                 path:str|None=UNSET, parents:list[Route|type]|None=UNSET,
                 children:list[Route]|None=UNSET,
                 fly_to:str|None=UNSET, layout = UNSET, layout_override:bool|None=UNSET,
                 fly_ins:list = UNSET, fly_in_override:bool|None=UNSET, 
                 fly_outs:list = UNSET, fly_out_override:bool|None=UNSET,
                 view_hero:bool|None=UNSET, layout_hero:bool|None=UNSET,
                 title:str|None=UNSET, icon:str|None=UNSET, loader=UNSET, props:dict|None=UNSET, **kwargs:Any 
                 ) -> Callable[[Union[Type[Any], Callable[..., Any]]], Any]: ...
    @overload # Decorator on a class
    def __call__(self,
                 path:str|None=UNSET, parents:list[Route|type]|None=UNSET,
                 view=UNSET, children:list[Route]=UNSET,
                 fly_to:str|None=UNSET, layout = UNSET, layout_override:bool|None=UNSET,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any
                 ) -> Callable[[Union[Type[Any], Callable[..., Any]]], Any]: ...
    @overload # Direct call with function
    def __call__(self, func: Callable[..., bool|str],
                 path:str=None, parents:list[Route|type]=None,
                 children:list[Route]=None,
                 fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any)-> Any: ...

    @overload # Direct call with a class
    def __call__(self, cls: type,
                 path:str=None, parents:list[Route|type]=None,
                 view=None, children:list[Route]=None,
                 fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any) -> Any: ...


    # index
    @overload # Decorator on a function
    def __call__(self, fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any 
                 ) -> Callable[[Union[Type[Any], Callable[..., Any]]], Any]: ...
    @overload # Decorator on a class
    def __call__(self, view=None, fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any
                 ) -> Callable[[Union[Type[Any], Callable[..., Any]]], Any]: ...
    @overload # Direct call with function
    def __call__(self, func: Callable[..., bool|str],
                 fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any)-> Any: ...
    @overload # Direct call with a class
    def __call__(self, cls: type, view=None,
                 fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any) -> Any: ...

class ObjDecorativeLoader: # Case: @obj.use.loader() -> returns the decorator wrapper
    def __call__(self,
                 props: dict[str, Any] | None = UNSET,
                 **kwargs: Any) -> Callable[[T], T]:
        """
        Decorates a callable to set it as the loader for the Route instance.

        Accepts additional loader configurations via the 'props' dictionary or arbitrary keyword arguments (**kwargs).
        """
        ...
class CallableLoader:  # Case: use.loader(func) -> returns payload dict 
    def __call__(self,
                 func: Callable[..., Any] = UNSET,
                 props: dict[str, Any] | None = UNSET,
                 **kwargs: Any) -> FuncDict:
        """
        Creates a loader configuration dictionary (FuncDict) for the Route instance.

        Capsules custom configurations passed via 'props' or arbitrary keyword arguments (**kwargs)."""
        ...
class DecorativeLoader:
    @overload
    def __get__(self, instance: None, owner: type) -> DecorativeLoader: ...
    @overload
    def __get__(self, instance: object, owner: type) -> FuncDict | ObjCallableLoader: ...

    def __call__(self,
                 props: dict[str, Any] | None = UNSET,
                 **kwargs: Any) -> Callable[[T], T]:
        """
        Decorates a callable to mark it as the loader for the containing class.

        Accepts additional loader configurations via the 'props' dictionary or arbitrary keyword arguments (**kwargs).
        """
        ...
class ObjCallableLoader:
    def __call__(self,
                 func: Callable[..., Any] = UNSET,
                 props: dict[str, Any] | None = UNSET,
                 **kwargs: Any) -> Route:
        """
        Assigns the callable as the loader of the Route instance.
        
        Applies custom loader configuration via 'props' or **kwargs.
        """
        ...




    @overload # Decorator on a function
    def __call__(self,
                 path:str|None=UNSET, parents:list[Route|type]|None=UNSET,
                 children:list[Route]|None=UNSET,
                 fly_to:str|None=UNSET, layout = UNSET, layout_override:bool|None=UNSET,
                 fly_ins:list = UNSET, fly_in_override:bool|None=UNSET, 
                 fly_outs:list = UNSET, fly_out_override:bool|None=UNSET,
                 view_hero:bool|None=UNSET, layout_hero:bool|None=UNSET,
                 title:str|None=UNSET, icon:str|None=UNSET, loader=UNSET, props:dict|None=UNSET, **kwargs:Any 
                 ) -> Callable[[Union[Type[Any], Callable[..., Any]]], Any]: ...
    @overload # Decorator on a class
    def __call__(self,
                 path:str|None=UNSET, parents:list[Route|type]|None=UNSET,
                 view=UNSET, children:list[Route]=UNSET,
                 fly_to:str|None=UNSET, layout = UNSET, layout_override:bool|None=UNSET,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any
                 ) -> Callable[[Union[Type[Any], Callable[..., Any]]], Any]: ...
    @overload # Direct call with function
    def __call__(self, func: Callable[..., bool|str],
                 path:str=None, parents:list[Route|type]=None,
                 children:list[Route]=None,
                 fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any)-> Any: ...

    @overload # Direct call with a class
    def __call__(self, cls: type,
                 path:str=None, parents:list[Route|type]=None,
                 view=None, children:list[Route]=None,
                 fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any) -> Any: ...


    # index
    @overload # Decorator on a function
    def __call__(self, fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any 
                 ) -> Callable[[Union[Type[Any], Callable[..., Any]]], Any]: ...
    @overload # Decorator on a class
    def __call__(self, view=None, fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any
                 ) -> Callable[[Union[Type[Any], Callable[..., Any]]], Any]: ...
    @overload # Direct call with function
    def __call__(self, func: Callable[..., bool|str],
                 fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any)-> Any: ...
    @overload # Direct call with a class
    def __call__(self, cls: type, view=None,
                 fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any) -> Any: ...



    @overload # Decorator on a function
    def __call__(self,
                 path:str|None=UNSET, parents:list[Route|type]|None=UNSET,
                 children:list[Route]|None=UNSET,
                 fly_to:str|None=UNSET, layout = UNSET, layout_override:bool|None=UNSET,
                 fly_ins:list = UNSET, fly_in_override:bool|None=UNSET, 
                 fly_outs:list = UNSET, fly_out_override:bool|None=UNSET,
                 view_hero:bool|None=UNSET, layout_hero:bool|None=UNSET,
                 title:str|None=UNSET, icon:str|None=UNSET, loader=UNSET, props:dict|None=UNSET, **kwargs:Any 
                 ) -> Callable[[Union[Type[Any], Callable[..., Any]]], Any]: ...
    @overload # Decorator on a class
    def __call__(self,
                 path:str|None=UNSET, parents:list[Route|type]|None=UNSET,
                 view=UNSET, children:list[Route]=UNSET,
                 fly_to:str|None=UNSET, layout = UNSET, layout_override:bool|None=UNSET,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any
                 ) -> Callable[[Union[Type[Any], Callable[..., Any]]], Any]: ...
    @overload # Direct call with function
    def __call__(self, func: Callable[..., bool|str],
                 path:str=None, parents:list[Route|type]=None,
                 children:list[Route]=None,
                 fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any)-> Any: ...

    @overload # Direct call with a class
    def __call__(self, cls: type,
                 path:str=None, parents:list[Route|type]=None,
                 view=None, children:list[Route]=None,
                 fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any) -> Any: ...


    # index
    @overload # Decorator on a function
    def __call__(self, fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any 
                 ) -> Callable[[Union[Type[Any], Callable[..., Any]]], Any]: ...
    @overload # Decorator on a class
    def __call__(self, view=None, fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any
                 ) -> Callable[[Union[Type[Any], Callable[..., Any]]], Any]: ...
    @overload # Direct call with function
    def __call__(self, func: Callable[..., bool|str],
                 fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any)-> Any: ...
    @overload # Direct call with a class
    def __call__(self, cls: type, view=None,
                 fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any) -> Any: ...

class ObjDecorativeFlyIn: # Case: @obj.use.fly_in(hero=True) -> returns the decorator wrapper
    def __call__(self,
                 inheritable: bool = True,
                 apply_per_view: bool = False,
                 override: bool | None = UNSET,
                 props: dict[str, Any] | None = UNSET,
                 **kwargs: Any) -> Callable[[T], T]:
        """
        Decorates a callable to set it as the fly_in for the Route instance.

        Sets 'inheritable' and 'apply_per_view' props of the fly_in.

        Applies 'fly_in_override' properties to the Route instance.

        Accepts additional fly_in configurations via the 'props' dictionary or arbitrary keyword arguments (**kwargs).
        """
        ...
class CallableFlyIn:  # Case: use.fly_in(func) -> returns payload dict 
    def __call__(self,
                 func: Callable[..., Any] = UNSET,
                 inheritable: bool = True,
                 apply_per_view: bool = False,
                 override: bool | None = UNSET,
                 props: dict[str, Any] | None = UNSET,
                 **kwargs: Any) -> FuncDict:
        """
        Creates a fly_in configuration dictionary (FuncDict) for the Route instance.

        Sets 'inheritable' and 'apply_per_view' props of the fly_in.

        Capsules the fly_in function along with 'fly_in_override' prop of the Route instance.

        Capsules custom configurations passed via 'props' or arbitrary keyword arguments (**kwargs)."""
        ...
class DecorativeFlyIn:
    @overload
    def __get__(self, instance: None, owner: type) -> DecorativeFlyIn: ...
    @overload
    def __get__(self, instance: object, owner: type) -> FuncDict | ObjCallableFlyIn: ...
    def __call__(self,
                 inheritable: bool = True,
                 apply_per_view: bool = False,
                 override: bool | None = UNSET,
                 props: dict[str, Any] | None = UNSET,
                 **kwargs: Any) -> Callable[[T], T]:
        """
        Decorates a callable to mark it as the fly_in for the containing class.

        Sets 'inheritable' and 'apply_per_view' props of the fly_in.

        Sets 'fly_in_override' attribute for the containing class.

        Accepts additional fly_in configurations via the 'props' dictionary or arbitrary keyword arguments (**kwargs).
        """
        ...
class ObjCallableFlyIn:
    def __call__(self,
                 func: Callable[..., Any] = UNSET,
                 inheritable: bool = True,
                 apply_per_view: bool = False,
                 override: bool | None = UNSET,
                 props: dict[str, Any] | None = UNSET,
                 **kwargs: Any) -> Route:
        """
        Assigns the callable as the fly_in of the Route instance.
        
        Sets 'inheritable' and 'apply_per_view' props of the fly_in.

        Sets 'fly_in_override' property of the Route instance.
        
        Applies custom fly_in configuration via 'props' or **kwargs.
        """
        ...


class ObjDecorativeFlyOut: # Case: @obj.use.fly_out(hero=True) -> returns the decorator wrapper
    def __call__(self,
                 inheritable: bool = False,
                 apply_per_view: bool = False,
                 override: bool | None = UNSET,
                 props: dict[str, Any] | None = UNSET,
                 **kwargs: Any) -> Callable[[T], T]:
        """
        Decorates a callable to set it as the fly_out for the Route instance.

        Sets 'inheritable' and 'apply_per_view' props of the fly_out.

        Applies 'fly_out_override' properties to the Route instance.

        Accepts additional fly_out configurations via the 'props' dictionary or arbitrary keyword arguments (**kwargs).
        """
        ...
class CallableFlyOut:  # Case: use.fly_out(func) -> returns payload dict 
    def __call__(self,
                 func: Callable[..., Any] = UNSET,
                 inheritable: bool = False,
                 apply_per_view: bool = False,
                 override: bool | None = UNSET,
                 props: dict[str, Any] | None = UNSET,
                 **kwargs: Any) -> FuncDict:
        """
        Creates a fly_out configuration dictionary (FuncDict) for the Route instance.

        Sets 'inheritable' and 'apply_per_view' props of the fly_out.

        Capsules the fly_out function along with 'fly_out_override' prop of the Route instance.

        Capsules custom configurations passed via 'props' or arbitrary keyword arguments (**kwargs)."""
        ...
class DecorativeFlyOut:
    @overload
    def __get__(self, instance: None, owner: type) -> DecorativeFlyOut: ...
    @overload
    def __get__(self, instance: object, owner: type) -> FuncDict | ObjCallableFlyOut: ...
    def __call__(self,
                 inheritable: bool = False,
                 apply_per_view: bool = False,
                 override: bool | None = UNSET,
                 props: dict[str, Any] | None = UNSET,
                 **kwargs: Any) -> Callable[[T], T]:
        """
        Decorates a callable to mark it as the fly_out for the containing class.

        Sets 'inheritable' and 'apply_per_view' props of the fly_out.

        Sets 'fly_out_override' attribute for the containing class.

        Accepts additional fly_out configurations via the 'props' dictionary or arbitrary keyword arguments (**kwargs).
        """
        ...
class ObjCallableFlyOut:
    def __call__(self,
                 func: Callable[..., Any] = UNSET,
                 inheritable: bool = False,
                 apply_per_view: bool = False,
                 override: bool | None = UNSET,
                 props: dict[str, Any] | None = UNSET,
                 **kwargs: Any) -> Route:
        """
        Assigns the callable as the fly_out of the Route instance.
        
        Sets 'inheritable' and 'apply_per_view' props of the fly_out.

        Sets 'fly_out_override' property of the Route instance.
        
        Applies custom fly_out configuration via 'props' or **kwargs.
        """
        ...


class ObjDecorativeChild: # Case: @obj.use.child() -> returns the decorator wrapper
    def __call__(self,
                 props: dict[str, Any] | None = UNSET,
                 **kwargs: Any) -> Callable[[T], T]:
        """
        Decorates a callable to create a Route instance from it. then appends it as a child for the parent instance.
        

        Accepts additional child configurations via the 'props' dictionary or arbitrary keyword arguments (**kwargs).
        """
        ...
class CallableChild:  # Case: use.child(func) -> returns payload dict 
    def __call__(self,
                 func: Callable[..., Any] = UNSET,
                 props: dict[str, Any] | None = UNSET,
                 **kwargs: Any) -> FuncDict:
        """
        Creates a child configuration dictionary (FuncDict) for the Route instance.

        Capsules custom configurations passed via 'props' or arbitrary keyword arguments (**kwargs)."""
        ...
class DecorativeChild:
    @overload
    def __get__(self, instance: None, owner: type) -> DecorativeChild: ...
    @overload
    def __get__(self, instance: object, owner: type) -> FuncDict | ObjCallableChild: ...

    def __call__(self,
                 props: dict[str, Any] | None = UNSET,
                 **kwargs: Any) -> Callable[[T], T]:
        """
        Decorates a callable to mark it as the child for the containing class.

        Accepts additional child configurations via the 'props' dictionary or arbitrary keyword arguments (**kwargs).
        """
        ...
class ObjCallableChild:
    def __call__(self,
                 func: Callable[..., Any] = UNSET,
                 props: dict[str, Any] | None = UNSET,
                 **kwargs: Any) -> Route:
        """
        Assigns the callable as the child of the Route instance.
        
        Applies custom child configuration via 'props' or **kwargs.
        """
        ...



    @overload # Decorator on a function
    def __call__(self,
                 path:str|None=UNSET, parents:list[Route|type]|None=UNSET,
                 children:list[Route]|None=UNSET,
                 fly_to:str|None=UNSET, layout = UNSET, layout_override:bool|None=UNSET,
                 fly_ins:list = UNSET, fly_in_override:bool|None=UNSET, 
                 fly_outs:list = UNSET, fly_out_override:bool|None=UNSET,
                 view_hero:bool|None=UNSET, layout_hero:bool|None=UNSET,
                 title:str|None=UNSET, icon:str|None=UNSET, loader=UNSET, props:dict|None=UNSET, **kwargs:Any 
                 ) -> Callable[[Union[Type[Any], Callable[..., Any]]], Any]: ...
    @overload # Decorator on a class
    def __call__(self,
                 path:str|None=UNSET, parents:list[Route|type]|None=UNSET,
                 view=UNSET, children:list[Route]=UNSET,
                 fly_to:str|None=UNSET, layout = UNSET, layout_override:bool|None=UNSET,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any
                 ) -> Callable[[Union[Type[Any], Callable[..., Any]]], Any]: ...
    @overload # Direct call with function
    def __call__(self, func: Callable[..., bool|str],
                 path:str=None, parents:list[Route|type]=None,
                 children:list[Route]=None,
                 fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any)-> Any: ...

    @overload # Direct call with a class
    def __call__(self, cls: type,
                 path:str=None, parents:list[Route|type]=None,
                 view=None, children:list[Route]=None,
                 fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any) -> Any: ...


    # index
    @overload # Decorator on a function
    def __call__(self, fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any 
                 ) -> Callable[[Union[Type[Any], Callable[..., Any]]], Any]: ...
    @overload # Decorator on a class
    def __call__(self, view=None, fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any
                 ) -> Callable[[Union[Type[Any], Callable[..., Any]]], Any]: ...
    @overload # Direct call with function
    def __call__(self, func: Callable[..., bool|str],
                 fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any)-> Any: ...
    @overload # Direct call with a class
    def __call__(self, cls: type, view=None,
                 fly_to:str=None, layout = None, layout_override:bool=None,
                 fly_ins = None, fly_in_override:bool=None, 
                 fly_outs=None, fly_out_override:bool=None,
                 view_hero:bool=None, layout_hero:bool=None,
                 title=None, icon=None, loader=None, props:dict=None, **kwargs:Any) -> Any: ...




class CallableChildren:
    @overload
    def __get__(self, instance: None, owner: type) -> CallableChildren: ...
    @overload
    def __get__(self, instance: object, owner: type) -> FuncDict | ObjCallableChildren: ...
    def __call__(self, *routes: Route)-> list[Route]: ...
class ObjCallableChildren:
    def __call__(self, *routes: Route) -> Route: ...

class CallableFlyIns:
    @overload
    def __get__(self, instance: None, owner: type) -> CallableFlyIns: ...
    @overload
    def __get__(self, instance: object, owner: type) -> FuncDict | ObjCallableFlyIns: ...
    def __call__(self, *fly_ins: Callable[..., Any] | FuncDict, override: bool | None = UNSET)-> list[FuncDict]: ...
class ObjCallableFlyIns:
    def __call__(self, *fly_ins: Callable[..., Any] | FuncDict, override: bool | None = UNSET)-> Route: ...

class CallableFlyOuts:
    @overload
    def __get__(self, instance: None, owner: type) -> CallableFlyOuts: ...
    @overload
    def __get__(self, instance: object, owner: type) -> FuncDict | ObjCallableFlyOuts: ...
    def __call__(self, *fly_outs: Callable[..., Any] | FuncDict, override: bool | None = UNSET)-> list[FuncDict]: ...
class ObjCallableFlyOuts:
    def __call__(self, *fly_outs: Callable[..., Any] | FuncDict, override: bool | None = UNSET)-> Route: ...

class CallableProps:
    def __call__(self, props: dict | None = UNSET, **kwargs)-> Route:
        """
        Accepts a dictionary of configurations directly, keyword arguments, or both.
        Explicit None overrides any previous props of the Route instance.
        """
        ...
class CallableTitle:
    def __call__(self, value: str | None = UNSET)-> Route: ...
class CallableIcon:
    def __call__(self, value: str | None = UNSET)-> Route: ...
class CallableFlyTo:
    def __call__(self, value: str | None = UNSET)-> Route: ...
class CallablePath:
    def __call__(self, value: str | None = UNSET)-> Route: ...
class CallableLayoutOverride:
    def __call__(self, value: bool | None = UNSET) -> Route: ...
class CallableFlyInOverride:
    def __call__(self, value: bool | None = UNSET) -> Route: ...
class CallableFlyOutOverride:
    def __call__(self, value: bool | None = UNSET) -> Route: ...
class CallableLayoutHero:
    def __call__(self, value: bool | int | None = UNSET)-> Route:  ...
class CallableViewHero:
    def __call__(self, value: bool | int | None = UNSET)-> Route:  ...
    
use: UseProxy

layout: DecorativeLayout
view: DecorativeView
loader: DecorativeLoader
fly_in: DecorativeFlyIn
fly_out: DecorativeFlyOut
child: DecorativeChild
index: DecorativeIndex

children: CallableChildren
fly_ins: CallableFlyIns
fly_outs: CallableFlyOuts
class Route: 
    use: UseProxy
    layout: DecorativeLayout
    view: _DecorativeView
    loader: _DecorativeLoader
    fly_in: _DecorativeFlyIn
    fly_out: _DecorativeFlyOut
    child: _DecorativeChild
    index: _DecorativeIndex

    children: list[Route] | CallableChildren = UNSET
    fly_ins: list[FuncDict] | CallableFlyIns = UNSET
    fly_outs: list[FuncDict] | CallableFlyOuts = UNSET
    props: dict | CallableProps = UNSET
    title: str | CallableTitle = UNSET
    icon: str | CallableIcon = UNSET
    path: str | CallablePath = UNSET
    fly_to: str | CallableFlyTo = UNSET
    layout_override: bool | CallableLayoutOverride = UNSET
    fly_in_override: bool | CallableFlyInOverride = UNSET
    fly_out_override: bool | CallableFlyOutOverride = UNSET
    layout_hero: bool | int | CallableLayoutHero = UNSET
    view_hero: bool | int | CallableViewHero = UNSET
    
@overload
def fly(page, path=None, *args, **kwargs):...
@overload
def fly(page, path=None, *args, **kwargs):...
def fly(page, path=None, *args, **kwargs):
    """
    ok, read this
    """
    ...



    
__all__=[]