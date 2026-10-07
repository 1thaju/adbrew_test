"""Business logic for todo operations."""

from typing import Any, Dict, List

from .exceptions import TodoValidationError


class TodoService:
    """Validate todo requests and delegate persistence to a repository."""

    def __init__(self, repository: Any) -> None:
        """Initialize the service with an injected todo repository."""
        self.repository = repository

    def list_todos(self) -> List[Dict[str, Any]]:
        """Return todos from the repository."""
        return self.repository.list_all()

    def create_todo(self, payload: Any) -> Dict[str, Any]:
        """Validate a todo payload and create its todo."""
        if not isinstance(payload, dict):
            raise TodoValidationError("Request body must be a JSON object.")

        description = payload.get("description")
        if not isinstance(description, str):
            raise TodoValidationError("Description must be a string.")

        description = description.strip()
        if not description:
            raise TodoValidationError("Description cannot be empty.")
        if len(description) > 200:
            raise TodoValidationError("Description must be 200 characters or fewer.")

        return self.repository.create(description)
