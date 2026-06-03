# fletfly/tests/test_get_set_payload.py
import fletfly, pytest
_get_set_payload = fletfly._get_set_payload

def sample_clean_func(x, y="hi"): pass

def sample_with_kwargs(page, **kwargs):
    pass

def sample_with_page(page, user_id):
    pass

def sample_with_positional_only(x, /, y):
    pass

class SampleClass:
    pass

class CallableClass:
    def __call__(self, page):
        pass


def test_clean_function_payload():
    res = _get_set_payload(sample_clean_func)
    assert res is not None
    assert res.get("page", None) is None
    assert res["params"]["x"] == "_fletfly"
    assert res["params"]["y"] == "hi"

def test_function_with_page_and_kwargs():
    res = _get_set_payload(sample_with_kwargs)
    assert res is not None
    assert res["params"]["page"] is True
    assert res["kwargs"] is True

def test_positional_only_exclusion():
    with pytest.raises(ValueError):
        _get_set_payload(sample_with_positional_only)

def test_cache_mechanism():
    res1 = _get_set_payload(sample_clean_func)
    res2 = _get_set_payload(sample_clean_func)
    assert res1 is res2

def test_invalid_targets():
    with pytest.raises(TypeError):
        assert _get_set_payload(SampleClass) is None
        assert _get_set_payload("not_a_callable") is None

def test_builtin_functions_handling():
    with pytest.raises(ValueError):
        _get_set_payload(print)

def sample_invalid_positional_only(x, /, y):
    pass

def sample_invalid_var_positional(x, *args):
    pass

# Update or add these test cases
def test_positional_only_raises_error():
    with pytest.raises(ValueError):
        _get_set_payload(sample_invalid_positional_only)

def test_var_positional_raises_error():
    with pytest.raises(ValueError):
        _get_set_payload(sample_invalid_var_positional)

class TestHandler:
    def method(self, x, y="hi"):
        pass

    @classmethod
    def class_method(cls, x, y="hi"):
        pass

    @staticmethod
    def static_method(x, y="hi"):
        pass

def test_class_methods():
    # self and cls must be excluded from params
    res = _get_set_payload(TestHandler().method)
    assert "self" not in res
    assert res["params"]["x"] == "_fletfly"
    assert res["params"]["y"] == "hi"

    res = _get_set_payload(TestHandler.class_method)
    assert "cls" not in res
    assert res["params"]["x"] == "_fletfly"
    assert res["params"]["y"] == "hi"

def test_static_method():
    res = _get_set_payload(TestHandler.static_method)
    assert res["params"]["x"] == "_fletfly"
    assert res["params"]["y"] == "hi"