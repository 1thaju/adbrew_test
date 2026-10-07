"""Application exceptions for todo operations."""


class TodoValidationError(Exception):
    """Raised when a todo payload does not meet validation requirements."""


class RepositoryError(Exception):
    """Raised when the todo repository cannot complete an operation."""
