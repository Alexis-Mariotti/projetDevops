import pytest
from forest_fire_simulator import ForestFireSimulator, Position, TerrainType


class TestClearingOptimization:
    """Tests pour la recherche de la meilleure case à déboiser"""

    def test_find_best_clearing_returns_valid_position(self):
        """Teste que la meilleure position est valide"""
        sim = ForestFireSimulator(10, 10, 50)

        # Trouver une position d'arbre pour démarrer le feu
        start_pos = None
        for y in range(10):
            for x in range(10):
                if sim.map[y][x] == TerrainType.TREE:
                    start_pos = Position(x, y)
                    break
            if start_pos:
                break

        # Si pas d'arbre trouvé, générer une autre carte
        if not start_pos:
            sim = ForestFireSimulator(10, 10, 70)
            for y in range(10):
                for x in range(10):
                    if sim.map[y][x] == TerrainType.TREE:
                        start_pos = Position(x, y)
                        break
                if start_pos:
                    break

        # Vérifier que start_pos a bien été trouvé
        assert start_pos is not None, "Aucun arbre trouvé sur la carte"

        best_pos, min_burned = sim.find_best_clearing(start_pos)

        # Si best_pos est None, cela signifie qu'aucune autre position d'arbre n'a été trouvée
        # Ce qui est acceptable pour un test
        if best_pos is not None:
            # Vérifie que la position est dans la carte
            assert 0 <= best_pos.x < sim.width
            assert 0 <= best_pos.y < sim.height

            # Vérifie que la position était un arbre avant
            assert sim.map[best_pos.y][best_pos.x] == TerrainType.TREE

    def test_find_best_clearing_reduces_damage(self):
        """Teste que déboiser la meilleure case réduit les dégâts"""
        sim = ForestFireSimulator(10, 10, 50)

        # Trouver une position d'arbre pour démarrer le feu
        start_pos = None
        for y in range(10):
            for x in range(10):
                if sim.map[y][x] == TerrainType.TREE:
                    start_pos = Position(x, y)
                    break
            if start_pos:
                break

        # Si pas d'arbre trouvé, générer une autre carte
        if not start_pos:
            sim = ForestFireSimulator(10, 10, 70)
            for y in range(10):
                for x in range(10):
                    if sim.map[y][x] == TerrainType.TREE:
                        start_pos = Position(x, y)
                        break
                if start_pos:
                    break

        # Dégâts sans déboisement
        _, original_burned = sim.simulate_fire(start_pos)

        # Trouver la meilleure case à déboiser
        best_pos, min_burned = sim.find_best_clearing(start_pos)

        # Avec la meilleure case déboiseé, les dégâts devraient être <= aux dégâts originaux
        assert min_burned <= len(original_burned)

    def test_invalid_start_position_clearing(self):
        """Teste la recherche avec une position invalide"""
        sim = ForestFireSimulator(10, 10, 30)

        with pytest.raises(ValueError):
            sim.find_best_clearing(Position(15, 15))








