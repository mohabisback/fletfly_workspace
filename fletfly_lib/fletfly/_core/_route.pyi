# fletfly.pyi
__all__=[Route]
from typing import Any, Callable, TypeVar, overload
from typing_extensions import TypedDict, Unpack

T = TypeVar("T", bound=Callable[..., Any])


class RouteKwargs(TypedDict, total=False, extra_items=Any):
    index: Route | None = ...
    fly_to: str | None = ...
    layout: Callable[..., Any] | UseFunc | None = ...
    layout_override: bool | None = ...
    fly_ins: list[UseFunc] | None = ...
    fly_in_override: bool | None = ...
    fly_outs: list[UseFunc] | None = ...
    fly_out_override: bool | None = ...
    view_hero: bool | int | None = ...
    layout_hero: bool | int | None = ...
    title: str | None = ...
    icon: Any | None = ...
    loader: Callable[..., Any] | UseFunc | None = ...
    props: dict[str, Any] | None = ...

class SharedKwargs(TypedDict, total=False, extra_items=Any):
    hero: bool | int | None = ...
    loader: Callable[..., Any] | UseFunc | None = ...
    props: dict[str, Any] | None = ...

class UseFunc: pass
class _MethodHandler: pass

class UseProxy:
    @overload
    def __get__(self, instance: None, owner: type) -> UseProxy: ...
    @overload
    def __get__(self, instance: object, owner: type) -> ObjUseProxy: ...
    
    @property
    def layout(self) -> UseLayoutCall: ...
    @property
    def view(self) -> UseViewCall: ...
    @property
    def loader(self) -> UseLoaderCall: ...
    @property
    def fly_in(self) -> UseFlyInCall: ...
    @property
    def fly_out(self) -> UseFlyOutCall: ...
    @property
    def child(self) -> UseChildCall: ...
    @property
    def index(self) -> UseIndexCall: ...

class ObjUseProxy:   
    @property
    def layout(self) -> ObjUseLayoutDecoration: ...
    @property
    def view(self) -> ObjUseViewDecoration: ...
    @property
    def loader(self) -> ObjUseLoaderDecoration: ...
    @property
    def fly_in(self) -> ObjUseFlyInDecoration: ...
    @property
    def fly_out(self) -> ObjUseFlyOutDecoration: ...
    @property
    def child(self) -> ObjUseChildDecoration: ...
    @property
    def index(self) -> ObjUseIndexDecoration: ...

class ObjUseLayoutDecoration: # @obj.use.layout(hero=True) -> wrarpped function
    def __call__(self,
                 hero: bool | int | None = ...,
                 override: bool | None = ...,
                 props: dict[str, Any] | None = ...,
                 **kwargs: Any) -> Callable[[T], T]:
        """
        Decorates a callable to set it as the layout for the Route instance.

        Applies 'layout_hero' and 'layout_override' properties to the Route instance.

        Accepts additional layout configurations via the 'props' dictionary or arbitrary keyword arguments (**kwargs).
        """
        ...
class UseLayoutCall:  # use.layout(func) -> returns payload dict 
    def __call__(self,
                 func: Callable[..., Any] = ...,
                 hero: bool | int | None = ...,
                 override: bool | None = ...,
                 props: dict[str, Any] | None = ...,
                 **kwargs: Any) -> UseFunc:
        """
        Creates a layout configuration dictionary (FuncDict).

        Capsules the layout function along with 'layout_hero', 'layout_override'.

        Capsules custom configurations passed via 'props' or arbitrary keyword arguments (**kwargs)."""
        ...
class DecorativeLayout:
    @overload
    def __get__(self, instance: None, owner: type) -> DecorativeLayout: ...
    @overload
    def __get__(self, instance: object, owner: type) -> UseFunc | ObjCallableLayout: ...
    def __call__(self,
                 hero: bool | int | None = ...,
                 override: bool | None = ...,
                 props: dict[str, Any] | None = ...,
                 **kwargs: Any) -> Callable[[T], T]:
        """
        Decorates a callable to mark it as the layout for the containing class.

        Sets 'layout_hero' and 'layout_override' attributes for the containing class.

        Accepts additional layout configurations via the 'props' dictionary or arbitrary keyword arguments (**kwargs).
        """
        ...
