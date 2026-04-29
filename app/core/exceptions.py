"""
Exceptions for the application
Principe :
- Services raise these errors
- Routers handle nothing
- A global handler converts them to HTTP responses
"""

# Base exception for the application - all errors must inherit from this
class AppException(Exception):
    status_code = 400
    detail = "Application error"

    # allows passing a custom message
    def __init__(self, detail:str | None = None):
        self.detail = detail or self.__class__.detail
        super().__init__(self.detail)

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
class ConflictingEventLocationError(BadRequestError):
    detail = "An event cannot have both an address and GPS coordinates"

# ==============================
# 403 - BAD REQUEST
# ==============================
class ForbiddenError(AppException):
    status_code = 403
    detail = "Forbidden"
class PasswordError(ForbiddenError):
    detail = "Invalid password"
class NotAllowedGuardianError(ForbiddenError):
    detail = "Not a legal guardian"

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
class AddressNotFoundError(NotFoundError):
    detail = "Address not found"
class UserInvitedNotFoundError(NotFoundError):
    detail = "User invited not found"
class UserInviterNotFoundError(NotFoundError):
    detail = "User inviter not found"
class ParticipationNotFoundError(NotFoundError):
    detail = "Participation not found"

# ==============================
# 409 - CONFLICT
# ==============================
class ConflictError(AppException):
    status_code = 409
    detail = "Conflict"
class MaxGuardiansReachedError(ConflictError):
    detail = "A minor cannot have more than 2 guardians"
class RelationshipAlreadyExistsError(ConflictError):
    detail = "This guardian is already assigned to this minor"
class AlreadyInvitedError(ConflictError):
    detail = "User is already invited to this event"
# ==============================
# 500 - SERVER ERROR
# ==============================
class ServerError(AppException):
    status_code = 500
    detail = "Server error"
class DatabaseError(ServerError):
    detail = "Database error"