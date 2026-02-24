import uuid
from datetime import datetime
from app.models.user import User
from app.models.place import Place


class Review:
    """
    Represents a review entity in the HBnB application.
    This class handles review data, validation, and relationships 
    between Users and Places.
    """

    def __init__(self, comment, rating, place, user):
        """
        Initializes a new Review instance.

        Args:
            comment (str): The content of the review.
            rating (int): Rating between 1 and 5.
            place (Place): The Place object being reviewed.
            user (User): The User object who wrote the review.

        Raises:
            ValueError: If validation fails for comment, rating, or instances.
        """
        # Unique identifier for each review
        self.id = str(uuid.uuid4())
        # Timestamp for creation
        self.createDate = datetime.now()
        # Timestamp for last update
        self.updateDate = datetime.now()

        # Validation Logic
        if not comment:
            raise ValueError("Review comment is required")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        if not isinstance(place, Place):
            raise ValueError("Invalid place instance")
        if not isinstance(user, User):
            raise ValueError("Invalid user instance")

        # Assigning values after validation
        self.comment = comment
        self.rating = rating
        self.place = place
        self.user = user

    def create(self):
        """
        Saves the current review instance to the storage.
        """
        pass

    def update(self, data):
        """
        Updates the updateDate timestamp to the current time.
        """
        for key, value in data.items():
            if hasattr(self, key):
                if key == 'rating' and not (1 <= value <= 5):
                    raise ValueError("Rating must be between 1 and 5")
                setattr(self, key, value)

    def list(self):
        """
        Retrieves a list of all review instances.
        """
        pass