class ObjCallableLayout:
    def __call__(self,
                 func: Callable[..., Any] = ...,
                 hero: bool | int | None = ...,
                 override: bool | None = ...,
                 props: dict[str, Any] | None = ...,
                 **kwargs: Any) -> Route:
        """
        Assigns the callable as the layout of the Route instance.
        
        Sets 'layout_hero', 'layout_override' properties of the Route instance.
        
        Applies custom layout configuration via 'props' or **kwargs.
        """
        ...

class ObjUseViewDecoration: # @obj.use.view(hero=True) -> wrapped function
    def __call__(self,
                 hero: bool | int | None = ...,
                 props: dict[str, Any] | None = ...,
                 **kwargs: Any) -> Callable[[T], T]:
        """
        Decorates a callable to set it as the view for the Route instance.

        Applies 'view_hero' property to the Route instance.

        Accepts additional view configurations via the 'props' dictionary or arbitrary keyword arguments (**kwargs).
        """
        ...
class UseViewCall:  # use.view(func) -> returns payload dict 
    def __call__(self,
                 func: Callable[..., Any] = ...,
                 hero: bool | int | None = ...,
                 props: dict[str, Any] | None = ...,
                 **kwargs: Any) -> UseFunc:
        """
        Creates a view configuration dictionary (FuncDict).

        Capsules the view function along with 'view_hero'.

        Capsules custom configurations passed via 'props' or arbitrary keyword arguments (**kwargs)."""
        ...
class DecorativeView:
    @overload
    def __get__(self, instance: None, owner: type) -> DecorativeView: ...
    @overload
    def __get__(self, instance: object, owner: type) -> UseFunc | ObjCallableView: ...

    def __call__(self,
                 hero: bool | int | None = ...,
                 props: dict[str, Any] | None = ...,
                 **kwargs: Any) -> Callable[[T], T]:
        """
        Decorates a callable to mark it as the view for the containing class.

        Sets 'view_hero' attribute for the containing class.

        Accepts additional view configurations via the 'props' dictionary or arbitrary keyword arguments (**kwargs).
        """
        ...
class ObjCallableView:
    def __call__(self,
                 func: Callable[..., Any] = ...,
                 hero: bool | int | None = ...,
                 props: dict[str, Any] | None = ...,
                 **kwargs: Any) -> Route:
        """
        Assigns the callable as the view of the Route instance.
        
        Sets 'view_hero' property of the Route instance.
        
        Applies custom view configuration via 'props' or **kwargs.
        """
        ...

class ObjUseLoaderDecoration: # @obj.use.loader() -> wrapped function
    def __call__(self,
                 props: dict[str, Any] | None = ...,
                 **kwargs: Any) -> Callable[[T], T]:
        """
        Decorates a callable to set it as the loader for the Route instance.

        Accepts additional loader configurations via the 'props' dictionary or arbitrary keyword arguments (**kwargs).
        """
        ...
class UseLoaderCall:  # use.loader(func) -> returns payload dict 
    def __call__(self,
                 func: Callable[..., Any] = ...,
                 props: dict[str, Any] | None = ...,
                 **kwargs: Any) -> UseFunc:
        """
        Creates a loader configuration dictionary (FuncDict).

        Capsules custom configurations passed via 'props' or arbitrary keyword arguments (**kwargs)."""
        ...
class DecorativeLoader: # @loader/func
    @overload
    def __get__(self, instance: None, owner: type) -> DecorativeLoader: ...
    @overload
    def __get__(self, instance: object, owner: type) -> UseFunc | ObjCallableLoader: ...

    def __call__(self,
                 props: dict[str, Any] | None = ...,
                 **kwargs: Any) -> Callable[[T], T]:
        """
        Decorates a callable to mark it as the loader for the containing class.

        Accepts additional loader configurations via the 'props' dictionary or arbitrary keyword arguments (**kwargs).
        """
        ...
