#!/usr/bin/python3
"""Independent tests for the Amenity class."""

import time
import unittest

from app.models.amenity import Amenity
from app.models.base_model import BaseModel


class TestAmenity(unittest.TestCase):
    def test_amenity_inherits_base_model(self):
        amenity = Amenity(name="Wi-Fi")
        self.assertIsInstance(amenity, BaseModel)
        self.assertIsInstance(amenity.id, str)
        self.assertIsNotNone(amenity.created_at)
        self.assertIsNotNone(amenity.updated_at)

    def test_amenity_creation(self):
        amenity = Amenity(name="Parking")
        self.assertEqual(amenity.name, "Parking")

    def test_invalid_amenity_name(self):
        with self.assertRaises(ValueError):
            Amenity(name="")

    def test_update_method(self):
        amenity = Amenity(name="Pool")
        old_updated_at = amenity.updated_at
        time.sleep(0.001)
        amenity.update({"name": "Gym"})
        self.assertEqual(amenity.name, "Gym")
        self.assertGreater(amenity.updated_at, old_updated_at)


if __name__ == "__main__":
    unittest.main()
