import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.core.config import settings
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path

templates = Environment(
    loader=FileSystemLoader(Path(__file__).parent.parent / "templates"),
    autoescape=select_autoescape(["html"]),
)

def get_email_service():
    return EmailService()

class EmailService:
    @staticmethod
    async def send_registration_email(to: str, first_name: str) -> None:
        try:
            html = templates.get_template("registration_template.html").render(first_name=first_name)
            message = MIMEMultipart("alternative")
            message["From"] = settings.MAIL_FROM
            message["To"] = to
            message["Subject"] = "Bienvenue sur Indiana !"
            message.attach(MIMEText(html, "html"))

            await aiosmtplib.send(
                message,
                hostname="smtp.gmail.com",
                port=587,
                username=settings.MAIL_FROM,
                password=settings.GMAIL_APP_PASSWORD,
                start_tls=True,
            )
        except Exception as e:
            print(e)
            raise

    @staticmethod
    async def send_invitation_event_email(to: str, first_name: str, inviter_name: str, event_name: str, event_date: str,
                                          event_location: str) -> None:
        try:
            html = templates.get_template("invite_template.html").render(
                first_name=first_name,
                inviter_name=inviter_name,
                event_name=event_name,
                event_date=event_date,
                event_location=event_location,
            )
            message = MIMEMultipart("alternative")
            message["From"] = settings.MAIL_FROM
            message["To"] = to
            message["Subject"] = "Tu as été invité(e) à un événement !"
            message.attach(MIMEText(html, "html"))

            await aiosmtplib.send(
                message,
                hostname="smtp.gmail.com",
                port=587,
                username=settings.MAIL_FROM,
                password=settings.GMAIL_APP_PASSWORD,
                start_tls=True,
            )
        except Exception as e:
            print(e)
            raise