from sqlalchemy.orm import Session
from fastapi import APIRouter, Body, Depends, Query
from app.users import current_active_user
from app.db import User, get_async_session
import app.extensions.schema as s
import app.extensions.service as service

router = APIRouter()


@router.post("/add", response_model=s.Extension)
async def add_extension(
    i: s.ExtensionInput,
    user: User = Depends(current_active_user),
    db: Session = Depends(get_async_session),
):
    return await service.add_extension(db, i, user)


@router.post("/delete/{extension_id}", response_model=s.Extension)
async def delete_extension(
    extension_id: int = Query(description="ID of the extension"),
    id: int = Body(description="ID of the extension"),
    user: User = Depends(current_active_user),
):
    return s.Extension()


@router.post(
    "/update/{extension_id}",
    response_model=s.Extension,
    description="Update an extension. Only the owner can do this. Only non-null fields will be updated.",
)
async def update_extension(
    extension_id: int = Query(description="ID of the extension"),
    db: Session = Depends(get_async_session),
    i: s.ExtensionUpdateInput = Body(),
    user: User = Depends(current_active_user),
):
    return await service.update_extension(extension_id, db, i, user)


@router.get("/list", response_model=list[s.Extension])
async def list_extensions(
    db: Session = Depends(get_async_session),
    skip: int = 0,
    limit: int = 100,
):
    return await service.list_all_extensions(db, skip, limit)
