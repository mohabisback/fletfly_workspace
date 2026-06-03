# fletfly/tests/test_fly_ins_outs.py
import pytest
from fletfly import Airway

def sample_middleware_1(page): pass
def sample_middleware_2(page): pass
def sample_middleware_3(page): pass

def test_initial_data_loading():
    # Test if initial list data is loaded correctly during Airway initialization
    airway = Airway(fly_ins=[sample_middleware_1, sample_middleware_2])
    assert len(airway.fly_ins) == 2
    assert airway.fly_ins[0] == sample_middleware_1

def test_calling_as_callable_method():
    # Test calling fly_ins() as a method and updating the override attribute
    airway = Airway()
    result = airway.fly_ins(sample_middleware_1, sample_middleware_2, override=True)
    
    # Check chaining return value
    assert result is airway.fly_ins
    # Check internal data update
    assert len(airway.fly_ins) == 2
    # Check attribute dynamic assignment on owner
    assert airway.fly_ins_override is True

def test_list_mutations_append_and_extend():
    # Test that standard list operations work perfectly
    airway = Airway()
    
    # Test append
    airway.fly_ins.append(sample_middleware_1)
    assert len(airway.fly_ins) == 1
    assert airway.fly_ins[0] == sample_middleware_1
    
    # Test extend
    airway.fly_ins.extend([sample_middleware_2, sample_middleware_3])
    assert len(airway.fly_ins) == 3
    assert airway.fly_ins[2] == sample_middleware_3

def test_fly_outs_behavior():
    # Test fly_outs method call and its independent override attribute
    airway = Airway()
    airway.fly_outs(sample_middleware_3, override=False)
    
    assert airway.fly_outs_override is False
    assert airway.fly_outs == [sample_middleware_3]