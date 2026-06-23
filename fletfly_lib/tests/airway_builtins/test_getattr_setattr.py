# fletfly/tests/test_route_attributes.py
import pytest
from fletfly import Route, General

def test_getattr_resolves_standard_alias():
    """Verify __getattr__ routes standard aliases to their official fields."""
    # 'logo' is an alias for 'icon'
    aw = Route(icon="my_icon.png")
    assert aw.logo == "my_icon.png"

    # 'route' is an alias for 'path'
    aw2 = Route(path="/profile")
    assert aw2.path == "/profile"

def test_getattr_resolves_protected_alias():
    """Verify __getattr__ routes aliases for view and layout to their underscore versions."""
    def dummy_view(page): pass
    def dummy_layout(page): pass
    
    aw = Route(view=dummy_view, layout=dummy_layout)
    
    # 'viewer', 'view', 'element' map to view -> stored in _view
    assert aw.viewer["func"] == dummy_view
    assert aw.view["func"] == dummy_view
    assert aw.element["func"] == dummy_view
    
    # 'frame' maps to layout -> stored in _layout
    assert aw.frame["func"] == dummy_layout

def test_getattr_raises_attribute_error_on_missing():
    """Verify __getattr__ raises AttributeError when field or alias does not exist."""
    aw = Route()
    with pytest.raises(AttributeError) as exc_info:
        _ = aw.non_existent_field
        
    assert "Route" in str(exc_info.value)
    assert "non_existent_field" in str(exc_info.value)

def test_setattr_and_getattr_interaction():
    """Verify explicit attribute updates reflect dynamically via aliases."""
    aw = Route()
    aw.icon = "new_icon.png"
    
    assert aw.icon == "new_icon.png"
    assert aw.logo == "new_icon.png"