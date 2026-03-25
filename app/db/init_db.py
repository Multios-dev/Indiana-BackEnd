from sqlalchemy import text
from app.db.session import engine
from app.db.base import Base
from app.db.model_loader import load_all_models

async def init_db():
    load_all_models()  # s'assure que tous les modèles sont connus avant create_all
    async with engine.begin() as conn:
        result = await conn.execute(text(
            "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users')"
        ))
        exists = result.scalar()

        if not exists:
            print("Aucune table trouvée. Création...")
            await conn.run_sync(Base.metadata.create_all)
            print("Tables créées avec succès")
        else:
            print("Les tables existent déjà")