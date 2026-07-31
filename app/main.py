from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import get_db
from app.database.models.health import HealthTable
from sqlalchemy import select
from app.api import tag, todo

app = FastAPI(title="Basic Todo App Server")

app.include_router(todo.router, prefix="/api/todo", tags=["todo"])
app.include_router(tag.router, prefix="/api/tag", tags=["tag"])


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


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    # This intercepts EVERY HTTPException and reformats it
    return JSONResponse(
        status_code=exc.status_code, content={"status": False, "message": exc.detail}
    )
