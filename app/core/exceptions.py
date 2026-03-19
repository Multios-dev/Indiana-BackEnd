"""
Exceptions métier de l'application
Principe :
- Les services lèvent ces erreurs
- Les routers ne gèrent rien
- Un handler global transforme en HTTP
"""

# Exception de base pour l'application dont toutes les erreurs métier doivent hériter
class AppException(Exception):
    status_code = 400
    detail = "Application error"

    # permet de pouvoir passer un message custom
    def __init__(self, detail:str | None = None):
        self.detail = detail or self.__class__.detail
        super().__init__(self.detail)

# ==============================
# 404 - NOT FOUND
# ==============================
class NotFoundError(AppException):
    status_code = 404
    detail = "Resource not found"
class UserNotFoundError(NotFoundError):
    detail = "User not found"
class OrganizationNotFoundError(NotFoundError):
    detail = "Organization not found"
class MembershipNotFoundError(NotFoundError):
    detail = "Membership not found"
class ContactNotFoundError(NotFoundError):
    detail = "Contact not found"
class EventNotFoundError(NotFoundError):
    detail = "Event not found"

# ==============================
# 400 - BAD REQUEST
# ==============================
class BadRequestError(AppException):
    status_code = 400
    detail = "Bad request"
class InvalidDateRangeError(BadRequestError):
    detail = "End date cannot be earlier than start date"
class EmptyUpdatePayloadError(BadRequestError):
    detail = "No data provided for update"
class InvalidParentOrganizationError(BadRequestError):
    detail = "Parent organization does not exist"
class SelfParentOrganizationError(BadRequestError):
    detail = "An organization cannot be its own parent"
class DuplicateOrganizationError(BadRequestError):
    detail = "Organization already exists"
class DuplicateUserError(BadRequestError):
    detail = "User already exists"
class InvalidParentEventError(BadRequestError):
    detail = "Parent event does not exist"
class SelfParentEventError(BadRequestError):
    detail = "An event cannot be its own parent"

# ==============================
# 500 - SERVER ERROR
# ==============================
class ServerError(AppException):
    status_code = 500
    detail = "Server error"
class DatabaseError(ServerError):
    detail = "Database error"