import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from app.auth.router import custom_auth_router
from app.db import create_db_and_tables
from app.users import jwt_backend, cookie_backend, fastapi_users
from app.extensions.router import router as ext_router
from app.versions.router import router as vs_router
from app.schemas import UserRead, UserCreate, UserUpdate
from starlette.middleware.cors import CORSMiddleware


# Make sure the data path exists
p = os.path.join(os.getcwd(), "data/files")
try:
    os.makedirs(p)
except FileExistsError:
    pass


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(f"/static", StaticFiles(directory="app/static/"), name="static")


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def index():
    with open("app/static/index.html") as f:
        lines = f.read()

    return HTMLResponse(lines)


app.include_router(
    fastapi_users.get_auth_router(jwt_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_auth_router(cookie_backend), prefix="/auth/cookie", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(custom_auth_router, prefix="/users", tags=["Users"])
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["Users"],
)
app.include_router(ext_router, prefix="/ext", tags=["Extensions"])
app.include_router(vs_router, prefix="/version", tags=["Versions"])


@app.on_event("startup")
async def on_startup():
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()
