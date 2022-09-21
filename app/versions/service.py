import os
import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import app.versions.schema as schema
import app.extensions.models as ext_models
import app.versions.models as models
from app.db import User
from fastapi import UploadFile, HTTPException, status

# CRUD service for extension versions

CURR_CWD = os.getcwd()


async def add_version(
    ext_id: int, db: Session, input: schema.ExtensionVersionInput, user: User
) -> schema.ExtensionVersion:
    db_ext = await db.get(ext_models.Extension, ext_id)

    if db_ext.owner != str(user.id):
        raise Exception("You are not the owner of this extension!")

    semver = f"{input.major}.{input.minor}.{input.patch}"
    db_vs = models.ExtensionVersion(**input.dict(), semver=semver, extension_id=ext_id)
    try:
        db.add(db_vs)
        await db.commit()
        await db.refresh(db_vs)
        return db_vs
    except IntegrityError as e:
        db.rollback()
        if "UNIQUE constraint failed: extension_version.semver" in e.args[0]:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Version number {semver} already exists for this extension",
            )

        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unknown error while persisting version",
        )


async def list_versions(
    extension_id: int, db: Session, skip: int = 0, limit: int = 100
) -> list[schema.ExtensionVersion]:
    q = (
        select(models.ExtensionVersion)
        .where(models.ExtensionVersion.extension_id == extension_id)
        .offset(skip)
        .limit(limit)
    )
    res = await db.execute(q)
    b = res.unique().scalars().all()
    return b


async def delete_version(id: int) -> schema.ExtensionVersion:
    pass


async def update_version(
    id: int,
    db: Session,
    input: schema.ExtensionVersionUpdateInput,
    user: User,
) -> schema.ExtensionVersion:
    version = await db.get(models.ExtensionVersion, id)

    # get extension from the database and check if the user doesn't lie to us
    db_ext = await db.get(ext_models.Extension, version.extension_id)
    if db_ext.owner != str(user.id):
        raise Exception("You are not the owner of this extension!")

    # update the version
    setattr(version, "note", input.note)

    await db.commit()
    await db.refresh(version)
    return db_ext


async def upload_version_file(
    version_id: int,
    db: Session,
    user: User,
    file: UploadFile,
) -> models.VersionFile:
    version: models.ExtensionVersion = await db.get(models.ExtensionVersion, version_id)

    # get extension from the database and check if the user doesn't lie to us
    db_ext = await db.get(ext_models.Extension, version.extension_id)
    if db_ext.owner != str(user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to access this resource",
        )

    if version.file_id is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This version already has a file attached!",
        )

    file_id = str(uuid.uuid4())
    p = os.path.join(CURR_CWD, "data/files", f"{file_id}.zip")
    while os.path.exists(p):
        # Handle possible filename clashes (very unlikely but oh well)
        p = os.path.join(CURR_CWD, "data/files", f"{file_id}.zip")

    try:
        with open(p, "xb") as f:
            while contents := file.file.read(1024 * 1024):
                f.write(contents)
    except OSError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unknown error while writing file to disk",
        )
    finally:
        file.file.close()

    db_file = models.VersionFile(
        id=file_id,
        file_name=file.filename,
        version_id=version_id,
    )
    db.add(db_file)

    # update the version
    setattr(version, "file_id", db_file.id)

    await db.commit()
    await db.refresh(db_file)
    return db_file
