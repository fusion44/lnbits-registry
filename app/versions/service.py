from sqlalchemy import select
from sqlalchemy.orm import Session
import app.versions.schema as schema
import app.extensions.models as ext_models
import app.versions.models as models
from app.db import User

# CRUD service for extension versions


async def add_version(
    ext_id: int, db: Session, input: schema.ExtensionVersionInput, user: User
) -> schema.ExtensionVersion:
    db_ext = await db.get(ext_models.Extension, ext_id)

    if db_ext.owner != str(user.id):
        raise Exception("You are not the owner of this extension!")

    db_vs = models.ExtensionVersion(**input.dict(), extension_id=ext_id)
    db.add(db_vs)
    await db.commit()
    await db.refresh(db_vs)
    return db_vs


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
