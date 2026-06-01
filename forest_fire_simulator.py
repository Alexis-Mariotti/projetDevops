"""
Forest Fire Simulator - Main Module
Classe pour simuler et analyser les incendies de forêts
"""

import random
from enum import Enum
from typing import List, Tuple, Set
from dataclasses import dataclass
from datetime import datetime


class TerrainType(Enum):
    """Types de terrain possibles"""
    WATER = 0       # Plan d'eau
    BARE = 1        # Terrain nu
    TREE = 2        # Arbre
    BURNED = 3      # Terrain brûlé
    SAVED = 4       # Arbre sauvé par l'optimisation


@dataclass
class Position:
    """Représente une position sur la carte"""
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class ForestFireSimulator:
    """Simulateur de feu de forêt avec génération aléatoire de carte et analyse"""

    def __init__(self, width: int, height: int, tree_percentage: float = 30):
        """
        Initialise le simulateur

        Args:
            width: Largeur de la carte
            height: Hauteur de la carte
            tree_percentage: Pourcentage d'arbres (0-100)
        """
        if not (0 <= tree_percentage <= 100):
            raise ValueError("tree_percentage doit être entre 0 et 100")
        if width <= 0 or height <= 0:
            raise ValueError("Dimensions doivent être positives")

        self.width = width
        self.height = height
        self.tree_percentage = tree_percentage
        self.map = []
        self.generate_map()

    def generate_map(self):
        """Génère aléatoirement une carte"""
        self.map = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                rand = random.random() * 100
                if rand < 5:  # 5% de chance d'avoir de l'eau
                    row.append(TerrainType.WATER)
                elif rand < (5 + self.tree_percentage):  # Ajout du pourcentage d'arbres
                    row.append(TerrainType.TREE)
                else:  # Terrain nu
                    row.append(TerrainType.BARE)
            self.map.append(row)

    def get_neighbors(self, pos: Position) -> List[Position]:
        """Retourne les positions voisines (y compris diagonales) valides"""
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                new_x = pos.x + dx
                new_y = pos.y + dy
                if 0 <= new_x < self.width and 0 <= new_y < self.height:
                    neighbors.append(Position(new_x, new_y))
        return neighbors

    def simulate_fire(self, start_pos: Position) -> Tuple[List[List[TerrainType]], Set[Position]]:
        """
        Simule la progression du feu à partir d'une position donnée

        Args:
            start_pos: Position de départ du feu

        Returns:
            Tuple (carte résultante, ensemble des cases brûlées)

        Raises:
            ValueError: Si la position n'est pas valide ou n'est pas un arbre
        """
        if not self._is_valid_position(start_pos):
            raise ValueError(f"Position invalide: ({start_pos.x}, {start_pos.y})")

        # Le feu ne peut démarrer que sur un arbre
        if self.map[start_pos.y][start_pos.x] != TerrainType.TREE:
            raise ValueError(f"Le feu ne peut démarrer que sur un arbre. La position ({start_pos.x}, {start_pos.y}) est de type {self.map[start_pos.y][start_pos.x].name}")

        # Copie de la carte
        fire_map = [row[:] for row in self.map]
        burned = set()

        # BFS pour simuler la propagation du feu
        to_burn = [start_pos]

        while to_burn:
            current = to_burn.pop(0)

            if current in burned:
                continue

            # Le feu ne se propage que sur les arbres
            if fire_map[current.y][current.x] != TerrainType.TREE:
                continue

            burned.add(current)
            fire_map[current.y][current.x] = TerrainType.BURNED

            # Ajouter les voisins à brûler
            for neighbor in self.get_neighbors(current):
                if neighbor not in burned and fire_map[neighbor.y][neighbor.x] == TerrainType.TREE:
                    to_burn.append(neighbor)

        return fire_map, burned

    def find_best_clearing(self, fire_start_pos: Position) -> Tuple[Position, int, Set[Position]]:
        """
        Trouve la meilleure case d'arbre à déboiser pour minimiser l'incendie

        Args:
            fire_start_pos: Position de départ du feu

        Returns:
            Tuple (position optimale à déboiser, nombre de cases brûlées, ensemble des positions sauvées)

        Raises:
            ValueError: Si la position n'est pas valide ou n'est pas un arbre
        """
        if not self._is_valid_position(fire_start_pos):
            raise ValueError(f"Position invalide: ({fire_start_pos.x}, {fire_start_pos.y})")
        
        if self.map[fire_start_pos.y][fire_start_pos.x] != TerrainType.TREE:
            raise ValueError(f"Le feu doit démarrer sur un arbre. La position ({fire_start_pos.x}, {fire_start_pos.y}) est de type {self.map[fire_start_pos.y][fire_start_pos.x].name}")

        # Simuler sans déboisement
        _, original_burned = self.simulate_fire(fire_start_pos)
        best_clearing_pos = None
        min_burned = len(original_burned)
        best_burned_with_clearing = set()

        # Essayer de déboiser chaque arbre (sauf la position du feu)
        for y in range(self.height):
            for x in range(self.width):
                # Exclure la position de départ du feu
                if x == fire_start_pos.x and y == fire_start_pos.y:
                    continue
                
                if self.map[y][x] == TerrainType.TREE:
                    # Créer une map temporaire sans cet arbre
                    temp_map = self.map
                    self.map = [row[:] for row in self.map]
                    self.map[y][x] = TerrainType.BARE

                    # Simuler l'incendie
                    _, burned = self.simulate_fire(fire_start_pos)
                    burned_count = len(burned)

                    # Restaurer la map
                    self.map[y][x] = TerrainType.TREE
                    self.map = temp_map

                    # Mettre à jour le meilleur
                    if burned_count < min_burned:
                        min_burned = burned_count
                        best_clearing_pos = Position(x, y)
                        best_burned_with_clearing = burned

        # Calculer les arbres sauvés (brûlés sans déboisement mais pas avec)
        saved_positions = original_burned - best_burned_with_clearing

        return best_clearing_pos, min_burned, saved_positions

    def export_to_html(self, output_file: str, fire_map: List[List[TerrainType]] = None,
                       burned_positions: Set[Position] = None, clearing_pos: Position = None,
                       saved_positions: Set[Position] = None):
        """
        Exporte la carte en HTML pour visualisation

        Args:
            output_file: Chemin du fichier HTML de sortie
            fire_map: Carte après incendie (optionnel)
            burned_positions: Ensemble des positions brûlées (optionnel)
            clearing_pos: Position du déboisement optimal (optionnel)
            saved_positions: Ensemble des positions d'arbres sauvés (optionnel)
        """
        html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simulateur de Feu de Forêt</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            text-align: center;
        }}
        .info {{
            margin-bottom: 20px;
            padding: 10px;
            background-color: #e3f2fd;
            border-left: 4px solid #2196F3;
            border-radius: 4px;
        }}
        .map {{
            display: inline-block;
            border: 2px solid #333;
            margin: 20px 0;
        }}
        .cell {{
            width: 30px;
            height: 30px;
            display: inline-block;
            border: 1px solid #ddd;
            line-height: 30px;
            text-align: center;
            font-weight: bold;
        }}
        .water {{
            background-color: #64B5F6;
        }}
        .bare {{
            background-color: #D4AF37;
        }}
        .tree {{
            background-color: #2E8B57;
            color: white;
        }}
        .burned {{
            background-color: #8B4513;
            color: white;
        }}
        .clearing {{
             background-color: #FFD700;
             color: red;
             border: 3px solid red;
         }}
         .saved {{
             background-color: #90EE90;
             color: #2E8B57;
         }}
         .legend {{
            margin-top: 20px;
            padding: 15px;
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 4px;
        }}
        .legend-item {{
            margin: 8px 0;
            padding: 8px;
            display: flex;
            align-items: center;
        }}
        .legend-box {{
            width: 30px;
            height: 30px;
            margin-right: 10px;
            border: 1px solid #ddd;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Simulateur de Feu de Forêt</h1>
        
        <div class="info">
            <p><strong>Dimensions:</strong> {self.width}x{self.height}</p>
            <p><strong>Pourcentage d'arbres:</strong> {self.tree_percentage}%</p>
            <p><strong>Date de génération:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div style="text-align: center;">
"""

        # Ajouter la carte à afficher
        map_to_display = fire_map if fire_map is not None else self.map

        html_content += "            <div class=\"map\">\n"
        for y in range(self.height):
            for x in range(self.width):
                terrain = map_to_display[y][x]
                pos = Position(x, y)

                # Déterminer la classe CSS
                if clearing_pos and pos == clearing_pos:
                    css_class = "clearing"
                    symbol = "✂️"
                elif saved_positions and pos in saved_positions:
                    css_class = "saved"
                    symbol = "🌲"
                elif terrain == TerrainType.WATER:
                    css_class = "water"
                    symbol = "💧"
                elif terrain == TerrainType.BARE:
                    css_class = "bare"
                    symbol = "∘"
                elif terrain == TerrainType.TREE:
                    css_class = "tree"
                    symbol = "🌲"
                else:  # BURNED
                    css_class = "burned"
                    symbol = "🔥"

                html_content += f'                <div class="cell {css_class}">{symbol}</div>\n'
            html_content += "                <br/>\n"
        html_content += "            </div>\n"

        # Ajouter les statistiques
        if fire_map and burned_positions:
            html_content += f"""
        <div class="info" style="margin-top: 20px;">
            <h2>Résultats de la Simulation</h2>
            <p><strong>Cases brûlées:</strong> {len(burned_positions)}</p>
            <p><strong>Pourcentage de forêt détruite:</strong> {len(burned_positions) / (self.width * self.height) * 100:.2f}%</p>
"""
            if clearing_pos:
                html_content += f"            <p><strong>Case à déboiser (optimale):</strong> ({clearing_pos.x}, {clearing_pos.y})</p>\n"
            html_content += "        </div>\n"

        html_content += """
         <div class="legend">
             <h2>Légende</h2>
             <div class="legend-item">
                 <div class="legend-box water"></div>
                 <span>Plan d'eau</span>
             </div>
             <div class="legend-item">
                 <div class="legend-box bare"></div>
                 <span>Terrain nu</span>
             </div>
             <div class="legend-item">
                 <div class="legend-box tree"></div>
                 <span>Arbre</span>
             </div>
             <div class="legend-item">
                 <div class="legend-box burned"></div>
                 <span>Terrain brûlé</span>
             </div>
             <div class="legend-item">
                 <div class="legend-box clearing"></div>
                 <span>Case à déboiser (optimale)</span>
             </div>
             <div class="legend-item">
                 <div class="legend-box saved"></div>
                 <span>Arbre sauvé par l'optimisation</span>
             </div>
         </div>
     </div>
 </body>
 </html>
 """

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

    def _is_valid_position(self, pos: Position) -> bool:
        """Vérifie si une position est valide"""
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height

    def generate_map_with_saved(self, fire_map: List[List[TerrainType]],
                                saved_positions: Set[Position]) -> List[List[TerrainType]]:
        """
        Génère une carte avec les arbres sauvés marqués

        Args:
            fire_map: Carte avec les terrains brûlés
            saved_positions: Positions des arbres sauvés

        Returns:
            Carte avec les arbres sauvés marqués comme TerrainType.SAVED
        """
        map_to_display = [row[:] for row in fire_map]
        for pos in saved_positions:
            if 0 <= pos.x < self.width and 0 <= pos.y < self.height:
                map_to_display[pos.y][pos.x] = TerrainType.SAVED
        return map_to_display


if __name__ == '__main__':
    """Main pour tester le simulateur séparement de l'UI"""
    # Exemple d'utilisation
    simulator = ForestFireSimulator(width=20, height=20, tree_percentage=30)

    # Simuler un incendie
    start = Position(5, 5)
    fire_map, burned = simulator.simulate_fire(start)

    # Trouver la meilleure case à déboiser
    best_pos, min_burned = simulator.find_best_clearing(start)

    # Exporter en HTML
    simulator.export_to_html('output.html', fire_map, burned, best_pos)
    print(f"Simulation terminée. Fichier généré: output.html")
    print(f"Cases brûlées: {len(burned)}")
    print(f"Meilleure position à déboiser: ({best_pos.x}, {best_pos.y}) pour {min_burned} cases brûlées")

