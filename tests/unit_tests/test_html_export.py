
import pytest
import os
import tempfile
from forest_fire_simulator import ForestFireSimulator, Position, TerrainType


class TestHTMLExport:
    """Tests pour l'export HTML"""

    def test_html_export_creates_file(self):
        """Teste que l'export HTML crée un fichier"""
        sim = ForestFireSimulator(10, 10, 30)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, 'test_output.html')

            sim.export_to_html(output_file)

            assert os.path.exists(output_file)
            assert os.path.getsize(output_file) > 0

    def test_html_export_with_fire_simulation(self):
        """Teste l'export HTML avec une simulation de feu"""
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

        fire_map, burned = sim.simulate_fire(start_pos)
        best_pos, _ = sim.find_best_clearing(start_pos)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, 'test_with_fire.html')

            sim.export_to_html(output_file, fire_map, burned, best_pos)

            assert os.path.exists(output_file)

            # Vérifier que le fichier contient du contenu HTML valide
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
                assert '<!DOCTYPE html>' in content
                assert 'Simulateur de Feu de Forêt' in content

    def test_html_export_contains_map_cells(self):
        """Teste que l'HTML contient les cellules de la carte"""
        sim = ForestFireSimulator(5, 5, 30)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, 'test_cells.html')

            sim.export_to_html(output_file)

            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Vérifier la présence de cellules
                assert 'class="cell' in content



