
import pytest
from forest_fire_simulator import ForestFireSimulator, TerrainType


class TestMapGeneration:
    """Tests pour la génération de carte"""

    def test_map_dimensions(self):
        """Teste que la carte a les bonnes dimensions"""
        widths = [5, 10, 20]
        heights = [5, 15, 25]

        for w in widths:
            for h in heights:
                sim = ForestFireSimulator(w, h, 30)
                assert len(sim.map) == h
                for row in sim.map:
                    assert len(row) == w

    def test_map_contains_valid_terrain(self):
        """Teste que la carte ne contient que des types de terrain valides"""
        sim = ForestFireSimulator(20, 20, 30)
        valid_types = {TerrainType.WATER, TerrainType.BARE, TerrainType.TREE}

        for row in sim.map:
            for cell in row:
                assert cell in valid_types

    def test_trees_percentage_approximately_correct(self):
        """Teste que le pourcentage d'arbres est approximativement correct"""
        # Test avec un grand nombre de cellules pour avoir de la fiabilité
        sim = ForestFireSimulator(100, 100, 30)

        tree_count = 0
        for row in sim.map:
            for cell in row:
                if cell == TerrainType.TREE:
                    tree_count += 1

        total_cells = 100 * 100
        actual_percentage = (tree_count / total_cells) * 100

        # Permettre une variation de ±10%
        assert 20 <= actual_percentage <= 40

