"""Custom application exceptions for the Task Manager API."""


class NotFoundException(Exception):
    """
    Raised when a requested resource does not exist.
    """

    def __init__(self, message: str = "Resource not found"):
        self.message = message
        super().__init__(self.message)


class DuplicateException(Exception):
    """
    Raised when attempting to create a duplicate resource.
    """

    def __init__(self, message: str = "Resource already exists"):
        self.message = message
        super().__init__(self.message)


class ForbiddenException(Exception):
    """
    Raised when a user attempts to access a resource
    they do not have permission to access.
    """

    def __init__(self, message: str = "Access forbidden"):
        self.message = message
        super().__init__(self.message)