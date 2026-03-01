#!/usr/bin/python3
"""Place entity implementation."""

from app.models.base_model import BaseModel
from app.models.user import User


class Place(BaseModel):
    """Represents a listing owned by a user."""

    def __init__(
        self,
        title,
        price,
        latitude,
        longitude,
        owner,
        description="",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._title = ""
        self._description = ""
        self._price = 0.0
        self._latitude = 0.0
        self._longitude = 0.0
        self._owner = None

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

        # Relationships are lists in Part 2 in-memory mode.
        self.reviews = []
        self.amenities = []

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("title must be a non-empty string")
        if len(value.strip()) > 100:
            raise ValueError("title must be at most 100 characters")
        self._title = value.strip()
        self.save()

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if value is None:
            self._description = ""
        elif not isinstance(value, str):
            raise ValueError("description must be a string")
        else:
            self._description = value.strip()
        self.save()

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("price must be a number")
        if float(value) < 0:
            raise ValueError("price must be non-negative")
        self._price = float(value)
        self.save()

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("latitude must be a number")
        latitude = float(value)
        if latitude < -90 or latitude > 90:
            raise ValueError("latitude must be between -90 and 90")
        self._latitude = latitude
        self.save()

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("longitude must be a number")
        longitude = float(value)
        if longitude < -180 or longitude > 180:
            raise ValueError("longitude must be between -180 and 180")
        self._longitude = longitude
        self.save()

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):
        if not isinstance(value, User):
            raise ValueError("owner must be a User instance")
        self._owner = value
        self.save()

    @property
    def owner_id(self):
        return self.owner.id

    def add_review(self, review):
        # Local import avoids a module cycle between place and review.
        from app.models.review import Review

        if not isinstance(review, Review):
            raise ValueError("review must be a Review instance")
        if review not in self.reviews:
            self.reviews.append(review)
            self.save()

    def add_amenity(self, amenity):
        from app.models.amenity import Amenity

        if not isinstance(amenity, Amenity):
            raise ValueError("amenity must be an Amenity instance")
        if amenity not in self.amenities:
            self.amenities.append(amenity)
            self.save()

    def update(self, data):
        """Restrict updates to editable place fields only."""
        mutable_fields = {"title", "description", "price", "latitude", "longitude"}
        super().update({key: value for key, value in data.items() if key in mutable_fields})