class ObjCallableLoader: # @ obj.loader(func)
    def __call__(self,
                 func: Callable[..., Any] = ...,
                 props: dict[str, Any] | None = ...,
                 **kwargs: Any) -> Route:
        """
        Assigns the callable as the loader of the Route instance.
        
        Applies custom loader configuration via 'props' or **kwargs.
        """
        ...

class ObjUseFlyInDecoration: # Case: @obj.use.fly_in(hero=True) -> wrapped function
    def __call__(self,
                 inheritable: bool = True,
                 apply_per_view: bool = False,
                 override: bool | None = ...,
                 props: dict[str, Any] | None = ...,
                 **kwargs: Any) -> Callable[[T], T]:
        """
        Decorates a callable to set it as the fly_in for the Route instance.

        Sets 'inheritable' and 'apply_per_view' props of the fly_in.

        Applies 'fly_in_override' properties to the Route instance.

        Accepts additional fly_in configurations via the 'props' dictionary or arbitrary keyword arguments (**kwargs).
        """
        ...
class UseFlyInCall:  # use.fly_in(func) -> returns payload dict 
    def __call__(self,
                 func: Callable[..., Any] = ...,
                 inheritable: bool = True,
                 apply_per_view: bool = False,
                 override: bool | None = ...,
                 props: dict[str, Any] | None = ...,
                 **kwargs: Any) -> UseFunc:
        """
        Creates a fly_in configuration dictionary (FuncDict).

        Sets 'inheritable' and 'apply_per_view' props of the fly_in.

        Capsules the fly_in function along with 'fly_in_override' prop of the Route instance.

        Capsules custom configurations passed via 'props' or arbitrary keyword arguments (**kwargs)."""
        ...
class DecorativeFlyIn:
    @overload
    def __get__(self, instance: None, owner: type) -> DecorativeFlyIn: ...
    @overload
    def __get__(self, instance: object, owner: type) -> UseFunc | ObjCallableFlyIn: ...
    def __call__(self,
                 inheritable: bool = True,
                 apply_per_view: bool = False,
                 override: bool | None = ...,
                 props: dict[str, Any] | None = ...,
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
                 func: Callable[..., Any] = ...,
                 inheritable: bool = True,
                 apply_per_view: bool = False,
                 override: bool | None = ...,
                 props: dict[str, Any] | None = ...,
                 **kwargs: Any) -> Route:
        """
        Assigns the callable as the fly_in of the Route instance.
        
        Sets 'inheritable' and 'apply_per_view' props of the fly_in.

        Sets 'fly_in_override' property of the Route instance.
        
        Applies custom fly_in configuration via 'props' or **kwargs.
        """
        ...

class ObjUseFlyOutDecoration: # @obj.use.fly_out(hero=True) -> wrapped function
    def __call__(self,
                 inheritable: bool = False,
                 apply_per_view: bool = False,
                 override: bool | None = ...,
                 props: dict[str, Any] | None = ...,
                 **kwargs: Any) -> Callable[[T], T]:
        """
        Decorates a callable to set it as the fly_out for the Route instance.

        Sets 'inheritable' and 'apply_per_view' props of the fly_out.

        Applies 'fly_out_override' properties to the Route instance.

        Accepts additional fly_out configurations via the 'props' dictionary or arbitrary keyword arguments (**kwargs).
        """
        ...
class UseFlyOutCall:  # use.fly_out(func) -> returns payload dict 
    def __call__(self,
                 func: Callable[..., Any] = ...,
                 inheritable: bool = False,
                 apply_per_view: bool = False,
                 override: bool | None = ...,
                 props: dict[str, Any] | None = ...,
                 **kwargs: Any) -> UseFunc:
        """
        Creates a fly_out configuration dictionary (FuncDict).

        Sets 'inheritable' and 'apply_per_view' props of the fly_out.

        Capsules the fly_out function along with 'fly_out_override' prop of the Route instance.

        Capsules custom configurations passed via 'props' or arbitrary keyword arguments (**kwargs)."""
        ...
