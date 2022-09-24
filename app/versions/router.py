from sqlalchemy.orm import Session
from fastapi import APIRouter, Body, Depends, Query, File, UploadFile
from fastapi.responses import FileResponse
from app.users import current_active_user
from app.db import User, get_async_session
import app.versions.schema as s
import app.versions.service as service

router = APIRouter()


@router.post(
    "/add/{extension_id}",
    response_model=s.ExtensionVersion,
    responses={
        409: {"description": "Version number already exists for this extension"}
    },
    summary="Add a new version to an extension",
)
async def add_extension_version(
    extension_id: int,
    input: s.ExtensionVersionInput,
    user: User = Depends(current_active_user),
    db: Session = Depends(get_async_session),
):
    return await service.add_version(extension_id, db, input, user)


@router.delete("/delete/{version_id}", response_model=s.ExtensionVersion)
async def delete_extension_version(
    version_id: int = Query(description="ID of the extension"),
    user: User = Depends(current_active_user),
    db: Session = Depends(get_async_session),
    description="Delete an extension",
):
    return s.Extension()


@router.patch(
    "/update/{version_id}",
    response_model=s.ExtensionVersion,
    summary="Update a version.",
    description="Only the extension owner can do this. Only non-null fields will be updated.",
)
async def update_extension_version(
    version_id: int = Query(description="ID of the version"),
    db: Session = Depends(get_async_session),
    i: s.ExtensionVersionUpdateInput = Body(),
    user: User = Depends(current_active_user),
):
    return await service.update_version(version_id, db, i, user)


@router.get(
    "/download/{version_id}",
    summary="Download a extension zip file for the given version",
)
async def download_extension_version_file(
    version_id: int = Query(description="ID of the version this file belongs to"),
    db: Session = Depends(get_async_session),
) -> FileResponse:
    return await service.download_version_file(version_id, db)


@router.post(
    "/upload/{version_id}",
    response_model=s.VersionFile,
    summary="Upload a extension zip file for a version.",
)
async def upload_extension_version_file(
    version_id: int = Query(description="ID of the version this file belongs to"),
    db: Session = Depends(get_async_session),
    user: User = Depends(current_active_user),
    file: UploadFile = File(...),
):
    return await service.upload_version_file(version_id, db, user, file)


@router.get(
    "/list/{extension_id}",
    response_model=list[s.ExtensionVersion],
    summary="List all versions for an extension",
)
async def list_extensions(
    extension_id: int = Query(description="ID of the extension"),
    db: Session = Depends(get_async_session),
    skip: int = 0,
    limit: int = 100,
):
    return await service.list_versions(extension_id, db, skip, limit)
