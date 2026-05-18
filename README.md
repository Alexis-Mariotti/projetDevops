# 🔥 Simulateur de Feu de Forêt - Projet DevOps

## 📋 Description

Simulateur de feu de forêt développé en Python
Dispose d'une interface graphique et d'un export sous forme html

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

### Exécution

```bash
python forest_fire_simulator_tkinter.py
```

## 🧪 Tests

### Exécuter tous les tests

```bash
pytest -v
```

### Exécuter les tests avec couverture

```bash
pytest --cov=. --cov-report=html
```


