from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel

from app.core.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)