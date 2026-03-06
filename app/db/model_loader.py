import importlib
from pathlib import Path

import app.db.models

"""
Cette fonction permet d'importer automatiquement tous les fichiers Python
présents dans le dossier app.db.models

C'est nécessaire parce que Alembic et SQLAlchemy ne détectent les modèles que
s'ils sont importés. Donc si un modèle existe dans un fichier, mais que ce
fichier n'a jamais été chargé, Alembic ne "voit" pas ce modèle.

Cette fonction évite de devoir écrire manuellement dans env.py :
- from app.db.models import Person
- etc.

Désormais, à chaque fois qu'on ajoute un nouveau fichier dans app/db/models,
il sera automatiquement importé.
"""
def load_all_models():
    # Chemin du dossier models
    models_path = Path(app.db.models.__file__).parent

    # Nom du package python
    package_name = "app.db.models"

    # On parcourt les fichiers du dossier models
    for file in models_path.iterdir():

        # On ignore les dossiers, __init__.py et les fichiers qui ne sont pas du Python
        if file.is_file() and file.suffix == ".py" and file.stem != "__init__":

            # Ex :
            # file = person.py
            # file.stem = "person"
            module_name = file.stem

            # On construit le chemin du modèle Python (-> app.db.models.person)
            module_path = f"{package_name}.{module_name}"

            # On importe le module
            importlib.import_module(module_path)