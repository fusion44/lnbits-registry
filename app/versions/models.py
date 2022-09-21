from typing import Any
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.db import Base


# DATABASE MODELS


class ExtensionVersion(Base):
    __tablename__ = "extension_version"

    id = Column(Integer, primary_key=True, index=True)
    major = Column(Integer)
    minor = Column(Integer)
    patch = Column(Integer)
    note = Column(String, default=None)
    semver = Column(String, unique=True)
    status: int = Column(Integer, default=0)
    is_latest = Column(Boolean, default=False)
    extension_id = Column(Integer, ForeignKey("extension.id"))
    file_id = Column(String, ForeignKey("version_file.id"), default=None)

    def __init__(self, major, minor, patch, note, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.major = major
        self.minor = minor
        self.patch = patch
        self.note = note


class VersionFile(Base):
    __tablename__ = "version_file"

    id = Column(String, primary_key=True)
    file_name = Column(String)
    version_id = Column(Integer, ForeignKey("extension_version.id"))

    def __init__(self, id, file_name, version_id, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.id = id
        self.file_name = file_name
        self.version_id = version_id
