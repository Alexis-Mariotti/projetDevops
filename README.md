# Simulateur de Feu de Forêt - Projet DevOps

## Description

Simulateur de feu de forêt développé en Python
Dispose d'une interface graphique (tkinter) et d'un export sous forme html

## Installation et utilisation

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

## Tests

Les tests sont réalisés avec pytest

### Exécuter tous les tests

```bash
pytest -v
```

### Exécuter les tests avec rapport de couverture

Afficher rapport de couveture resumé dans le terminal
```bash
pytest --cov=.
```

Pour generer une version html du rapport de couverture
```bash
pytest --cov-report=html
```

