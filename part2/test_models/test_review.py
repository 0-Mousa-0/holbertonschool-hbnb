#!/usr/bin/python3
"""Independent tests for the Review class."""

import time
import unittest

from app.models.base_model import BaseModel
from app.models.place import Place
from app.models.review import Review
from app.models.user import User


class TestReview(unittest.TestCase):
    def setUp(self):
        self.user = User("John", "Doe", "reviewer@example.com")
        self.place = Place(
            title="Flat",
            description="Nice view",
            price=80,
            latitude=45.0,
            longitude=9.0,
            owner=self.user,
        )

    def test_review_inherits_base_model(self):
        review = Review("Amazing stay", 5, self.place, self.user)
        self.assertIsInstance(review, BaseModel)
        self.assertIsInstance(review.id, str)
        self.assertIsNotNone(review.created_at)
        self.assertIsNotNone(review.updated_at)

    def test_review_creation(self):
        review = Review("Amazing stay", 5, self.place, self.user)
        self.assertEqual(review.text, "Amazing stay")
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.user_id, self.user.id)
        self.assertEqual(review.place_id, self.place.id)

    def test_review_invalid_rating(self):
        with self.assertRaises(ValueError):
            Review("Bad rating", 0, self.place, self.user)
        with self.assertRaises(ValueError):
            Review("Bad rating", 6, self.place, self.user)

    def test_review_invalid_text(self):
        with self.assertRaises(ValueError):
            Review("", 4, self.place, self.user)

    def test_review_update(self):
        review = Review("Good", 4, self.place, self.user)
        old_updated_at = review.updated_at
        time.sleep(0.001)
        review.update({"text": "Excellent", "rating": 5})
        self.assertEqual(review.text, "Excellent")
        self.assertEqual(review.rating, 5)
        self.assertGreater(review.updated_at, old_updated_at)


if __name__ == "__main__":
    unittest.main()
