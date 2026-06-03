# fletfly/tests/test_airway_lifecycle.py
import pytest
from fletfly import Airway

def test_defaults():
    """Verify Airway sets up correct defaults and registers itself globally."""
    aw = Airway()
    
    assert aw._build is None
    assert aw._layout is None
    assert aw.path is None
    assert aw.subways == []
    assert aw.fly_ins == []
    assert aw.fly_outs == []
    assert aw.fly_ins_clsattr == []
    assert aw.fly_outs_clsattr == []
    assert aw._class is None
    
    assert aw in Airway._pending_airways

def test_init_with_arguments():
    """Verify explicit arguments are properly processed and stored."""
    def dummy_build(page): pass
    def dummy_layout(page): pass
    subway_route = Airway(path="/sub")

    aw = Airway(
        path="/HOME", 
        build=dummy_build, 
        layout=dummy_layout, 
        subways=[subway_route],
        build_hero=True
    )

    assert aw.path == "/home"
    assert aw._build == dummy_build
    assert aw._layout == dummy_layout
    assert aw.subways == [subway_route]
    assert aw.build_hero is True

def test_adjust_locals_with_clsattres():
    """Verify kwargs aliases map correctly to official fields and get popped from kwargs."""
    def dummy_build(page): pass
    def dummy_layout(page): pass
    def useless_build(page): pass
    
    # 'frame' maps to layout, 'element' maps to build, 'logo' maps to icon
    aw = Airway(frame=dummy_layout, element=useless_build, build=dummy_build, logo="company_logo.png")
    
    assert aw._layout == dummy_layout
    assert aw._build == dummy_build
    assert aw.icon == "company_logo.png"
    assert hasattr(aw, "frame") is True
    assert hasattr(aw, "element") is True
    assert hasattr(aw, "logo") is True

def test_new_class_decorator_without_parentheses():
    """Verify @Airway directly on a class registers it in pending classes."""
    @Airway
    class TargetClass:
        pass

    assert TargetClass in Airway._pending_classes
    assert isinstance(TargetClass, type)

def test_call_as_class_decorator():
    """Verify @obj on a class injects values and strips underscores from build/layout."""
    def dummy_build(page): pass
    aw = Airway(path="/dashboard", build=dummy_build, title="Dashboard")

    @aw
    class DashboardView:
        pass

    assert getattr(DashboardView, "path") == "/dashboard"
    assert getattr(DashboardView, "title") == "Dashboard"
    assert getattr(DashboardView, "build") == dummy_build
    assert not hasattr(DashboardView, "_build")

    assert aw._class is DashboardView
    assert DashboardView in Airway._pending_classes

def test_call_reconfiguration():
    """Verify calling an existing instance updates its attributes via _adjust_locals."""
    aw = Airway(path="/initial", title="Old Title")
    result = aw(path="/updated", title="New Title", build_hero=True)
    
    assert result is aw
    assert aw.path == "/updated"
    assert aw.title == "New Title"
    assert aw.build_hero is True