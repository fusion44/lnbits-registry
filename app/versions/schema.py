from app.models import ORJSONModel
from fastapi import Query

# PYDANTIC SCHEMAS


class ExtensionVersionBase(ORJSONModel):
    major: int
    minor: int
    patch: int
    note: str = ""
    status: int = Query(
        0,
        description="""
        0: `draft` - For testing, not yet released, only visible to extension admins.
        1: `private` - Released, but for visible testers only.
        2: `public` - For public consumption.
        3: `deprecated` - No longer recommended for use.
        4: `withdrawn` - No longer available for use. Use a different version.
        """,
    )


class ExtensionVersionInput(ExtensionVersionBase):
    pass


class ExtensionVersionUpdateInput(ExtensionVersionBase):
    # SEMVER versions are immutable
    note: str


class ExtensionVersion(ExtensionVersionBase):
    # !! Inherits other fields from ExtensionVersionBase !!
    semver: str
    id: int
    extension_id: int
    is_latest: bool
    file_id: str = Query(
        None,
        alias="If this version has a file attached to it. A version must have an source file to publish it officially.",
    )

    class Config:
        orm_mode = True


class VersionFile(ORJSONModel):
    id: str = Query(description="UUID of the extension")
    file_name: str = Query(description="Original filename")
    version_id: int = Query(description="ID of the version this file belongs to")

    class Config:
        orm_mode = True
