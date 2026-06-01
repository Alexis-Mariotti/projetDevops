

import pytest
import os
import tempfile
from forest_fire_simulator import ForestFireSimulator, TerrainType, Position


class TestIntegration:
    """Tests d'intégration complets"""

    def test_complete_workflow(self):
        """Teste le flux complet: créer, simuler, optimiser, exporter"""
        # Créer un simulateur
        sim = ForestFireSimulator(15, 15, 40)

        # Trouver une position d'arbre pour démarrer le feu
        start_pos = None
        for y in range(15):
            for x in range(15):
                if sim.map[y][x] == TerrainType.TREE:
                    start_pos = Position(x, y)
                    break
            if start_pos:
                break

        # Si aucun arbre trouvé, générer une autre carte
        if not start_pos:
            sim = ForestFireSimulator(15, 15, 60)
            for y in range(15):
                for x in range(15):
                    if sim.map[y][x] == TerrainType.TREE:
                        start_pos = Position(x, y)
                        break
                if start_pos:
                    break

        # Simuler un incendie
        fire_map, burned = sim.simulate_fire(start_pos)
        burned_count = len(burned)

        # Trouver la meilleure case à déboiser
        best_pos, min_burned = sim.find_best_clearing(start_pos)

        # Vérifier les résultats
        assert burned_count > 0
        assert min_burned <= burned_count
        assert best_pos is not None

        # Exporter les résultats
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, 'complete_test.html')
            sim.export_to_html(output_file, fire_map, burned, best_pos)
            assert os.path.exists(output_file)

    def test_multiple_simulations_consistency(self):
        """Teste que les simulations donnent des résultats valides"""
        for _ in range(5):
            sim = ForestFireSimulator(20, 20, 35)

            # Trouver une position d'arbre pour démarrer le feu
            start_pos = None
            for y in range(20):
                for x in range(20):
                    if sim.map[y][x] == TerrainType.TREE:
                        start_pos = Position(x, y)
                        break
                if start_pos:
                    break

            # Si aucun arbre trouvé, sauter cette itération
            if not start_pos:
                continue

            fire_map, burned = sim.simulate_fire(start_pos)

            # Vérifier que tous les brûlés sont bien marqués comme brûlés
            for burned_pos in burned:
                assert fire_map[burned_pos.y][burned_pos.x] == TerrainType.BURNED



