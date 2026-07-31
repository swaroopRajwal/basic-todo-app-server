from fastapi import HTTPException, status
from sqlalchemy import asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.tags import TagsTable
from app.schemas.api_request import SortOrder
from app.schemas.api_response import PaginatedResponseSchema, ResponseSchema
from app.schemas.tag import TagCreate, TagQueryParamsSchema, TagSortField, TagUpdate
from app.utils import get_id


class TagService:
    async def _get_tag_by_id(self, db: AsyncSession, id: str) -> TagsTable | None:
        result = await db.execute(select(TagsTable).where(TagsTable.id == id))
        return result.scalars().first()

    async def _tag_name_exists(
        self, db: AsyncSession, name: str, exclude_id: str | None = None
    ) -> bool:
        stmt = select(TagsTable.id).where(func.lower(TagsTable.name) == name.lower())
        if exclude_id is not None:
            stmt = stmt.where(TagsTable.id != exclude_id)
        return (await db.execute(stmt)).scalar_one_or_none() is not None

    async def create_tag(self, db: AsyncSession, data: TagCreate):
        if await self._tag_name_exists(db, data.name):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Tag name already exists"
            )

        tag = TagsTable(id=get_id(), name=data.name)
        db.add(tag)
        await db.commit()
        await db.refresh(tag)
        return ResponseSchema(status=True, data=tag)

    async def get_all_tags(self, db: AsyncSession, params: TagQueryParamsSchema):
        stmt = select(TagsTable)

        if params.search:
            stmt = stmt.where(TagsTable.name.ilike(f"%{params.search}%"))

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await db.execute(count_stmt)).scalar_one()

        sort_field = params.sort_by or TagSortField.created_at
        sort_column = getattr(TagsTable, sort_field.value)
        order_fn = asc if params.sort_order == SortOrder.asc else desc
        stmt = stmt.order_by(order_fn(sort_column))
        stmt = stmt.offset((params.page - 1) * params.limit).limit(params.limit)

        result = await db.execute(stmt)
        return PaginatedResponseSchema(
            status=True,
            data=result.scalars().all(),
            page=params.page,
            limit=params.limit,
            count=total,
        )

    async def get_single_tag(self, db: AsyncSession, id: str):
        tag = await self._get_tag_by_id(db, id)
        if tag:
            return ResponseSchema(status=True, data=tag)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")

    async def update_single_tag(self, db: AsyncSession, id: str, data: TagUpdate):
        tag = await self._get_tag_by_id(db, id)
        if not tag:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")

        updated_tag = data.model_dump(exclude_unset=True)
        if "name" in updated_tag and await self._tag_name_exists(
            db, updated_tag["name"], exclude_id=id
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Tag name already exists"
            )

        for field, value in updated_tag.items():
            setattr(tag, field, value)

        await db.commit()
        await db.refresh(tag)
        return ResponseSchema(status=True, data=tag)

    async def delete_single_tag(self, db: AsyncSession, id: str):
        tag = await self._get_tag_by_id(db, id)
        if not tag:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")

        await db.delete(tag)
        await db.commit()


tag_service = TagService()
