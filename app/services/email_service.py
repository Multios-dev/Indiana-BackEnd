import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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

    @staticmethod
    async def _send_email(to: str, subject: str, html: str) -> None:
        message = MIMEMultipart("alternative")
        message["From"] = settings.MAIL_FROM
        message["To"] = to
        message["Subject"] = subject
        message.attach(MIMEText(html, "html"))

        await aiosmtplib.send(
            message,
            hostname="smtp.gmail.com",
            port=587,
            username=settings.MAIL_FROM,
            password=settings.GMAIL_APP_PASSWORD,
            start_tls=True,
        )

    @staticmethod
    async def send_registration_email(to: str, first_name: str) -> None:
        try:
            html = templates.get_template("registration_template.html").render(first_name=first_name)
            await EmailService._send_email(to, "Bienvenue sur Indiana !", html)
        except Exception as e:
            print(e)
            raise

    @staticmethod
    async def send_invitation_event_email(self, payload: InvitationEmailInput) -> None:
        try:
            event = await self.event_repo.get_event_by_id(payload.event_id)
            invited = await self.user_repo.get_user_by_id(payload.invited_id)
            inviter = await self.user_repo.get_user_by_id(payload.inviter_id)

            html = templates.get_template("invite_template.html").render(
                first_name=invited.first_names[0],
                inviter_name=inviter.first_names[0],
                event_name=event.name,
                event_date=event.start_date.strftime("%d/%m/%Y à %Hh%M"),
                event_location=event.address.thoroughfare if event.address else "Lieu non défini",
            )
            await EmailService._send_email(
                to=invited.contact.email,
                subject="Tu as été invité(e) à un événement !",
                html=html
            )
        except Exception as e:
            print(e)
            raise