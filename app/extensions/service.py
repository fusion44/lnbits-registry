from sqlalchemy import select
from sqlalchemy.orm import Session
import app.extensions.schema as schema
import app.extensions.models as models
from app.db import User
from fastapi import HTTPException
from app.extensions.exceptions import ExtensionNotFound


# CRUD service for extensions


async def add_extension(
    db: Session, input: schema.ExtensionInput, user: User
) -> schema.Extension:
    db_ext = models.Extension(
        **input.dict(),
        owner=str(user.id),
    )
    db.add(db_ext)
    await db.commit()
    await db.refresh(db_ext)
    return db_ext


async def list_all_extensions(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    include_unversioned: bool = False,
) -> list[schema.Extension]:
    res = await db.execute(select(models.Extension).offset(skip).limit(limit))
    b = res.unique().scalars().all()

    if not include_unversioned:
        b = [i for i in b if len(i.versions) > 0]

    return b


async def delete_extension(id: int) -> schema.Extension:
    pass


async def update_extension(
    id: int,
    db: Session,
    input: schema.ExtensionUpdateInput,
    user: User,
) -> list[schema.Extension]:
    # get extension from the database and check if the user doesn't lie to us
    db_ext = await db.get(models.Extension, id)
    if db_ext.owner != str(user.id):
        raise Exception("You are not the owner of this extension!")

    # update the extension
    for k, v in input.dict().items():
        if v is not None and k != "id":
            setattr(db_ext, k, v)

    await db.commit()
    await db.refresh(db_ext)
    return db_ext


async def get_extension(id: int | str, db: Session) -> schema.Extension:
    if isinstance(id, str):
        q = select(models.Extension).where(models.Extension.name == id)
        res = await db.execute(q)
        res = res.unique().scalar_one_or_none()
        if res is None:
            raise ExtensionNotFound()

        return res
    if isinstance(id, int):
        return await db.get(models.Extension, id)

    raise HTTPException("Id must either be an positive int or a non-empty string")
