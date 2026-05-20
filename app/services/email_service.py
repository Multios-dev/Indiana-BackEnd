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

    async def send_registration_email(self, to: str, last_name: str, first_name: str):
        payload = {
            "M_NomProduit": "",
            "M_DateVersion": "",
            "M_Version_Installee": "",
            "M_Corps_Message": "",
            "M_Variable_Libre": "",
            "M_ContexteID": 1,
            "M_TemplateId": 7966388,
            "M_AdresseMailExpediteur": "support@multios.be",
            "M_LOGIN": "Indiana",
            "M_Programmation": "00000000000000000",
            "M_CleReconnaissanceGroupe": "",
            "M_CleReconnaissanceEnvoiListeDiffusion": "",
            "M_Contexte_NomFichier": "",
            "M_Contexte_NomCle": "",
            "M_Contexte_IDFichier": "",
            "M_TAB_Liste": [
                {
                    "M_NomSociete": "",
                    "M_Civilite": "",
                    "M_NomContact": last_name,
                    "M_PrenomContact": first_name,
                    "M_AdresseMail": to,
                    "M_Corps_Message_Personnalise": "",
                    "M_CC": "",
                    "M_CleReconnaissanceListeDiffusion": "",
                    "M_NomFichierLigne": "",
                    "M_NomCleFichierLigne": "",
                    "M_ValeurCleLigne": ""
                }
            ],
            "M_TAB_Liste_Textes": [],
            "M_TAB_Liste_Fichiers": []
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.mailjet_base_url}/api/ext/mailjet/sendemails",
                headers={
                    "X-API-Key": settings.mailjet_api_key,
                    "Content-Type": "application/json"
                },
                json=payload
            )
            return response.json()

    # TODO : envoyer un mail lorsqu'on invite un utilisateur