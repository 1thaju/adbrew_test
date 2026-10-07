"""MongoDB persistence for todo items."""

from datetime import datetime, timezone
from typing import Any, Dict, List

from pymongo import DESCENDING
from pymongo.errors import PyMongoError

from .exceptions import RepositoryError


class TodoRepository:
    """Read and write todo items in an injected MongoDB collection."""

    def __init__(self, collection: Any) -> None:
        """Initialize the repository with its MongoDB collection."""
        self.collection = collection

    def list_all(self) -> List[Dict[str, Any]]:
        """Return all todos newest first, converting Mongo IDs to strings."""
        try:
            documents = self.collection.find().sort("created_at", DESCENDING)
            todos = []
            for document in documents:
                todo = dict(document)
                todo["id"] = str(todo.pop("_id"))
                todos.append(todo)
            return todos
        except PyMongoError as exc:
            raise RepositoryError("Unable to retrieve todos from the database.") from exc

    def create(self, description: str) -> Dict[str, Any]:
        """Persist and return a todo with a UTC creation timestamp."""
        todo = {
            "description": description,
            "created_at": datetime.now(timezone.utc),
        }
        try:
            result = self.collection.insert_one(todo)
            todo.pop("_id", None)
            todo["id"] = str(result.inserted_id)
            return todo
        except PyMongoError as exc:
            raise RepositoryError("Unable to create todo in the database.") from exc
