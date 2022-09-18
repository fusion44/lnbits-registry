import imp
from sqlalchemy import select
from sqlalchemy.orm import Session
import app.extensions.schema as schema
import app.extensions.models as models
from app.db import User

# CRUD service for extensions


async def add_extension(
    db: Session, i: schema.ExtensionInput, user: User
) -> schema.Extension:
    db_ext = models.Extension(
        **i.dict(),
        owner=str(user.id),
    )
    db.add(db_ext)
    await db.commit()
    await db.refresh(db_ext)
    return db_ext


async def list_all_extensions(
    db: Session, skip: int = 0, limit: int = 100
) -> list[schema.Extension]:
    res = await db.execute(select(models.Extension).offset(skip).limit(limit))
    b = res.unique().scalars().all()
    return b


async def delete_extension(id: int) -> schema.Extension:
    pass


async def update_extension(
    db: Session, i: schema.ExtensionUpdateInput, user: User
) -> list[schema.Extension]:
    # get extension from the database and check if the user doesn't lie to us
    db_ext = await db.get(models.Extension, i.id)
    if db_ext.owner != str(user.id):
        raise Exception("You are not the owner of this extension!")

    # update the extension
    for k, v in i.dict().items():
        if v is not None and k != "id":
            setattr(db_ext, k, v)

    await db.commit()
    await db.refresh(db_ext)
    return db_ext
