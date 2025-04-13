import time
from contextlib import contextmanager, asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from src.auth.routers.admin_router import admin_router
from src.auth.routers.auth_router import auth_router
from src.auth.routers.user_router import user_router
# from src.object.object_router import obj_router
from src.config import origins
from src.database import get_db
from src.db.mongo import close_mongo_connection, connect_to_mongo
from src.objects.routers.admin_objects_router import admin_objects_router
from src.objects.routers.objects_router import object_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_to_mongo()
    yield
    close_mongo_connection()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow only these origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/")
async def health_check():
    return {"status": "OK"}


app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])

app.include_router(user_router, prefix="/api/user", tags=["User"])
app.include_router(admin_router, prefix="/api/admin", tags=["Admin"])
app.include_router(object_router, prefix="/api/objects", tags=["Objects"])

app.include_router(admin_objects_router, prefix="/api/admin/objects", tags=["Admin/Objects"])



if __name__ == '__main__':
    get_db()
    uvicorn.run("src.app:app", host="127.0.0.1", port=8000, reload=True)