from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.models.base import Base
from backend.db.session import engine

from backend.api.routers.task import router as task_router
from backend.api.routers.categories import router as category_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield



app = FastAPI(lifespan = lifespan)
app.include_router(router = task_router)
app.include_router(category_router)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
