import resend
from app.core.config import settings
from jinja2 import Environment, FileSystemLoader

resend.api_key = settings.RESEND_API_KEY
templates = Environment(loader=FileSystemLoader('templates'))

def get_email_service():
    return EmailService()

class EmailService:
    async def send_registration_email(self, to:str, first_name:str) -> None:
        html = templates.get_template("registration.html").render(first_name=first_name)
        params: resend.Emails.SendParams = {
            "from" : settings.MAIL_FROM,
            "to" : [to],
            "subject" : "Bienvenue sur Indiana !",
            "html" : html
        }
        await resend.Emails.send_async(params)