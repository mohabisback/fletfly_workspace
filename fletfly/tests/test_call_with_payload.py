# fletfly/tests/test_call_with_payload.py
import fletfly
import pytest

_call_with_payload = fletfly._call_with_payload
_get_set_payload = fletfly._get_set_payload

# Global Mock Page Object
MOCK_PAGE = "flet_page_instance"

# ---------------------------------------------------------
# Sample Handlers for Live Testing
# ---------------------------------------------------------

def sample_clean_func(x, y="hi"):
    return x, y

def sample_with_page(page, user_id):
    return page, user_id

def sample_with_kwargs(page, item_id, **kwargs):
    return page, item_id, kwargs

def sample_fallback_no_args():
    return "no_args_fallback"

def sample_fallback_with_page(page):
    return page

class SampleHandler:
    def method(self, x, y="hi"):
        return x, y

    @classmethod
    def class_method(cls, x, y="hi"):
        return x, y

    @staticmethod
    def static_method(x, y="hi"):
        return x, y


# ---------------------------------------------------------
# Test Cases (Integration)
# ---------------------------------------------------------

def test_integration_basic_mapping():
    # x is required, y should fall back to its default "hi"
    res = _call_with_payload(sample_clean_func, MOCK_PAGE, [{"x": 10}], False, False)
    assert res == (10, "hi")


def test_integration_page_injection_and_priority():
    # The first dict has highest priority. user_id should be 101, not 202
    availables = [
        {"user_id": 101, "theme": "light"},
        {"user_id": 202, "theme": "dark"}
    ]
    res = _call_with_payload(sample_with_page, MOCK_PAGE, availables, False, False)
    assert res == (MOCK_PAGE, 101)


def test_integration_kwargs_forwarding():
    # Extra arguments should be captured by **kwargs smoothly
    availables = [{"item_id": 50, "extra_1": "val1", "extra_2": "val2"}]
    res = _call_with_payload(sample_with_kwargs, MOCK_PAGE, availables, False, False)
    assert res == (MOCK_PAGE, 50, {"extra_1": "val1", "extra_2": "val2"})


def test_integration_missing_argument_raises_error():
    # sample_clean_func requires 'x', providing only 'y' must raise ValueError
    with pytest.raises(ValueError) as exc_info:
        _call_with_payload(sample_clean_func, MOCK_PAGE, [{"y": "hello"}], False, False)
    assert "Missing required argument" in str(exc_info.value)


def test_integration_instance_method_execution():
    handler = SampleHandler()
    # Testing bound method execution through the framework pipeline
    res = _call_with_payload(handler.method, MOCK_PAGE, [{"x": 55}], False, False)
    assert res == (55, "hi")


def test_integration_classmethod_execution():
    # Testing classmethod execution through the framework pipeline (cls must be omitted)
    res = _call_with_payload(SampleHandler.class_method, MOCK_PAGE, [{"x": 77}], False, False)
    assert res == (77, "hi")


def test_integration_staticmethod_execution():
    # Testing staticmethod execution through the framework pipeline
    res = _call_with_payload(SampleHandler.static_method, MOCK_PAGE, [{"x": 88}], False, False)
    assert res == (88, "hi")


def test_integration_fallback_mechanism(monkeypatch):
    fallback_page = "fallback_page"
    
    # Force _get_set_payload to return None to test the raw function fallback
    monkeypatch.setattr(fletfly, "_get_set_payload", lambda func: None)
    
    # Should safely invoke functions based on their ability to accept the page argument
    assert _call_with_payload(sample_fallback_no_args, fallback_page, []) == "no_args_fallback"
    assert _call_with_payload(sample_fallback_with_page, fallback_page, []) == fallback_page