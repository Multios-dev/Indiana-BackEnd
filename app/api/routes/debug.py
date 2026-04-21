from fastapi import APIRouter, BackgroundTasks, Depends
from app.services.email_service import EmailService, get_email_service

router = APIRouter(prefix="/debug", tags=["debug"])

@router.post("/send-test-email", summary="⚠️ TEST ONLY — Envoyer un mail de test")
async def send_test_email(
        background_tasks: BackgroundTasks,
        email_service: EmailService = Depends(get_email_service),
):
    background_tasks.add_task(
        email_service.send_registration_email,
        to="amel.multios@gmail.com",  # ← remplace par ton adresse
        first_name="Testeur",
    )
    return {"message": "Mail de test envoyé en arrière-plan."}