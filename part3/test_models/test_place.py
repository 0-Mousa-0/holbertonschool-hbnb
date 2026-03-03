#!/usr/bin/python3
"""Independent tests for the Place class and relationships."""

import time
import unittest

from app.models.amenity import Amenity
from app.models.base_model import BaseModel
from app.models.place import Place
from app.models.review import Review
from app.models.user import User


class TestPlace(unittest.TestCase):
    def setUp(self):
        self.owner = User("Alice", "Smith", "alice@example.com")
        self.place = Place(
            title="Cozy Apartment",
            description="A nice place to stay",
            price=100,
            latitude=37.7749,
            longitude=-122.4194,
            owner=self.owner,
        )

    def test_place_inherits_base_model(self):
        self.assertIsInstance(self.place, BaseModel)
        self.assertIsInstance(self.place.id, str)
        self.assertIsNotNone(self.place.created_at)
        self.assertIsNotNone(self.place.updated_at)

    def test_place_creation_valid_data(self):
        self.assertEqual(self.place.title, "Cozy Apartment")
        self.assertEqual(self.place.price, 100.0)
        self.assertEqual(self.place.owner.id, self.owner.id)

    def test_place_invalid_price(self):
        with self.assertRaises(ValueError):
            self.place.price = -10

    def test_place_invalid_coordinates(self):
        with self.assertRaises(ValueError):
            self.place.latitude = 100
        with self.assertRaises(ValueError):
            self.place.longitude = -200

    def test_place_relationships_reviews_and_amenities(self):
        review = Review("Great stay!", 5, self.place, self.owner)
        amenity = Amenity("Wi-Fi")

        self.place.add_review(review)
        self.place.add_amenity(amenity)

        self.assertEqual(len(self.place.reviews), 1)
        self.assertEqual(len(self.place.amenities), 1)
        self.assertEqual(self.place.reviews[0].text, "Great stay!")
        self.assertEqual(self.place.amenities[0].name, "Wi-Fi")

    def test_update_updates_timestamp(self):
        old_updated_at = self.place.updated_at
        time.sleep(0.001)
        self.place.update({"title": "Luxury Condo", "price": 200})
        self.assertEqual(self.place.title, "Luxury Condo")
        self.assertEqual(self.place.price, 200.0)
        self.assertGreater(self.place.updated_at, old_updated_at)


if __name__ == "__main__":
    unittest.main()
