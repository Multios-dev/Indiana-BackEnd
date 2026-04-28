import httpx
from app.core.config import settings
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories.event.event_repository import EventRepository
from app.db.repositories.user.user_repository import UserRepository
from fastapi import Depends

from app.db.session import get_db
from app.schemas.dtos.input.event_input import InvitationEmailInput

templates = Environment(
    loader=FileSystemLoader(Path(__file__).parent.parent / "templates"),
    autoescape=select_autoescape(["html"]),
)

def get_email_service(db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    event_repo = EventRepository(db)
    return EmailService(user_repo, event_repo)

class EmailService:
    def __init__(self, user_repo: UserRepository, event_repo: EventRepository):
        self.user_repo = user_repo
        self.event_repo = event_repo

    async def send_registration_email(self, to:str, last_name:str, first_name:str, email:str):
        payload = {
            "M_ContexteID": 1,
            "M_TemplateID": 7966388,
            "M_AdresseMailExpediteur": "support@multios.be",
            "M_LOGIN": "Indiana",
            "M_Programmation": 00000000000000000,
            "M_TAB_Liste": [
                {
                    "M_NomContact": last_name,
                    "M_PrenomContact": first_name,
                    "M_AdresseMail": to
                }
            ]
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.MAILJET_BASE_URL}/api/ext/mailjet/sendemails",
                headers={"X-API-Key": settings.MAILJET_API_KEY},
                json=payload
            )
            return response.json()