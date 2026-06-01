
import pytest
from forest_fire_simulator import ForestFireSimulator, Position


class TestNeighbors:
    """Tests pour la méthode get_neighbors"""

    def test_neighbors_center(self):
        """Teste les voisins d'une position centrale"""
        sim = ForestFireSimulator(10, 10, 30)
        pos = Position(5, 5)
        neighbors = sim.get_neighbors(pos)

        # Une position centrale a 8 voisins
        assert len(neighbors) == 8

        # Vérifier que tous les voisins sont valides
        for neighbor in neighbors:
            assert 0 <= neighbor.x < 10
            assert 0 <= neighbor.y < 10

    def test_neighbors_corner(self):
        """Teste les voisins d'un coin"""
        sim = ForestFireSimulator(10, 10, 30)
        pos = Position(0, 0)
        neighbors = sim.get_neighbors(pos)

        # Un coin a 3 voisins
        assert len(neighbors) == 3

    def test_neighbors_edge(self):
        """Teste les voisins d'une position au bord"""
        sim = ForestFireSimulator(10, 10, 30)
        pos = Position(0, 5)
        neighbors = sim.get_neighbors(pos)

        # Une position au bord (non-coin) a 5 voisins
        assert len(neighbors) == 5

    def test_neighbors_includes_diagonals(self):
        """Teste que les voisins incluent les diagonales"""
        sim = ForestFireSimulator(10, 10, 30)
        pos = Position(5, 5)
        neighbors = sim.get_neighbors(pos)

        # Vérifier que les diagonales sont incluses
        expected_diagonals = [
            Position(4, 4), Position(6, 4),
            Position(4, 6), Position(6, 6)
        ]

        for diagonal in expected_diagonals:
            assert diagonal in neighbors

