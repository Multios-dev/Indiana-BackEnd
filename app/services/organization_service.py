from app.db.repositories.organization.organization_repository import OrganizationRepository


class OrganizationService:
    def __init__(self, repo:OrganizationRepository):
        self.repo = repo

    # Récupérer toutes les organisations
    async def get_all_organizations(self):
        organizations = await self.repo.get_all_organizations()
        if not organizations:
            raise ValueError("No organizations found")
        return organizations
