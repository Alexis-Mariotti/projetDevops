
import pytest
from forest_fire_simulator import Position


class TestPosition:
    """Tests pour la classe Position"""

    def test_position_creation(self):
        """Teste la création d'une position"""
        pos = Position(5, 10)
        assert pos.x == 5
        assert pos.y == 10

    def test_position_equality(self):
        """Teste l'égalité de deux positions"""
        pos1 = Position(5, 10)
        pos2 = Position(5, 10)
        pos3 = Position(5, 11)

        assert pos1 == pos2
        assert pos1 != pos3

    def test_position_hash(self):
        """Teste que les positions peuvent être utilisées en set"""
        pos1 = Position(5, 10)
        pos2 = Position(5, 10)
        pos_set = {pos1, pos2}
        assert len(pos_set) == 1

