
import pytest
from game.scripts.character import Character

@pytest.fixture
def character():
    return Character('Bob',13,4)

def test_character_class_create_new_print_info(character):
    print(character)