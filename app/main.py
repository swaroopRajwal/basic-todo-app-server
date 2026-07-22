from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import get_db
from app.database.models.health import HealthTable
from sqlalchemy import select

app = FastAPI(title="Basic Todo App Server")


@app.get("/")
async def home():
    return {
        "status": True,
        "message": "Check service health on /health and docs on /docs",
    }


@app.get("/health")
async def health(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(HealthTable))
    message = result.scalars().all()[0].message

    return {
        "status": True,
        "db_message": message,
    }
