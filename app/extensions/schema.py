from fastapi import Query
from app.models import ORJSONModel
from app.versions.schema import ExtensionVersion

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
    prefix: str = Query(
        ...,
        description="""The extension prefix as defined in the extensions `__init__.py` file. Max characters: 40
        
        bleskomat_ext: APIRouter = APIRouter(prefix="*/bleskomat*", tags=["Bleskomat"])
        """,
        max_length=40,
        min_length=3,
    )


class ExtensionInput(ExtensionBase):
    pass


class ExtensionUpdateInput(ORJSONModel):
    name: str = Query(None, description="Short name of the extension")
    description_short: str = Query(
        None,
        description="A short description what the extension is about. Max characters: 140",
    )
    description_long: str = Query(
        None, description="An elaborate description what the extension does"
    )


class Extension(ExtensionBase):
    id: int = Query(None, description="UUID of the extension")
    owner: str = Query(description="UUID of the extension owner")
    versions: list[ExtensionVersion] = []

    class Config:
        orm_mode = True
