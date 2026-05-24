from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.router.user_router import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
