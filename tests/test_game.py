import pytest
from main import Hunter, Rabbit, Forest, is_inside_forest

@pytest.fixture
def hunter():
    return Hunter()

@pytest.fixture
def forest():
    # Create a forest object for testing
    forest = Forest(10, 5)
    forest.generate_rabbits(10)
    forest.generate_trees(1000)
    forest.generate_burrows(5)
    return forest

def test_hunter_move(forest, hunter):
    # Test the move method of the Hunter class
    original_position = hunter.position.copy()
    hunter.move()
    assert hunter.distance == 1
    assert hunter.position != original_position

def test_rabbit_move(forest):
    # Test the move method of the Rabbit class
    rabbit = Rabbit()
    original_position = rabbit.position.copy()
    rabbit.move()
    assert rabbit.distance == 1
    assert rabbit.position != original_position

def test_rabbit_seek_burrow(forest):
    # Test the seek_burrow method of the Rabbit class
    rabbit = Rabbit()
    burrow = forest.burrows[0]
    burrow.occupied = False
    rabbit.position = burrow.position.copy()
    assert rabbit.seek_burrow() is True
    assert burrow.occupied is True

def test_is_inside_forest():
    # Test the is_inside_forest function
    assert is_inside_forest([0, 0]) is True
    assert is_inside_forest([-1, 0]) is False
    assert is_inside_forest([10, 10]) is False
