import uuid
from datetime import datetime
from user import User

class Place:
    """Represents a Place in HBnB project."""

    def __init__(self, title, price, latitude, longitude, owner, description=None):
        self.id = str(uuid.uuid4())
        self._title = None
        self.title = title

        self.description = description

        self._price = None
        self.price = price

        self._latitude = None
        self.latitude = latitude

        self._longitude = None
        self.longitude = longitude

        if not isinstance(owner, User):
            raise ValueError("owner must be a User instance")
        self.owner = owner

        self.reviews = []
        self.amenities = []

        # Must match project naming
        self.createDate = datetime.now()
        self.updateDate = datetime.now()

    # -------------------
    # Title property
    # -------------------
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value:
            raise ValueError("Title cannot be empty")
        if len(value) > 100:
            raise ValueError("Title cannot exceed 100 characters")
        self._title = value
        self.updateDate = datetime.now()

    # -------------------
    # Price property
    # -------------------
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a non-negative number")
        self._price = float(value)
        self.updateDate = datetime.now()

    # -------------------
    # Latitude property
    # -------------------
    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)) or not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = float(value)
        self.updateDate = datetime.now()

    # -------------------
    # Longitude property
    # -------------------
    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)) or not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = float(value)
        self.updateDate = datetime.now()

    # -------------------
    # Reviews & Amenities
    # -------------------
    def add_review(self, review):
        self.reviews.append(review)
        self.updateDate = datetime.now()

    def add_amenity(self, amenity):
        self.amenities.append(amenity)
        self.updateDate = datetime.now()