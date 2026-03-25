from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DATABASE_URL = "postgresql+asyncpg://avnadmin:7bgJpfo0RVhv8A5DrLe1@postgresql-fbe70990-oa7247cc6.database.cloud.ovh.net:20184/indiana_test"

# engine est un objet qui gère la connexion à la base de données
# il peut ouvrir des connexions et envoyer des requêtes sql
engine = create_async_engine(
    DATABASE_URL,
    echo=True, # affiche les requêtes sql dans le terminal
)

# SessionLocal fabrique des sessions
# chaque requête API aura sa propre session
SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Fonctione utilisée pour obtenir une session DB
# FastAPI l'utilisera avec Depends(get_db)
async def get_db():
    """
    Crée une session de base de données et la ferme
    automatiquement après la requête
    """
    async with SessionLocal() as session:
        yield session