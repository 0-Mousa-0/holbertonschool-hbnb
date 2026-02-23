#!/usr/bin/python3
from app.persistence.repository import InMemoryRepository
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    """Facade for HBnB operations"""

    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # ======================= USERS =============================
    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def create_user(self, user):
        self.user_repo.add(user)
        return user

    def update_user(self, user_id, data):
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")

        for key, value in data.items():
            setattr(user, key, value)

        self.user_repo.update(user_id, user)
        return user

    # ===================== AMENITIES ==========================
    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def create_amenity(self, amenity):
        self.amenity_repo.add(amenity)
        return amenity

    def update_amenity(self, amenity_id, data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")
        if "name" in data:
            amenity.name = data["name"]
        self.amenity_repo.update(amenity_id, amenity)
        return amenity

    # ======================= PLACES ===========================
    def create_place(self, place_data):
        owner = self.get_user(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")

        amenities = []
        for aid in place_data.get("amenities", []):
            amenity = self.get_amenity(aid)
            if not amenity:
                raise ValueError(f"Amenity {aid} not found")
            amenities.append(amenity)

        place = Place(
            title=place_data['title'],
            description=place_data.get('description'),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner
        )

        for amenity in amenities:
            place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")

        for key in ['title', 'description', 'price', 'latitude', 'longitude']:
            if key in place_data:
                setattr(place, key, place_data[key])

        if 'owner_id' in place_data:
            owner = self.get_user(place_data['owner_id'])
            if not owner:
                raise ValueError("Owner not found")
            place.owner = owner

        if 'amenities' in place_data:
            amenities = []
            for aid in place_data['amenities']:
                amenity = self.get_amenity(aid)
                if not amenity:
                    raise ValueError(f"Amenity {aid} not found")
                amenities.append(amenity)
            place.amenities = amenities

        self.place_repo.update(place_id, place)
        return place

    # ======================= REVIEWS ==========================
    def create_review(self, review_data):
        user = self.get_user(review_data['user_id'])
        if not user:
            raise ValueError("User not found")

        place = self.get_place(review_data['place_id'])
        if not place:
            raise ValueError("Place not found")

        review = Review(
    comment=review_data['text'],
    rating=review_data['rating'],
    user=user,
    place=place
)

        place.add_review(review)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def update_review(self, review_id, data):
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")

        if 'text' in data:
            review.comment = data['text']

        if 'rating' in data:
            review.rating = data['rating']

        self.review_repo.update(review_id, review)
        return review

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)