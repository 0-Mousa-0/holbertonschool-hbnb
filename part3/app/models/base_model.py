#!/usr/bin/python3
"""Shared base model with UUID and timestamp behavior."""
from app import db
from datetime import datetime
import uuid


class BaseModel(db.Model):
    """Common behavior shared by all business entities."""
    __abstract__ = True  # This ensures SQLAlchemy does not create a table for BaseModel

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    
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
