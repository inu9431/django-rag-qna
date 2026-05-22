from fastapi import FastAPI
from sqlalchemy import text

from app.api.router import router
from app.database import Base, engine

app = FastAPI(
    title="FastAPI Docker Template",
    description="FastAPI project with Docker and CI/CD",
    version="0.1.0",
)

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)