class DecorativeFlyOut:
    @overload
    def __get__(self, instance: None, owner: type) -> DecorativeFlyOut: ...
    @overload
    def __get__(self, instance: object, owner: type) -> UseFunc | ObjCallableFlyOut: ...
    def __call__(self,
                 inheritable: bool = False,
                 apply_per_view: bool = False,
                 override: bool | None = ...,
                 props: dict[str, Any] | None = ...,
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
                 func: Callable[..., Any] = ...,
                 inheritable: bool = False,
                 apply_per_view: bool = False,
                 override: bool | None = ...,
                 props: dict[str, Any] | None = ...,
                 **kwargs: Any) -> Route:
        """
        Assigns the callable as the fly_out of the Route instance.
        
        Sets 'inheritable' and 'apply_per_view' props of the fly_out.

        Sets 'fly_out_override' property of the Route instance.
        
        Applies custom fly_out configuration via 'props' or **kwargs.
        """
        ...

class ObjUseChildDecoration: # @obj.use.child() -> wrapped function
    def __call__(self,
            path:str| None=...,
            view:UseFunc|Callable[..., Any]| None=...,
            children:list[Route]=[],
            parents:list[Route]=[],
            *uses:UseFunc,
            **kwargs: Unpack[RouteKwargs]
            ) -> Callable[[T], T]:
        """
        Decorates a callable to create a Route instance from it. then appends it as a child for the parent instance.

        Accepts complete configuration as a new route.

        Returns the decorated function.
        """
        ...
class UseChildCall:  # use.child(func) -> meaningless new child 
    def __call__(self,
                path:str| None=...,
                view:UseFunc|Callable[..., Any]| None=...,
                children:list[Route]=[],
                parents:list[Route]=[],
                *uses:UseFunc,
                **kwargs: Unpack[RouteKwargs]
                ) -> Route:
        """
        Creates a child route.

        Accepts complete configuration as a new route
         
        Returns the child route.
        """
        ...
class DecorativeChild: # @child -> Decorated 
    @overload
    def __get__(self, instance: None, owner: type) -> DecorativeChild: ...
    @overload
    def __get__(self, instance: object, owner: type) -> UseFunc | ObjCallableChild: ...

    def __call__(self,
                path:str| None=...,
                view:UseFunc|Callable[..., Any]| None=...,
                children:list[Route]=[],
                parents:list[Route]=[],
                *uses:UseFunc,
                **kwargs: Unpack[RouteKwargs]
                ) -> Callable[[T], T]:
        """
        Decorates a callable to mark it as the child for the containing class.

        Accepts complete configuration as a new route.

        Returns the Decorated function.
        """
        ...
class ObjCallableChild:# obj.child() -> new child 
    def __call__(self,
                path:str| None=...,
                view:UseFunc|Callable[..., Any]| None=...,
                children:list[Route]=[],
                parents:list[Route]=[],
                *uses:UseFunc,
                **kwargs: Unpack[RouteKwargs]
                ) -> Route:
        """
        Assigns the callable as the child of the Route instance.
        
        Accepts complete configuration as a new route.

        Returns the new child Route.
        """
        ...

class ObjUseIndexDecoration: # @obj.use.index() -> wrapped function
    def __call__(self,
            view:UseFunc|Callable[..., Any]| None=...,
            *uses:UseFunc,
            **kwargs: Unpack[RouteKwargs]
            ) -> Callable[[T], T]:
        """
        Decorates a callable to create a Route instance from it. then appends it as a index for the parent instance.

        Accepts complete configuration as a new route.

        Returns the decorated function.
        """
        ...
class UseIndexCall:  # use.index(func) -> meaningliess new index 
    def __call__(self,
                view:UseFunc|Callable[..., Any]| None=...,
                *uses:UseFunc,
                **kwargs: Unpack[RouteKwargs]
                ) -> Route:
        """
        Creates a index route.

        Accepts complete configuration as a new route
         
        Returns the index route.
        """
        ...
