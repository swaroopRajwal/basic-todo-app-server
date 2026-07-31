from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_db
from app.schemas.api_response import PaginatedResponseSchema, ResponseSchema
from app.schemas.tag import TagCreate, TagQueryParamsSchema, TagResponse, TagUpdate
from app.services.tags import tag_service


router = APIRouter()


@router.get("", response_model=PaginatedResponseSchema[TagResponse])
async def get_all_tags(
    params: TagQueryParamsSchema = Depends(), db: AsyncSession = Depends(get_db)
):
    return await tag_service.get_all_tags(db, params)


@router.post(
    "", response_model=ResponseSchema[TagResponse], status_code=status.HTTP_201_CREATED
)
async def create_tag(data: TagCreate, db: AsyncSession = Depends(get_db)):
    return await tag_service.create_tag(db, data)


@router.get("/{id}", response_model=ResponseSchema[TagResponse])
async def get_single_tag(id: str, db: AsyncSession = Depends(get_db)):
    return await tag_service.get_single_tag(db, id)


@router.put("/{id}", response_model=ResponseSchema[TagResponse])
async def update_single_tag(id: str, data: TagUpdate, db: AsyncSession = Depends(get_db)):
    return await tag_service.update_single_tag(db, id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_single_tag(id: str, db: AsyncSession = Depends(get_db)):
    return await tag_service.delete_single_tag(db, id)
