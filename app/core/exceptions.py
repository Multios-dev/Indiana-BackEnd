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