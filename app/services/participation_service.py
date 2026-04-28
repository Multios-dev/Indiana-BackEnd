import traceback
from app.core.exceptions import EventNotFoundError, UserNotFoundError, AlreadyInvitedError, DatabaseError
from app.db.models.participation_model import Participation
from app.db.repositories.event.event_repository import EventRepository
from app.db.repositories.participation.participation_repository import ParticipationRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.db.repositories.user.user_repository import UserRepository
from app.db.session import get_db

def get_participation_service(db:AsyncSession = Depends(get_db)):
    participation_repo = ParticipationRepository(db)
    event_repo = EventRepository(db)
    user_repo = UserRepository(db)
    return ParticipationService(participation_repo)

class ParticipationService:
    def __init__(
            self,
            participation_repo:ParticipationRepository,
            event_repo:EventRepository,
            user_repo:UserRepository
    ):
        self.participation_repo = participation_repo
        self.event_repo = event_repo
        self.user_repo = user_repo

    async def invite_to_event(self, participation:Participation):
        try:
            event = await self.event_repo.get_event_by_id(participation.event_id)
            if not event:
                raise EventNotFoundError()
            user = await self.user_repo.get_user_by_id(participation.user_id)
            if not user:
                raise UserNotFoundError()
            existing = await self.participation_repo.get_participation(participation.user_id, participation.event_id)
            if existing:
                raise AlreadyInvitedError()

            participation = Participation(
                user_id = participation.user_id,
                event_id = participation.event_id,
                role = "invited",
                price = participation.price,
            )
            return await self.participation_repo.invite_to_event(participation)
        except (EventNotFoundError, UserNotFoundError, AlreadyInvitedError):
            raise
        except Exception as e:
            traceback.print_exc()
            raise DatabaseError() from e