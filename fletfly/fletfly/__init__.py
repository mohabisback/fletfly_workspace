from .route import fly_in, fly_out, view, layout, child, fly_ins, fly_outs, _Layout, _View, _FlyIn, _FlyOut
from .route import UseFunc, _DictAttr, Shared, Zone, use
from .route import Route, General, _get_set_payload, _call_with_payload
from .Router import Router, fly, slot, data, StackMode
route = Route
__all__ = ['Route', 'route', 'Route', 'Router', 'Router', "General"
           'fly_in', 'fly_out', 'Zone', 'slot', 'data', 'layout', 'view', 'child']

