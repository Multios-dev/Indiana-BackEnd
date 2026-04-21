from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Environment variables
    DATABASE_URL: str
    KEYCLOAK_URL: str = ""  # Empty by default — auth bypass enabled in dev mode
    RESEND_API_KEY:str
    MAIL_FROM:str

    class Config:
        # Tell Pydantic to read from the .env file
        env_file = ".env"

# Global instance imported everywhere
settings = Settings()