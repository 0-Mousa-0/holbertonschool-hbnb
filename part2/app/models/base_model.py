#!/usr/bin/python3
"""Shared base model with UUID and timestamp behavior."""

from datetime import datetime
import uuid


class BaseModel:
    """Common behavior shared by all business entities."""

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", str(uuid.uuid4()))
        self.created_at = kwargs.get("created_at", datetime.now())
        self.updated_at = kwargs.get("updated_at", datetime.now())

    def save(self):
        """Refresh the update timestamp after a state change."""
        self.updated_at = datetime.now()

    def update(self, data):
        """
        Update existing attributes from a dictionary.

        Immutable base attributes are intentionally ignored.
        """
        protected = {"id", "created_at", "updated_at"}
        for key, value in data.items():
            if key in protected:
                continue
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
