"""
Fichier de configuration de pytest
On ajoute le répertoire parent au path pour que les imports fonctionnent correctement
"""

import os
import sys

# Ajouter le répertoire parent au chemin Python
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

