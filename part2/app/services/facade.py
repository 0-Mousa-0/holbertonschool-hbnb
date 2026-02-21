#!/usr/bin/python3
from app.persistence.repository import InMemoryRepository
from app.models.review import Review
from datetime import datetime


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()  # Assuming you have a repo for reviews
        self.amenity_repo = InMemoryRepository()

    # Placeholder method for creating a user
    def create_user(self, user_data):
        # Logic will be implemented in later tasks
        pass

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass

    def get_all_users(self):
        """ Retrieve a list of all users """
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """ Updates user data using your User class """
        user = self.get_user(user_id)
        if not user:
            return None

        # Using the profileUpdate method from your class
        # We use .get() to avoid errors if the user doesn't send all fields
        user.profileUpdate(
            firstName=user_data.get('firstName'),
            lastName=user_data.get('lastName'),
            email=user_data.get('email')
        )

        self.user_repo.update(user.id, user)
        return user

<<<<<<< HEAD
    def create_review(self, review_data):
        """Logic to create a review with validation for user, place, and rating"""
        user = self.get_user(review_data['user_id'])
        # Ensure you have get_place implemented
        place = self.get_place(review_data['place_id'])

        if not user or not place:
            raise ValueError("User or Place not found")

        # Create instance using your Review class constructor
        # Note: Your model uses 'comment', the API uses 'text'. We map them here.
        new_review = Review(
            comment=review_data['text'],
            rating=review_data['rating'],
            place=place,
            user=user
        )
        self.review_repo.add(new_review)
        return new_review

    def get_review(self, review_id):
        """Retrieve a review by ID"""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieve all reviews"""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Retrieve all reviews for a specific place"""
        all_reviews = self.review_repo.get_all()
        return [r for r in all_reviews if r.place.id == place_id]

    def update_review(self, review_id, review_data):
        """Update a review using the update method in your model"""
        review = self.get_review(review_id)
        if not review:
            return None

        # Mapping API 'text' to your model 'comment'
        if 'text' in review_data:
            review_data['comment'] = review_data.pop('text')

        review.update(review_data)
        review.updateDate = datetime.now()  # From your requirements
        self.review_repo.update(review_id, review)
        return review

    def delete_review(self, review_id):
        """Delete a review from storage"""
        return self.review_repo.delete(review_id)
=======
    def create_amenity(self, amenity_data):
        # Placeholder for logic to create an amenity
        pass

    def get_amenity(self, amenity_id):
        # Placeholder for logic to retrieve an amenity by ID
        pass

    def get_all_amenities(self):
        # Placeholder for logic to retrieve all amenities
        pass

    def update_amenity(self, amenity_id, amenity_data):
        # Placeholder for logic to update an amenity
        pass
>>>>>>> 0ffd783 (final fixes before sync)
