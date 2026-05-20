FROM python:3.11-slim

# Variables utiles
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dossier de travail
WORKDIR /app

# Dépendances système (important pour PostgreSQL)
RUN apt-get update && apt-get install -y gcc libpq-dev

# Installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier ton projet
COPY . .

# Lancer ton API FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]