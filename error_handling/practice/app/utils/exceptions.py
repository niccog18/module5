"""
Custom application exceptions.
"""


class AppException(Exception):
    """
    Base exception for application errors.
    """

    def __init__(self, detail: str, status_code: int = 400):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)


class NotFoundException(AppException):
    """
    Raised when a resource cannot be found.
    """

    def __init__(self, resource: str, resource_id: int):
        super().__init__(
            detail=f"{resource} with id {resource_id} not found.",
            status_code=404
        )


class DuplicateException(AppException):
    """
    Raised when attempting to create a duplicate resource.
    """

    def __init__(self, resource: str, field: str, value: str):
        super().__init__(
            detail=f"{resource} with {field} '{value}' already exists.",
            status_code=409
        )


class BadRequestException(AppException):
    """
    Raised when business rules are violated.
    """

    def __init__(self, detail: str):
        super().__init__(
            detail=detail,
            status_code=400
        )