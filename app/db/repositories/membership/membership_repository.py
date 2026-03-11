from app.db.repositories.membership.membership_interface import MembershipInterface

from sqlalchemy.ext.asyncio import AsyncSession

class MembershipRepository(MembershipInterface):
    def __init__(self, db:AsyncSession):
        # On garde une référence à la session db
        # Cette session permettra d'exécuter les requêtes
        self.db = db