"""Unit tests for todo service validation and repository delegation."""

import unittest

from .exceptions import TodoValidationError
from .services import TodoService


class FakeTodoRepository:
    """In-memory repository for service unit tests."""

    def __init__(self):
        self.todos = []

    def list_all(self):
        return list(self.todos)

    def create(self, description):
        todo = {"id": str(len(self.todos) + 1), "description": description}
        self.todos.append(todo)
        return todo


class TodoServiceTests(unittest.TestCase):
    def setUp(self):
        self.repository = FakeTodoRepository()
        self.service = TodoService(self.repository)

    def test_create_todo_trims_and_persists_description(self):
        todo = self.service.create_todo({"description": "  Buy milk  "})

        self.assertEqual(todo["description"], "Buy milk")
        self.assertEqual(self.repository.todos, [todo])

    def test_list_todos_returns_repository_items(self):
        expected = self.repository.create("Buy milk")

        self.assertEqual(self.service.list_todos(), [expected])

    def test_create_todo_rejects_empty_description(self):
        with self.assertRaisesRegex(TodoValidationError, "cannot be empty"):
            self.service.create_todo({"description": ""})

    def test_create_todo_rejects_whitespace_only_description(self):
        with self.assertRaisesRegex(TodoValidationError, "cannot be empty"):
            self.service.create_todo({"description": "   \t"})

    def test_create_todo_rejects_description_over_200_characters(self):
        with self.assertRaisesRegex(TodoValidationError, "200 characters"):
            self.service.create_todo({"description": "a" * 201})

    def test_create_todo_rejects_non_string_description(self):
        with self.assertRaisesRegex(TodoValidationError, "must be a string"):
            self.service.create_todo({"description": 123})

    def test_create_todo_rejects_non_object_payload(self):
        with self.assertRaisesRegex(TodoValidationError, "JSON object"):
            self.service.create_todo(["Buy milk"])
