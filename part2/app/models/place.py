from user import User
import uuid
from datetime import datetime

class Place:
    def __init__(self, title, price, latitude, longitude, owner, description=None):
        self.id = str(uuid.uuid4())
        
        # Use setters to validate
        self._title = None
        self.title = title
        
        self.description = description
        
        self._price = None
        self.price = price
        
        self._latitude = None
        self.latitude = latitude
        
        self._longitude = None
        self.longitude = longitude
        
        # Validate owner is User instance
        if not isinstance(owner, User):
            raise ValueError("owner must be a User instance")
        
        self.owner = owner
        
        self.reviews = []     # List to store related reviews
        self.amenities = []   # List to store related amenities
        
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    # User.id != owner
    # ------------------------
    # Title property
    # ------------------------
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        """validate"""
        if not value:
            raise ValueError("Title cannot be empty")
        if len(value) > 100:
            raise ValueError("Title cannot exceed 100 characters")
        self._title = value
        self.updated_at = datetime.utcnow()
    
    # ------------------------
    # Price property
    # ------------------------
    @property
    def price(self):
        """get"""
        return self._price

    @price.setter
    def price(self, value):
        """validate"""
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a positive number")
        self._price = float(value)
        self.updated_at = datetime.utcnow()
    
    # ------------------------
    # Latitude property
    # ------------------------
    @property
    def latitude(self):
        """validate"""
        return self._latitude
    
    @latitude.setter
    def latitude(self, value):
        """validate"""
        if not isinstance(value, (int, float)) or not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = float(value)
        self.updated_at = datetime.utcnow()
    
    # ------------------------
    # Longitude property
    # ------------------------
    @property
    def longitude(self):
        """validate"""
        return self._longitude
    
    @longitude.setter
    def longitude(self, value):
        """check"""
        if not isinstance(value, (int, float)) or not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = float(value)
        self.updated_at = datetime.utcnow()
    
    # ------------------------
    # Reviews and Amenities
    # ------------------------
    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)
        self.updated_at = datetime.utcnow()
    
    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
        self.updated_at = datetime.utcnow()
