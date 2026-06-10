# fletfly.pyi
from typing import overload, Callable, Any, TypeVar, Union, types, Literal
F = TypeVar("F", bound=Union[types.FunctionType, types.MethodType])
C = TypeVar("C", bound=type)
T = TypeVar("T", bound=Callable[..., Any])
class _MethodHandler:
    pass

class _Layout:
    @overload
    def __get__(self, instance: None, owner: type) -> '_Layout': ...
    @overload
    def __get__(self, instance: object, owner: type) -> '_ObjLayout': ...

    @overload
    def __call__(self, hero: Literal[True, False, None] = None, override: bool = None, props:dict=None, **kwargs:Any) -> Callable[[T], T]: ...
    @overload
    def __call__(self, func: Callable[..., Any], hero: Literal[True, False, None] = None, override: bool = None, props:dict=None, **kwargs: Any) -> dict: ...
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        1/2 Decorator usage:
            @layout(hero=True, param1=arg1)-> same function
            def function(): ...
        2/2 Direct call usage:
            layout = layout(function, hero=True, param1=arg1) -> {func:function, layout_hero:True, props={params1:arg1}}
        """
        ...
    
class _ObjLayout:
    @overload
    def __call__(self, hero: bool = None, override: bool = None) -> Route: ...
    @overload
    def __call__(self, func: Callable[..., Any], hero: bool = None, override: bool = None, props: dict = None, **kwargs: Any) -> Route: ...
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        1/2 Direct call usage:
            route_obj.layout(hero=True, override=False)->route_obj
        2/2 Direct call usage:
            route_obj.layout(function, hero=True, param1=arg1)->route_obj
        """
        ...

layout: _Layout

class Route: 
    layout: _Layout

@overload
def fly(page, path=None, *args, **kwargs):...
@overload
def fly(page, path=None, *args, **kwargs):...
def fly(page, path=None, *args, **kwargs):
    """
    ok, read this
    """
    ...