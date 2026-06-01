import pytest
from forest_fire_simulator import ForestFireSimulator, TerrainType, Position


class TestFireSimulation:
    """Tests pour la simulation de feu"""

    def test_fire_spreads_to_trees(self):
        """Teste que le feu se propage aux arbres"""
        # Créer une petite carte maîtrisée
        sim = ForestFireSimulator(5, 5, 100)  # 100% d'arbres

        start_pos = Position(2, 2)
        fire_map, burned = sim.simulate_fire(start_pos)

        # Au moins la position de départ doit être brûlée
        assert start_pos in burned
        assert fire_map[start_pos.y][start_pos.x] == TerrainType.BURNED

    def test_fire_does_not_burn_water(self):
        """Teste que le feu ne brûle pas l'eau"""
        sim = ForestFireSimulator(5, 5, 0)  # 0% d'arbres
        # Setups manuel une petite carte
        sim.map = [
            [TerrainType.WATER, TerrainType.TREE, TerrainType.TREE, TerrainType.BARE, TerrainType.BARE],
            [TerrainType.TREE, TerrainType.TREE, TerrainType.TREE, TerrainType.BARE, TerrainType.BARE],
            [TerrainType.TREE, TerrainType.TREE, TerrainType.WATER, TerrainType.BARE, TerrainType.BARE],
            [TerrainType.BARE, TerrainType.BARE, TerrainType.BARE, TerrainType.BARE, TerrainType.BARE],
            [TerrainType.BARE, TerrainType.BARE, TerrainType.BARE, TerrainType.BARE, TerrainType.BARE],
        ]

        start_pos = Position(1, 0)
        fire_map, burned = sim.simulate_fire(start_pos)

        # Aucune cellule d'eau ne doit être brûlée
        for y in range(5):
            for x in range(5):
                if sim.map[y][x] == TerrainType.WATER:
                    assert fire_map[y][x] == TerrainType.WATER

    def test_invalid_start_position(self):
        """Teste avec une position de départ invalide"""
        sim = ForestFireSimulator(10, 10, 30)

        with pytest.raises(ValueError):
            sim.simulate_fire(Position(-1, 5))

        with pytest.raises(ValueError):
            sim.simulate_fire(Position(10, 5))

    def test_fire_spreads_diagonally(self):
        """Teste que le feu se propage en diagonale"""
        sim = ForestFireSimulator(3, 3, 0)
        # Setup une carte maîtrisée
        sim.map = [
            [TerrainType.TREE, TerrainType.BARE, TerrainType.TREE],
            [TerrainType.BARE, TerrainType.TREE, TerrainType.BARE],
            [TerrainType.TREE, TerrainType.BARE, TerrainType.TREE],
        ]

        start_pos = Position(1, 1)
        fire_map, burned = sim.simulate_fire(start_pos)

        # Le feu au centre devrait se propager aux diagonales
        assert Position(0, 0) in burned
        assert Position(2, 0) in burned
        assert Position(0, 2) in burned
        assert Position(2, 2) in burned

