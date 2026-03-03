#!/usr/bin/python3
"""Black-box tests for HBnB Part 2 API endpoints."""

import unittest

from app import create_app
from app.services import facade


class TestApiBlackBox(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # Reset in-memory repositories to keep tests isolated and deterministic.
        facade.user_repo._storage.clear()
        facade.amenity_repo._storage.clear()
        facade.place_repo._storage.clear()
        facade.review_repo._storage.clear()

    def _create_user(self, email="john.doe@example.com"):
        response = self.client.post(
            "/api/v1/users/",
            json={
                "first_name": "John",
                "last_name": "Doe",
                "email": email,
            },
        )
        self.assertEqual(response.status_code, 201)
        return response.get_json()

    def _create_amenity(self, name="Wi-Fi"):
        response = self.client.post("/api/v1/amenities/", json={"name": name})
        self.assertEqual(response.status_code, 201)
        return response.get_json()

    def _create_place(self, owner_id, amenities=None):
        payload = {
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": owner_id,
            "amenities": amenities or [],
        }
        response = self.client.post("/api/v1/places/", json=payload)
        self.assertEqual(response.status_code, 201)
        return response.get_json()

    def _create_review(self, user_id, place_id, text="Great place!", rating=5):
        response = self.client.post(
            "/api/v1/reviews/",
            json={
                "text": text,
                "rating": rating,
                "user_id": user_id,
                "place_id": place_id,
            },
        )
        self.assertEqual(response.status_code, 201)
        return response.get_json()

    def test_user_create_and_get(self):
        created = self._create_user()
        response = self.client.get(f"/api/v1/users/{created['id']}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["email"], "john.doe@example.com")

    def test_user_invalid_input_returns_400(self):
        response = self.client.post(
            "/api/v1/users/",
            json={
                "first_name": "",
                "last_name": "Doe",
                "email": "invalid-email",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_user_update_unknown_id_returns_404(self):
        response = self.client.put(
            "/api/v1/users/does-not-exist",
            json={"email": "new.email@example.com"},
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["error"], "User not found")

    def test_amenity_invalid_name_returns_400(self):
        response = self.client.post("/api/v1/amenities/", json={"name": ""})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_place_create_and_update(self):
        owner = self._create_user("owner@example.com")
        amenity = self._create_amenity("Pool")
        place = self._create_place(owner["id"], amenities=[amenity["id"]])

        self.assertEqual(place["owner_id"], owner["id"])
        self.assertEqual(len(place["amenities"]), 1)

        old_updated_at = place["updated_at"]
        response = self.client.put(
            f"/api/v1/places/{place['id']}",
            json={"title": "Luxury Condo", "price": 200.0},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["title"], "Luxury Condo")
        self.assertEqual(payload["price"], 200.0)
        self.assertNotEqual(payload["updated_at"], old_updated_at)

    def test_place_update_unknown_id_returns_404(self):
        response = self.client.put("/api/v1/places/not-found", json={"title": "X"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["error"], "Place not found")

    def test_place_create_with_invalid_owner_returns_400(self):
        response = self.client.post(
            "/api/v1/places/",
            json={
                "title": "Invalid place",
                "description": "No owner",
                "price": 90,
                "latitude": 0,
                "longitude": 0,
                "owner_id": "missing-user",
                "amenities": [],
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"], "Owner not found")

    def test_review_crud_and_reviews_by_place(self):
        user = self._create_user("reviewer@example.com")
        place = self._create_place(user["id"])
        review = self._create_review(user["id"], place["id"])

        get_one = self.client.get(f"/api/v1/reviews/{review['id']}")
        self.assertEqual(get_one.status_code, 200)
        self.assertEqual(get_one.get_json()["text"], "Great place!")

        by_place = self.client.get(f"/api/v1/places/{place['id']}/reviews")
        self.assertEqual(by_place.status_code, 200)
        self.assertEqual(len(by_place.get_json()), 1)

        updated = self.client.put(
            f"/api/v1/reviews/{review['id']}",
            json={"text": "Amazing stay!", "rating": 4},
        )
        self.assertEqual(updated.status_code, 200)
        self.assertEqual(updated.get_json()["text"], "Amazing stay!")
        self.assertEqual(updated.get_json()["rating"], 4)

        deleted = self.client.delete(f"/api/v1/reviews/{review['id']}")
        self.assertEqual(deleted.status_code, 200)

        get_after_delete = self.client.get(f"/api/v1/reviews/{review['id']}")
        self.assertEqual(get_after_delete.status_code, 404)

    def test_review_invalid_rating_returns_400(self):
        user = self._create_user("rating@example.com")
        place = self._create_place(user["id"])
        response = self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "Bad rating",
                "rating": 6,
                "user_id": user["id"],
                "place_id": place["id"],
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_reviews_by_place_unknown_place_returns_404(self):
        response = self.client.get("/api/v1/places/missing-place/reviews")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["error"], "Place not found")


if __name__ == "__main__":
    unittest.main()
