from ._core._route import fly_in, fly_out, view, layout, child, fly_ins, fly_outs, _View, _FlyIn, _FlyOut
from ._core._route import UseFunc, _DictAttr, Shared, Zone, use, index, _Layout
from ._core._route import Route, General, _get_set_payload, _call_with_payload
from ._core._Router import Router, fly, slot, data, StackMode
_route = Route
__all__ = ['Route', '_Router', 'Shared', 'Zone', 
           'fly', 'slot', 'data', 'StackMode', 
           'layout', 'view', 'loader', 'child', 'index', 'fly_in', 'fly_out', ]

