from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Définir toutes les variables d'env dont l'app a besoin
    DATABASE_URL: str

    class Config:
        # Indique à pydantic d'aller lire dans le fichier .env
        env_file = ".env"

# Instance globale qu'on importe partout (évite de recréer la config à chaque fois)
settings = Settings()