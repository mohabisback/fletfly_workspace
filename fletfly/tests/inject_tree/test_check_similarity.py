# fletfly/tests/inject_tree/test_check_similarity.py

import pytest
from fletfly import Airway

class DummyClass: pass

def dummy_build(page): pass
def dummy_build_alt(page): pass

def test_check_similarity_exact_match_with_build(capsys):
    """Verify that two Airway nodes with identical paths and _build attributes return True and log a warning."""
    a1 = Airway(path="home", build=dummy_build)
    a2 = Airway(path="home", build=dummy_build)
    
    result = Airway._check_similarity(a1, a2)
    
    assert result is True
    captured = capsys.readouterr()
    assert "[fletfly]: Duplication Warning: Airway route with path='home' already added." in captured.out

def test_check_similarity_exact_match_with_class_attr(capsys):
    """Verify that two nodes with identical paths, classes, and build attributes return True and warn."""
    a1 = Airway(path="dashboard")
    a1._class = DummyClass
    a1.build_clsattr = "view_main"
    
    a2 = Airway(path="dashboard")
    a2._class = DummyClass
    a2.build_clsattr = "view_main"
    
    result = Airway._check_similarity(a1, a2)
    
    assert result is True
    captured = capsys.readouterr()
    assert "[fletfly]: Duplication Warning: Airway route with path='dashboard' already added." in captured.out

def test_check_similarity_mismatch_without_error_message():
    """Verify that if two nodes are different and no error message is specified, it returns False safely."""
    a1 = Airway(path="home", build=dummy_build)
    a2 = Airway(path="settings", build=dummy_build)
    
    result = Airway._check_similarity(a1, a2, err_msg=None)
    assert result is False

def test_check_similarity_mismatch_raises_value_error():
    """Verify that if two nodes are different and an error message is specified, a ValueError is raised."""
    a1 = Airway(path="home", build=dummy_build)
    a2 = Airway(path="home", build=dummy_build_alt)
    
    custom_error = "Custom conflict detected!"
    with pytest.raises(ValueError, match=custom_error):
        Airway._check_similarity(a1, a2, err_msg=custom_error)