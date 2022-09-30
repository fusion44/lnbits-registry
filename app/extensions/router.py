from sqlalchemy.orm import Session
from fastapi import APIRouter, Body, Depends, Query, Path
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


@router.delete("/delete/{extension_id}", response_model=s.Extension)
async def delete_extension(
    extension_id: int = Query(description="ID of the extension"),
    id: int = Body(description="ID of the extension"),
    user: User = Depends(current_active_user),
):
    return s.Extension()


@router.patch(
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
    include_unversioned: bool = Query(
        False, description="Include extensions without any versions attached to them."
    ),
):
    return await service.list_all_extensions(db, skip, limit, include_unversioned)


@router.get("/get/by-name/{name}", response_model=s.Extension)
async def get_extension_by_name(
    name: str = Path(description="`name` of the extension"),
    db: Session = Depends(get_async_session),
):
    return await service.get_extension(name, db)


@router.get("/get/by-id/{id}", response_model=s.Extension)
async def get_extension_by_id(
    id: int = Path(description="`id` of the extension"),
    db: Session = Depends(get_async_session),
):
    return await service.get_extension(id, db)
