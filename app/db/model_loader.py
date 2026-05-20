import importlib
from pathlib import Path

import app.db.models

"""
This function automatically imports all Python files
found in the app.db.models folder

This is necessary because Alembic and SQLAlchemy only detect models
if they are imported. If a model exists in a file that was never loaded,
Alembic won't "see" that model.

This function avoids having to manually write in env.py:
- from app.db.models import Person
- etc.

From now on, every time a new file is added to app/db/models,
it will be automatically imported.
"""
def load_all_models():
    # Path to the models folder
    models_path = Path(app.db.models.__file__).parent

    # Python package name
    package_name = "app.db.models"

    # Iterate over files in the models folder
    for file in models_path.iterdir():

        # Ignore folders, __init__.py and non-Python files
        if file.is_file() and file.suffix == ".py" and file.stem != "__init__":

            # Example:
            # file = user_model.py
            # file.stem = "user"
            module_name = file.stem

            # Build the Python module path (-> app.db.models.user)
            module_path = f"{package_name}.{module_name}"

            # Import the module
            importlib.import_module(module_path)