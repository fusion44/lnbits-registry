from fastapi import Query
from app.models import ORJSONModel

# PYDANTIC SCHEMAS


class ExtensionBase(ORJSONModel):
    name: str = Query(description="Short name of the extension")
    description_short: str = Query(
        "",
        description="A short description what the extension is about. Max characters: 140",
    )
    description_long: str = Query(
        "", description="An elaborate description what the extension does"
    )


class ExtensionInput(ExtensionBase):
    pass


class ExtensionUpdateInput(ORJSONModel):
    id: int = Query(description="UUID of the extension")
    name: str = Query(None, description="Short name of the extension")
    description_short: str = Query(
        None,
        description="A short description what the extension is about. Max characters: 140",
    )
    description_long: str = Query(
        None, description="An elaborate description what the extension does"
    )


class ExtensionVersion(ORJSONModel):
    id: int
    major: int
    minor: int
    patch: int
    note: str = ""

    class Config:
        orm_mode = True


class Extension(ExtensionBase):
    id: int = Query(None, description="UUID of the extension")
    owner: str = Query(description="UUID of the extension owner")
    versions: list[ExtensionVersion] = []

    class Config:
        orm_mode = True
