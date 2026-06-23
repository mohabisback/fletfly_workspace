# fletfly/tests/route_builtins/test_init.py
import pytest
from fletfly import Route, General

def test_defaults():
    """Verify Route sets up correct defaults and registers itself globally."""
    aw = Route()
    
    assert aw._view is None
    assert aw._layout is None
    assert aw._path is None
    assert aw.children == []
    assert aw.fly_ins == []
    assert aw.fly_outs == []
    assert aw.fly_ins == []
    assert aw.fly_outs == []
    assert aw._class is None
    
    assert aw in General._pending_routes

def test_init_with_arguments():
    """Verify explicit arguments are properly processed and stored."""
    def dummy_view(page): pass
    def dummy_layout(page): pass
    child_route = Route(path="/sub")

    aw = Route(
        path="/HOME", 
        view=dummy_view, 
        layout=dummy_layout, 
        children=[child_route],
        view_hero=True
    )

    assert aw.path == "/HOME"
    assert aw._view["func"] == dummy_view
    assert aw._layout["func"] == dummy_layout
    assert aw.children == [child_route]
    assert aw._view_hero == True

def test_adjust_locals_with_clsattres():
    """Verify kwargs aliases map correctly to official fields and get popped from kwargs."""
    def dummy_view(page): pass
    def dummy_layout(page): pass
    def useless_view(page): pass
    
    # 'frame' maps to layout, 'element' maps to view, 'logo' maps to icon
    aw = Route(frame=dummy_layout, element=useless_view, view=dummy_view, logo="company_logo.png")
    assert aw._layout["func"] == dummy_layout
    assert aw._view["func"] == dummy_view
    assert aw.icon == "company_logo.png"
    assert "element" in aw.props
    assert "frame" not in aw.props
    assert hasattr(aw, "frame") is True
    assert hasattr(aw, "element") is True
    assert hasattr(aw, "logo") is True

def test_new_class_decorator_without_parentheses():
    """Verify @Route directly on a class registers it in pending classes."""
    @Route
    class TargetClass:
        pass
    list(General._pending_routes)[0].path = "target-class"

def test_call_as_class_decorator():
    """Verify @obj on a class injects values and strips underscores from view/layout."""
    def dummy_view(page): pass
    aw = Route(path="/dashboard", view=dummy_view, title="Dashboard")

    @aw
    class DashboardView:
        pass

    assert aw._class is DashboardView

def test_call_reconfiguration():
    """Verify calling an existing instance updates its attributes via _adjust_locals."""
    aw = Route(path="/initial", title="Old Title")
    result = aw(path="/updated", title="New Title", view_hero=True)
    
    assert result is aw
    assert aw.path == "/updated"
    assert aw.title == "New Title"
    assert aw._view_hero == True