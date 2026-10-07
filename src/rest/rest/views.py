"""HTTP endpoints for todo operations."""

import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .database import db
from .exceptions import RepositoryError, TodoValidationError
from .repository import TodoRepository
from .services import TodoService


logger = logging.getLogger(__name__)
todo_service = TodoService(TodoRepository(db["todos"]))


class TodoListView(APIView):
    """Expose todo listing and creation over HTTP."""

    def get(self, request):
        """Return all todos."""
        try:
            return Response(todo_service.list_todos(), status=status.HTTP_200_OK)
        except RepositoryError:
            logger.exception("Failed to retrieve todos.")
            return Response(
                {"error": "Todo storage is temporarily unavailable."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

    def post(self, request):
        """Validate and create a todo."""
        try:
            todo = todo_service.create_todo(request.data)
            return Response(todo, status=status.HTTP_201_CREATED)
        except TodoValidationError as exc:
            return Response(
                {"error": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except RepositoryError:
            logger.exception("Failed to create todo.")
            return Response(
                {"error": "Todo storage is temporarily unavailable."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
