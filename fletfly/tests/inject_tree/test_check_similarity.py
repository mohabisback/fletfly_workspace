# fletfly/tests/inject_tree/test_check_similarity.py

import pytest
from fletfly import Route

class DummyClass: pass

def dummy_view(page): pass
def dummy_view_alt(page): pass

def test_check_similarity_exact_match_with_view(capsys):
    """Verify that two Route nodes with identical paths and _view attributes return True and log a warning."""
    a1 = Route(path="home", view=dummy_view)
    a2 = Route(path="home", view=dummy_view)
    
    result = Route._check_similarity(a1, a2)
    
    assert result is True
    captured = capsys.readouterr()
    assert "[fletfly]: Duplication Warning: Route route with path='home' already added." in captured.out

def test_check_similarity_exact_match_with_class_attr(capsys):
    """Verify that two nodes with identical paths, classes, and view attributes return True and warn."""
    a1 = Route(path="dashboard")
    a1._class = DummyClass
    a1.view_clsattr = "view_main"
    
    a2 = Route(path="dashboard")
    a2._class = DummyClass
    a2.view_clsattr = "view_main"
    
    result = Route._check_similarity(a1, a2)
    
    assert result is True
    captured = capsys.readouterr()
    assert "[fletfly]: Duplication Warning: Route route with path='dashboard' already added." in captured.out

def test_check_similarity_mismatch_without_error_message():
    """Verify that if two nodes are different and no error message is specified, it returns False safely."""
    a1 = Route(path="home", view=dummy_view)
    a2 = Route(path="settings", view=dummy_view)
    
    result = Route._check_similarity(a1, a2, err_msg=None)
    assert result is False

def test_check_similarity_mismatch_raises_value_error():
    """Verify that if two nodes are different and an error message is specified, a ValueError is raised."""
    a1 = Route(path="home", view=dummy_view)
    a2 = Route(path="home", view=dummy_view_alt)
    
    custom_error = "Custom conflict detected!"
    with pytest.raises(ValueError, match=custom_error):
        Route._check_similarity(a1, a2, err_msg=custom_error)