

import pytest
from forest_fire_simulator import ForestFireSimulator


class TestForestFireSimulatorInit:
    """Tests pour l'initialisation du simulateur"""

    def test_simulator_creation(self):
        """Teste la création d'un simulateur"""
        sim = ForestFireSimulator(10, 10, 30)
        assert sim.width == 10
        assert sim.height == 10
        assert sim.tree_percentage == 30
        assert len(sim.map) == 10
        assert len(sim.map[0]) == 10

    def test_invalid_tree_percentage_negative(self):
        """Teste avec un pourcentage d'arbres négatif"""
        with pytest.raises(ValueError):
            ForestFireSimulator(10, 10, -10)

    def test_invalid_tree_percentage_over_100(self):
        """Teste avec un pourcentage d'arbres > 100"""
        with pytest.raises(ValueError):
            ForestFireSimulator(10, 10, 150)

    def test_invalid_dimensions_zero_width(self):
        """Teste avec une largeur de 0"""
        with pytest.raises(ValueError):
            ForestFireSimulator(0, 10, 30)

    def test_invalid_dimensions_negative(self):
        """Teste avec des dimensions négatives"""
        with pytest.raises(ValueError):
            ForestFireSimulator(-5, 10, 30)

    def test_valid_tree_percentages(self):
        """Teste avec des pourcentages d'arbres valides"""
        for percentage in [0, 50, 100]:
            sim = ForestFireSimulator(10, 10, percentage)
            assert sim.tree_percentage == percentage

