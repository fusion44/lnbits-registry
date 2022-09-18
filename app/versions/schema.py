from app.models import ORJSONModel

# PYDANTIC SCHEMAS


class ExtensionVersionBase(ORJSONModel):
    major: int
    minor: int
    patch: int
    note: str = ""


class ExtensionVersionInput(ExtensionVersionBase):
    pass


class ExtensionVersionUpdateInput(ExtensionVersionBase):
    # SEMVER versions are immutable
    note: str


class ExtensionVersion(ExtensionVersionBase):
    id: int
    extension_id: int

    class Config:
        orm_mode = True