class DecorativeIndex: # @index -> Decorated 
    @overload
    def __get__(self, instance: None, owner: type) -> DecorativeIndex: ...
    @overload
    def __get__(self, instance: object, owner: type) -> UseFunc | ObjCallableIndex: ...

    def __call__(self,
                view:UseFunc|Callable[..., Any]| None=...,
                *uses:UseFunc,
                **kwargs: Unpack[RouteKwargs]
                ) -> Callable[[T], T]:
        """
        Decorates a callable to mark it as the index for the containing class.

        Accepts complete configuration as a new route.

        Returns the Decorated function.
        """
        ...
class ObjCallableIndex:# obj.index() -> new index 
    def __call__(self,
                view:UseFunc|Callable[..., Any]| None=...,
                *uses:UseFunc,
                **kwargs: Unpack[RouteKwargs]
                ) -> Route:
        """
        Assigns the callable as the index of the Route instance.
        
        Accepts complete configuration as a new route.

        Returns the new index Route.
        """
        ...

class CallableChildren:
    @overload
    def __get__(self, instance: None, owner: type) -> CallableChildren: ...
    @overload
    def __get__(self, instance: object, owner: type) -> UseFunc | ObjCallableChildren: ...
    def __call__(self, *routes: Route)-> list[Route]: ...
class ObjCallableChildren:
    def __call__(self, *routes: Route) -> Route: ...

class CallableFlyIns:
    @overload
    def __get__(self, instance: None, owner: type) -> CallableFlyIns: ...
    @overload
    def __get__(self, instance: object, owner: type) -> UseFunc | ObjCallableFlyIns: ...
    def __call__(self, *fly_ins: Callable[..., Any] | UseFunc, override: bool | None = ...)-> list[UseFunc]: ...
class ObjCallableFlyIns:
    def __call__(self, *fly_ins: Callable[..., Any] | UseFunc, override: bool | None = ...)-> Route: ...

class CallableFlyOuts:
    @overload
    def __get__(self, instance: None, owner: type) -> CallableFlyOuts: ...
    @overload
    def __get__(self, instance: object, owner: type) -> UseFunc | ObjCallableFlyOuts: ...
    def __call__(self, *fly_outs: Callable[..., Any] | UseFunc, override: bool | None = ...)-> list[UseFunc]: ...
class ObjCallableFlyOuts:
    def __call__(self, *fly_outs: Callable[..., Any] | UseFunc, override: bool | None = ...)-> Route: ...

class CallableProps:
    def __call__(self, props: dict | None = ..., **kwargs)-> Route:
        """
        Accepts a dictionary of configurations directly, keyword arguments, or both.
        Explicit None overrides any previous props of the Route instance.
        """
        ...

class CallablePath:
    def __call__(self, value: str | None = ...)-> Route: ...
class CallableName:
    def __call__(self, value: str | None = ...)-> Route: ...
class CallableTitle:
    def __call__(self, value: str | None = ...)-> Route: ...
class CallableIcon:
    def __call__(self, value: str | None = ...)-> Route: ...
class CallableFlyTo:
    def __call__(self, value: str | None = ...)-> Route: ...
class CallableLayoutOverride:
    def __call__(self, value: bool | None = ...) -> Route: ...
class CallableFlyInOverride:
    def __call__(self, value: bool | None = ...) -> Route: ...
class CallableFlyOutOverride:
    def __call__(self, value: bool | None = ...) -> Route: ...
class CallableLayoutHero:
    def __call__(self, value: bool | int | None = ...)-> Route:  ...
class CallableViewHero:
    def __call__(self, value: bool | int | None = ...)-> Route:  ...
