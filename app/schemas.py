import uuid
from fastapi_users import schemas
from fastapi import Query
from app.models import ORJSONModel


class UserRead(schemas.BaseUser[uuid.UUID]):
    # hack to tell the client lib generators that this is a UUID
    # the generator treats the ID field as a generic object otherwise
    # If we ever change to an int ID, we must also to change this
    id: uuid.UUID = Query(description="UUID of the user")

    display_name: str = Query(
        min_length=3, max_length=32, description="Display name of the user"
    )


class UserCreate(schemas.BaseUserCreate):
    display_name: str = Query(
        min_length=3, max_length=32, description="Display name of the user"
    )


class UserUpdate(schemas.BaseUserUpdate):
    display_name: str = Query(
        min_length=3, max_length=32, description="Display name of the user"
    )


class UserProfile(ORJSONModel):
    id: uuid.UUID = Query(description="UUID of the user")
    is_active: bool = Query(description="Is the user active")
    display_name: str = Query(
        min_length=3, max_length=32, description="Display name of the user"
    )
