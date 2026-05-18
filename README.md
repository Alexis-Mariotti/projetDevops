# 🔥 Simulateur de Feu de Forêt - Projet DevOps

## 📋 Description

Simulateur de feu de forêt développé en Python dans le cadre du cours "Tests et Intégration Continue" du CNAM. Ce projet implémente une classe pour simuler la propagation des incendies de forêt, analyser les dégâts et proposer les meilleures actions préventives.

### Fonctionnalités principales

1. **Génération aléatoire de carte** : Permet de créer une carte avec une distribution aléatoire d'arbres, d'eau et de terrain nu
2. **Simulation de feu** : Simule la propagation d'un incendie à partir d'une position donnée, en prenant en compte la propagation diagonale
3. **Optimisation du déboisement** : Trouve la meilleure case à déboiser pour minimiser les dégâts de l'incendie
4. **Export HTML** : Génère une visualisation HTML de la carte avec les résultats de la simulation

## 🏗️ Structure du projet

```
projetDevops/
├── forest_fire_simulator.py      # Module principal avec la classe ForestFireSimulator
├── test_forest_fire_simulator.py # Tests unitaires complets
├── requirements.txt              # Dépendances Python
├── README.md                     # Ce fichier
└── .github/
    └── workflows/
        └── tests.yml            # Configuration Github Actions pour CI/CD
```

## 🚀 Installation et utilisation

### Prérequis
- Python 3.8+

### Installation des dépendances

```bash
pip install -r requirements.txt
```

### Utilisation basique

```python
from forest_fire_simulator import ForestFireSimulator, Position

# Créer un simulateur (20x20 avec 30% d'arbres)
sim = ForestFireSimulator(width=20, height=20, tree_percentage=30)

# Simuler un incendie à la position (5, 5)
start_pos = Position(5, 5)
fire_map, burned_positions = sim.simulate_fire(start_pos)

# Trouver la meilleure case à déboiser
best_pos, min_burned = sim.find_best_clearing(start_pos)

# Exporter le résultat en HTML
sim.export_to_html('output.html', fire_map, burned_positions, best_pos)
```

### Exécution de l'exemple

```bash
python forest_fire_simulator.py
```

Cela génère un fichier `output.html` que vous pouvez ouvrir dans un navigateur.

## 🧪 Tests

### Exécuter tous les tests

```bash
pytest -v
```

### Exécuter les tests avec couverture

```bash
pytest --cov=. --cov-report=html
```

### Tests disponibles

- **TestPosition** : Tests de la classe Position
- **TestForestFireSimulatorInit** : Tests d'initialisation du simulateur
- **TestMapGeneration** : Tests de génération de carte
- **TestNeighbors** : Tests de détection des voisins
- **TestFireSimulation** : Tests de simulation de feu
- **TestClearingOptimization** : Tests d'optimisation du déboisement
- **TestHTMLExport** : Tests d'export HTML
- **TestIntegration** : Tests d'intégration complets

## 📊 Couverture de code

La couverture de code cible est supérieure à 90%. Les tests unitaires couvrent tous les cas nominaux et les cas limites.

## 🔄 Intégration Continue (CI/CD)

Ce projet utilise **Github Actions** pour automatiser les tests à chaque push ou pull request.

### Workflow CI
Le fichier `.github/workflows/tests.yml` configure :
- Tests sur Python 3.8, 3.9, 3.10, 3.11
- Vérification de style de code (flake8)
- Exécution de tests avec couverture (pytest)
- Upload automatique des rapports de couverture

## 🌿 Détails de l'algorithme

### Types de terrain
- **WATER** : Plan d'eau (le feu ne s'y propage pas)
- **BARE** : Terrain nu (le feu ne s'y propage pas)
- **TREE** : Arbre (le feu s'y propage)
- **BURNED** : Terrain brûlé (résultat de la simulation)

### Propagation du feu
L'algorithme utilise une **BFS (Breadth-First Search)** pour simuler la propagation du feu :
1. Commence à la position spécifiée
2. Propage le feu à tous les arbres voisins (8 directions, y compris diagonales)
3. Continue jusqu'à ce que le feu ne puisse plus se propager

### Optimisation du déboisement
La recherche de la meilleure case à déboiser :
1. Teste le déboisement de chaque arbre individuellement
2. Simule l'incendie avec chaque déboisement
3. Retourne la position qui minimise les dégâts

## 📈 Gestion des branches Git

Le projet utilise un modèle de branching structuré :

- **main** : Branch de production (releases)
- **develop** : Branch de développement (intégration)
- **features/** : Branches pour nouvelles fonctionnalités
- **bugfix/** : Branches pour corrections de bugs
- **docs/** : Branches pour documentation

Voir la section [Git Workflow](#git-workflow) pour les détails.

## 🎯 Roadmap

- [x] Classe simulateur de base
- [x] Génération aléatoire de carte
- [x] Simulation de fire propagation
- [x] Optimisation de déboisement
- [x] Export HTML
- [x] Tests unitaires complets
- [x] Intégration continue
- [ ] Optimisation des performances pour grandes cartes
- [ ] Interface graphique (optional)
- [ ] Visualisation en temps réel (optional)

## 📝 Licence

Ce projet est créé dans le cadre du cours CNAM.

## 👤 Auteur

Développé pour le projet DevOps - CNAM

## 📧 Contact

Pour toute question, veuillez contacter le responsable du cours.
