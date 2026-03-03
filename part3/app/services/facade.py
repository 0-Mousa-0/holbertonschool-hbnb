from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    def create_user(self, user_data):
        # Enforce unique email at the facade level (repository-aware check).
        if self.get_user_by_email(user_data.get('email')):
            raise ValueError("Email already registered")
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

        new_email = user_data.get('email')
        if new_email and new_email != user.email:
            existing_user = self.get_user_by_email(new_email)
            if existing_user and existing_user.id != user.id:
                raise ValueError("Email already registered")

        user.update(user_data)
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

        amenity.update(amenity_data)
        return amenity

    #-------place
    def create_place(self, place_data):
        """Creates a place after validating owner and amenities exist"""
        owner_id = place_data.get('owner_id')
        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError("Owner not found")

        # Validate amenities IDs and map them to real Amenity objects.
        amenity_ids = place_data.get('amenities', [])
        if amenity_ids is None:
            amenity_ids = []
        if not isinstance(amenity_ids, list):
            raise ValueError("amenities must be a list of amenity IDs")

        validated_amenities = []
        for amenity_id in amenity_ids:
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity {amenity_id} not found")
            validated_amenities.append(amenity)

        place = Place(
            title=place_data.get('title'),
            description=place_data.get('description', ''),
            price=place_data.get('price'),
            latitude=place_data.get('latitude'),
            longitude=place_data.get('longitude'),
            owner=owner,
        )
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

        # owner and relationships are immutable in this update endpoint.
        blocked = {'id', 'created_at', 'updated_at', 'owner', 'owner_id', 'amenities', 'reviews'}
        payload = {k: v for k, v in place_data.items() if k not in blocked}
        place.update(payload)
        return place

    #---------review

    def create_review(self, review_data):
        user = self.get_user(review_data.get('user_id'))
        place = self.get_place(review_data.get('place_id'))

        if not user:
            raise ValueError("User not found")
        if not place:
            raise ValueError("Place not found")

        review = Review(
            text=review_data.get('text'),
            rating=review_data.get('rating'),
            place=place,
            user=user,
        )
        place.add_review(review)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return [review for review in self.review_repo.get_all() if review.place_id == place_id]

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None

        payload = {k: v for k, v in review_data.items() if k in {'text', 'rating'}}
        review.update(payload)
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            return False

        # Keep place.relationship list consistent after deletion.
        review.place.reviews = [item for item in review.place.reviews if item.id != review_id]
        return self.review_repo.delete(review_id)