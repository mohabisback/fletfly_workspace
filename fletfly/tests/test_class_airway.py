# fletfly/tests/airways/test_mixed_hierarchy.py
import pytest
from fletfly import Airway

def dummy_build(page):
    pass

def test_mixed_instance_class_hierarchy():
    # Scenario: Verify a deep mixed hierarchy where Airway instances 
    # and Classes alternate as parents and children.
    
    # 4. Level Four: Class (Leaf)
    class LevelFourClass:
        path = "level-four-class"
        build = dummy_build

    # 3. Level Three: Airway Instance (Father of Class)
    level_three_airway = Airway(path="level-three-airway")
    level_three_airway.subways=[LevelFourClass]

    # 2. Level Two: Class (Father of Airway Instance)
    class LevelTwoClass:
        path = "level-two-class"
        build = dummy_build
        subways = [level_three_airway]

    # 1. Level One: Airway Instance (Root - Father of Class)
    root_airway = Airway(path="root-airway")
    root_airway.subways=[LevelTwoClass]

    Airway._create_tree()

    # Assertions to verify the entire combined path resolution
    assert "/root-airway" in Airway._map
    assert "/root-airway/level-two-class" in Airway._map
    assert "/root-airway/level-two-class/level-three-airway" in Airway._map
    assert "/root-airway/level-two-class/level-three-airway/level-four-class" in Airway._map

def test_mixed_class_first_hierarchy():
    # Scenario: Verify an alternating mixed hierarchy starting with a Class at the root.
    # Class (Root) -> Airway Instance -> Class -> Airway Instance (Leaf)
    
    # 4. Level Four: Airway Instance (Leaf)
    level_four_airway = Airway(path="level-four-airway", _build=dummy_build)

    # 3. Level Three: Class (Father of Airway Instance)
    class LevelThreeClass:
        path = "level-three-class"
        build = dummy_build
        subways = [level_four_airway]

    # 2. Level Two: Airway Instance (Father of Class)
    level_two_airway = Airway(path="level-two-airway")
    level_two_airway.subways=[LevelThreeClass]

    # 1. Level One: Class (Root - Father of Airway Instance)
    class RootClass:
        path = "root-class"
        build = dummy_build
        subways = [level_two_airway]

    Airway._map = {}
    Airway._create_tree(handed_classes=[RootClass])

    for k, v in Airway._map.items():
        print(v, ",", k)
    # Assertions to verify the entire combined path resolution
    assert "/root-class" in Airway._map
    assert "/root-class/level-two-airway" in Airway._map
    assert "/root-class/level-two-airway/level-three-class" in Airway._map
    assert "/root-class/level-two-airway/level-three-class/level-four-airway" in Airway._map