# fletfly/tests/routes/test_mixed_hierarchy.py
import pytest
from fletfly import Route, General

def dummy_view(page):
    pass

def test_mixed_instance_class_hierarchy():
    # Scenario: Verify a deep mixed hierarchy where Route instances 
    # and Classes alternate as parents and children.
    
    # 4. Level Four: Class (Leaf)
    class LevelFourClass:
        path = "level-four-class"
        view = dummy_view

    # 3. Level Three: Route Instance (Father of Class)
    level_three_route = Route(path="level-three-route")
    level_three_route.children=[LevelFourClass]

    # 2. Level Two: Class (Father of Route Instance)
    class LevelTwoClass:
        path = "level-two-class"
        view = dummy_view
        children = [level_three_route]

    # 1. Level One: Route Instance (Root - Father of Class)
    root_route = Route(path="root-route")
    root_route.children=[LevelTwoClass]

    Route._create_tree()

    # Assertions to verify the entire combined path resolution
    assert "/root-route" in General._tree_map
    assert "/root-route/level-two-class" in General._tree_map
    assert "/root-route/level-two-class/level-three-route" in General._tree_map
    assert "/root-route/level-two-class/level-three-route/level-four-class" in General._tree_map

def test_mixed_class_first_hierarchy():
    # Scenario: Verify an alternating mixed hierarchy starting with a Class at the root.
    # Class (Root) -> Route Instance -> Class -> Route Instance (Leaf)
    
    # 4. Level Four: Route Instance (Leaf)
    level_four_route = Route(path="level-four-route", _view=dummy_view)

    # 3. Level Three: Class (Father of Route Instance)
    class LevelThreeClass:
        path = "level-three-class"
        view = dummy_view
        children = [level_four_route]

    # 2. Level Two: Route Instance (Father of Class)
    level_two_route = Route(path="level-two-route")
    level_two_route.children=[LevelThreeClass]

    # 1. Level One: Class (Root - Father of Route Instance)
    class RootClass:
        path = "root-class"
        view = dummy_view
        children = [level_two_route]

    General._tree_map = {}
    Route._create_tree(handed_classes=[RootClass])

    for k, v in General._tree_map.items():
        print(v, ",", k)
    # Assertions to verify the entire combined path resolution
    assert "/root-class" in General._tree_map
    assert "/root-class/level-two-route" in General._tree_map
    assert "/root-class/level-two-route/level-three-class" in General._tree_map
    assert "/root-class/level-two-route/level-three-class/level-four-route" in General._tree_map