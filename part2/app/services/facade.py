from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    # --- New Methods to Add ---

    def get_all_users(self):
        """Returns all user objects from the repository"""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Updates user data. Returns the updated user or None if not found"""
        user = self.get_user(user_id)
        if not user:
            return None

        # Update user attributes
        if 'firstName' in user_data:
            user.firstName = user_data['firstName']
        if 'lastName' in user_data:
            user.lastName = user_data['lastName']
        if 'email' in user_data:
            user.email = user_data['email']

        self.user_repo.update(user.id, user_data)
        return user

    #-----amenity
    def create_amenity(self, amenity_data):
        """Creates a new amenity and adds it to the repository"""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieves an amenity by its unique ID"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Returns all amenities currently in the repository"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Updates an amenity's attributes and persists changes"""
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None

        # Update logic
        if 'name' in amenity_data:
            amenity.name = amenity_data['name']

        self.amenity_repo.update(amenity.id, amenity_data)
        return amenity

    #-------place
    def create_place(self, place_data):
        """Creates a place after validating owner and amenities exist"""
        # Validate Owner
        owner = self.get_user(place_data.get('owner_id'))
        if not owner:
            raise ValueError("Owner not found")

        # Validate Amenities (if provided)
        amenity_ids = place_data.pop('amenities', [])
        validated_amenities = []
        for amenity_id in amenity_ids:
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity {amenity_id} not found")
            validated_amenities.append(amenity)

        # Create Place instance (Validation for price/lat/long happens in model setters)
        place = Place(**place_data)
        place.owner = owner
        place.amenities = validated_amenities

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Retrieves a place by ID, including owner and amenity objects"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieves all places"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Updates place attributes"""
        place = self.get_place(place_id)
        if not place:
            return None

        # Update specific fields if they exist in the payload
        for key, value in place_data.items():
            if hasattr(place, key) and key not in ['id', 'created_at', 'updated_at', 'owner']:
                setattr(place, key, value)

        self.place_repo.update(place.id, place_data)
        return place

    #---------review

    def create_review(self, review_data):
        user = self.get_user(review_data.get('user_id'))
        place = self.get_place(review_data.get('place_id'))

        if not user or not place:
            raise ValueError("Invalid user_id or place_id")

        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return [r for r in self.review_repo.get_all() if r.place_id == place_id]

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None
        # Only update text and rating as per requirements
        if 'text' in review_data:
            review.text = review_data['text']
        if 'rating' in review_data:
            review.rating = review_data['rating']
        self.review_repo.update(review.id, review_data)
        return review

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)