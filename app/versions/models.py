from typing import Any
from uuid import UUID
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base


# DATABASE MODELS


class ExtensionVersion(Base):
    __tablename__ = "extension_version"

    id = Column(Integer, primary_key=True, index=True)
    major = Column(Integer)
    minor = Column(Integer)
    patch = Column(Integer)
    note = Column(String, default=None)
    extension_id = Column(Integer, ForeignKey("extension.id"))

    def __init__(self, major, minor, patch, note, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.major = major
        self.minor = minor
        self.patch = patch
        self.note = note
