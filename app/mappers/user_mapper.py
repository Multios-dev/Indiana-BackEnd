from app.db.models.user_model import User


class UserMapper:
    @staticmethod
    def to_user_entity(payload: "UserCreateInput") -> User:
        data = payload.model_dump(
            exclude={"contact"},
            exclude_none=True
        )
        return User(**data)

    @staticmethod
    def to_contact_entity(payload: "UserCreateInput", user_id:int) -> "Contact | None":
        if not payload.contact:
            return None
        data = payload.contact.model_dump(exclude_none=True)