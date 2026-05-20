from sqlalchemy import text
from app.db.session import engine
from app.db.base import Base
from app.db.model_loader import load_all_models

async def init_db():
    load_all_models()  # ensures all models are loaded before create_all
    async with engine.begin() as conn:
        result = await conn.execute(text(
            "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users')"
        ))
        exists = result.scalar()

        if not exists:
            print("No tables found. Creating...")
            await conn.run_sync(Base.metadata.create_all)
            print("Tables created successfully")
        else:
            print("Tables already exist")