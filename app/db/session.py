from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

# engine is an object that manages the database connection
# it can open connections and send SQL queries
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True, # prints SQL queries in the terminal
)

# SessionLocal creates sessions
# each API request will have its own session
SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Function used to obtain a DB session
# FastAPI will use it with Depends(get_db)
async def get_db():
    """
    Creates a database session and closes it
    automatically after the request
    """
    async with SessionLocal() as session:
        yield session