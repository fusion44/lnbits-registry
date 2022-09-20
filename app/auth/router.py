import uuid
from app.schemas import UserProfile
from app.users import current_active_user
from app.db import User, get_async_session
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, Query

custom_auth_router = APIRouter()


@custom_auth_router.get(
    "/profile/{user_id}",
    response_model=UserProfile,
    description="Get the public user profile",
)
async def get_profile(
    user_id: uuid.UUID = Query(description="UUID of the user"),
    _: User = Depends(current_active_user),
    db: Session = Depends(get_async_session),
) -> UserProfile:
    db_ext = await db.get(User, user_id)

    return UserProfile(
        id=db_ext.id,
        is_active=db_ext.is_active,
        display_name=db_ext.display_name,
    )
