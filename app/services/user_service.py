from app.db.repositories.user.user_repository import UserRepository


class UserService:
    def __init__(self, repo:UserRepository):
        # Injection du repository
        self.repo = repo

    # Récupérer tous les utilisateurs
    async def get_all_users(self):
        existing = await self.repo.get_all()
        if not existing:
            raise ValueError("Users not found")
        return existing