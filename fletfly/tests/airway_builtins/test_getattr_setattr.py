# fletfly/tests/test_airway_attributes.py
import pytest
from fletfly import Airway

def test_getattr_resolves_standard_alias():
    """Verify __getattr__ routes standard aliases to their official fields."""
    # 'logo' is an alias for 'icon'
    aw = Airway(icon="my_icon.png")
    assert aw.logo == "my_icon.png"

    # 'route' is an alias for 'path'
    aw2 = Airway(path="/profile")
    assert aw2.path == "/profile"

def test_getattr_resolves_protected_alias():
    """Verify __getattr__ routes aliases for build and layout to their underscore versions."""
    def dummy_build(page): pass
    def dummy_layout(page): pass
    
    aw = Airway(build=dummy_build, layout=dummy_layout)
    
    # 'builder', 'view', 'element' map to build -> stored in _build
    assert aw.builder["func"] == dummy_build
    assert aw.view["func"] == dummy_build
    assert aw.element["func"] == dummy_build
    
    # 'frame' maps to layout -> stored in _layout
    assert aw.frame["func"] == dummy_layout

def test_getattr_raises_attribute_error_on_missing():
    """Verify __getattr__ raises AttributeError when field or alias does not exist."""
    aw = Airway()
    with pytest.raises(AttributeError) as exc_info:
        _ = aw.non_existent_field
        
    assert "Airway" in str(exc_info.value)
    assert "non_existent_field" in str(exc_info.value)

def test_setattr_and_getattr_interaction():
    """Verify explicit attribute updates reflect dynamically via aliases."""
    aw = Airway()
    aw.icon = "new_icon.png"
    
    assert aw.icon == "new_icon.png"
    assert aw.logo == "new_icon.png"