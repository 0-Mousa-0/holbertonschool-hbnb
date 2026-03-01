#!/usr/bin/python3
"""Independent tests for the User class."""

import time
import unittest

from app.models.base_model import BaseModel
from app.models.user import User


class TestUser(unittest.TestCase):
    def test_user_inherits_base_model(self):
        user = User(first_name="John", last_name="Doe", email="john1@example.com")
        self.assertIsInstance(user, BaseModel)
        self.assertIsInstance(user.id, str)
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)

    def test_user_creation_valid_data(self):
        user = User(first_name="John", last_name="Doe", email="john2@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john2@example.com")
        self.assertFalse(user.is_admin)

    def test_user_invalid_first_name(self):
        with self.assertRaises(ValueError):
            User(first_name="", last_name="Doe", email="john3@example.com")

    def test_user_invalid_email(self):
        with self.assertRaises(ValueError):
            User(first_name="John", last_name="Doe", email="invalid-email")

    def test_save_updates_timestamp(self):
        user = User(first_name="John", last_name="Doe", email="john4@example.com")
        old_updated_at = user.updated_at
        time.sleep(0.001)
        user.save()
        self.assertGreater(user.updated_at, old_updated_at)

    def test_update_method_changes_fields_and_timestamp(self):
        user = User(first_name="John", last_name="Doe", email="john5@example.com")
        old_updated_at = user.updated_at
        time.sleep(0.001)
        user.update({"first_name": "Jane", "last_name": "Smith"})
        self.assertEqual(user.first_name, "Jane")
        self.assertEqual(user.last_name, "Smith")
        self.assertGreater(user.updated_at, old_updated_at)


if __name__ == "__main__":
    unittest.main()