class CallableHero:
    def __call__(self, value: bool | int | None = ...)-> Route:  ...
    
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
    view: DecorativeView
    loader: DecorativeLoader
    fly_in: DecorativeFlyIn
    fly_out: DecorativeFlyOut
    child: DecorativeChild
    index: DecorativeIndex

    children: list[Route] | CallableChildren = ...
    fly_ins: list[UseFunc] | CallableFlyIns = ...
    fly_outs: list[UseFunc] | CallableFlyOuts = ...
    props: dict | CallableProps = ...
    title: str | CallableTitle = ...
    icon: str | CallableIcon = ...
    path: str | CallablePath = ...
    fly_to: str | CallableFlyTo = ...
    layout_override: bool | CallableLayoutOverride = ...
    fly_in_override: bool | CallableFlyInOverride = ...
    fly_out_override: bool | CallableFlyOutOverride = ...
    layout_hero: bool | int | CallableLayoutHero = ...
    view_hero: bool | int | CallableViewHero = ...
    
    @overload
    def __new__(cls:type['Route'],
            path:str| None=...,
            view:UseFunc|Callable[..., Any]| None=...,
            children:list[Route]=[],
            *uses:UseFunc,
            **kwargs: Unpack[RouteKwargs]
            ) -> Route: ...
    @overload
    def __new__(cls: type['Route'],
                callable: T) -> T: ...
    @overload
    def __new__(cls:type['Route'],
            route: dict,
            path:str| None=...,
            view:UseFunc|Callable[..., Any]| None=...,
            children:list[Route]=[],
            *uses:UseFunc,
            **kwargs: Unpack[RouteKwargs]
            ) -> Route: ...
    @overload
    def __new__(cls:type['Route'],
            func: Callable[..., Any],
            path:str| None=...,
            children:list[Route]=[],
            *uses:UseFunc,
            **kwargs: Unpack[RouteKwargs]
            ) -> Route: ...
    def __new__(*args, **kwargs)->Any:
        """
        1/4 Creates new Route object from configurations, can be a decorator.
        
        2/4 Specially used as a decorator.
        
        3/4 Wraps a route dict, for auto detection and duplication.
        
        4/4 Creates new Route from callable function or class.
        """
        ...
    @overload
    def __call__(self,
        path:str| None=...,
        view:UseFunc|Callable[..., Any]| None=...,
        children:list[Route]=[],
        *uses:UseFunc,
        **kwargs: Unpack[RouteKwargs]
        ) -> Route: ...
    @overload
    def __call__(self, func: T) -> T: ...
    def __call__(*args, **kwargs)->Any:
        """
        1/2 Edits Route configurations

        2/2 Decoration
        """
        ...

class Shared: 
    view: DecorativeView
    loader: DecorativeLoader
    props: dict | CallableProps = ...
    name: str | CallableName = ...
    hero: bool | int | CallableHero = ...
    
    @overload
    def __new__(cls:type['Shared'],
            name:str| None=...,
            view:UseFunc|Callable[..., Any]| None=...,
            *uses:UseFunc,
            **kwargs: Unpack[SharedKwargs]
            ) -> Shared: ...
    @overload
    def __new__(cls: type['Shared'],
                callable: T) -> T: ...
    @overload
    def __new__(cls:type['Shared'],
            shared: dict,
            name:str| None=...,
            view:UseFunc|Callable[..., Any]| None=...,
            *uses:UseFunc,
            **kwargs: Unpack[SharedKwargs]
            ) -> Shared: ...
    @overload
    def __new__(cls:type['Shared'],
            func: Callable[..., Any],
            name:str| None=...,
            *uses:UseFunc,
            **kwargs: Unpack[SharedKwargs]
            ) -> Shared: ...
    def __new__(*args, **kwargs)->Any:
        """
        1/4 Creates new Shared object from configurations, can be a decorator.
        
        2/4 Specially used as a decorator.
        
        3/4 Wraps a shared dict, for auto detection and duplication.
        
        4/4 Creates new Shared from callable function or class.
        """
        ...
    @overload
    def __call__(self,
        name:str| None=...,
        view:UseFunc|Callable[..., Any]| None=...,
        *uses:UseFunc,
        **kwargs: Unpack[SharedKwargs]
        ) -> Shared: ...
    @overload
    def __call__(self, func: T) -> T: ...
    def __call__(*args, **kwargs)->Any:
        """
        1/2 Edits Shared configurations

        2/2 Decoration
        """
        ...

class Zone:
    def __init__(self,
                 modules:str|list[str],
                 routes:Route|type|dict|list[Route|type|dict]|None = None,
                 shared:Route|type|dict|list[Route|type|dict]|None = None,
                 path:str|None=None)-> None:
        """
        Creates a Zone object.

        Takes main module/modules of the sub project to be avoided in auto detection of main zone
        """
        ...

__all__=[]