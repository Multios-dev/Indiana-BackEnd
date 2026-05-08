from app.db.models.address_model import Address
from app.db.models.user_model import User
from app.db.models.contact_model import Contact
from app.schemas.dtos.input.user_input import UserCreateInput

class UserMapper:
    @staticmethod
    def to_user_entity(payload: UserCreateInput) -> User:
        data = payload.model_dump(
            exclude={"contact", "home_address", "residential_address"},
            exclude_none=True
        )
        return User(**data)

    @staticmethod
    def to_contact_entity(payload: UserCreateInput, user_id: int):
        if not payload.contact:
            return None
        data = payload.contact.model_dump(exclude_none=True)
        return Contact(user_id=user_id, **data)

    @staticmethod
    def to_address_entity(address_payload) -> Address:
        """
        Creates an Address entity from an AddressInput DTO.
        The id is never passed here, PostgreSQL handles auto-increment.
        """
        data = address_payload.model_dump(exclude_none=True)
        return Address(**data)