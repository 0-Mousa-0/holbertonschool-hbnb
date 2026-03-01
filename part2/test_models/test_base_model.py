#!/usr/bin/python3
"""Independent tests for BaseModel behavior."""

import time
import unittest

from app.models.base_model import BaseModel


class DummyModel(BaseModel):
    def __init__(self, name="demo", **kwargs):
        super().__init__(**kwargs)
        self.name = name


class TestBaseModel(unittest.TestCase):
    def test_default_fields_exist(self):
        obj = DummyModel()
        self.assertIsInstance(obj.id, str)
        self.assertIsNotNone(obj.created_at)
        self.assertIsNotNone(obj.updated_at)

    def test_save_updates_updated_at(self):
        obj = DummyModel()
        old_updated_at = obj.updated_at
        time.sleep(0.001)
        obj.save()
        self.assertGreater(obj.updated_at, old_updated_at)

    def test_update_updates_existing_attributes(self):
        obj = DummyModel(name="old")
        old_updated_at = obj.updated_at
        time.sleep(0.001)
        obj.update({"name": "new"})
        self.assertEqual(obj.name, "new")
        self.assertGreater(obj.updated_at, old_updated_at)


if __name__ == "__main__":
    unittest.main()
