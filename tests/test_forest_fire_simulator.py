"""
Tests unitaires pour le simulateur de feu de forêt
"""

import pytest
import os
import tempfile
from forest_fire_simulator import (
    ForestFireSimulator, TerrainType, Position
)


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


class TestClearingOptimization:
    """Tests pour la recherche de la meilleure case à déboiser"""

    def test_find_best_clearing_returns_valid_position(self):
        """Teste que la meilleure position est valide"""
        sim = ForestFireSimulator(10, 10, 50)
        start_pos = Position(5, 5)

        best_pos, min_burned = sim.find_best_clearing(start_pos)

        # Vérifie que la position est dans la carte
        assert 0 <= best_pos.x < sim.width
        assert 0 <= best_pos.y < sim.height

        # Vérifie que la position était un arbre avant
        assert sim.map[best_pos.y][best_pos.x] == TerrainType.TREE

    def test_find_best_clearing_reduces_damage(self):
        """Teste que déboiser la meilleure case réduit les dégâts"""
        sim = ForestFireSimulator(10, 10, 50)
        start_pos = Position(5, 5)

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
        start_pos = Position(5, 5)
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


class TestIntegration:
    """Tests d'intégration complets"""

    def test_complete_workflow(self):
        """Teste le flux complet: créer, simuler, optimiser, exporter"""
        # Créer un simulateur
        sim = ForestFireSimulator(15, 15, 40)

        # Simuler un incendie
        start_pos = Position(7, 7)
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
            start_pos = Position(10, 10)

            fire_map, burned = sim.simulate_fire(start_pos)

            # Vérifier que tous les brûlés sont bien marqués comme brûlés
            for burned_pos in burned:
                assert fire_map[burned_pos.y][burned_pos.x] == TerrainType.BURNED

