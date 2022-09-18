from typing import Any
from uuid import UUID
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base


# DATABASE MODELS


class Extension(Base):
    __tablename__ = "extension"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), unique=True)
    description_short = Column(String(140))
    description_long = Column(String, default=None)
    owner = Column(String(36), ForeignKey("user.id"))
    versions = relationship("ExtensionVersion", lazy="joined")

    def __init__(
        self, description_short, description_long, owner, *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.description_short = description_short
        self.description_long = description_long
        self.owner = owner


class ExtensionVersion(Base):
    __tablename__ = "extension_version"

    id = Column(Integer, primary_key=True, index=True)
    major = Column(Integer)
    minor = Column(Integer)
    patch = Column(Integer)
    note = Column(String, default=None)
    parent_id = Column(Integer, ForeignKey("extension.id"))

    def __init__(self, major, minor, patch, note, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.major = major
        self.minor = minor
        self.patch = patch
        self.note = note
