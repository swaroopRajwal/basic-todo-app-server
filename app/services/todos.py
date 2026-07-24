from app.schemas.api_response import ResponseSchema, PaginatedResponseSchema
from app.schemas.api_request import SortOrder
from app.schemas.todo import TodoCreate, TodoUpdate, TodoQueryParamsSchema, TodoSortField
from sqlalchemy import select, func, asc, desc
from app.database.models.todo import TodoTable
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.utils import get_id


class TodoService:
    async def create_todo(self, db: AsyncSession, data: TodoCreate):
        new_todo = TodoTable(
            id=get_id(),
            title=data.title,
            description=data.description,
        )
        db.add(new_todo)
        await db.commit()
        await db.refresh(new_todo)
        return ResponseSchema(
            status=True,
            data=new_todo,
        )

    async def get_all_todos(self, db: AsyncSession, params: TodoQueryParamsSchema):
        stmt = select(TodoTable)

        if params.search:
            stmt = stmt.where(TodoTable.title.ilike(f"%{params.search}%"))

        if params.is_completed is not None:
            stmt = stmt.where(TodoTable.is_completed == params.is_completed)

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await db.execute(count_stmt)).scalar_one()

        sort_field = params.sort_by or TodoSortField.created_at
        sort_column = getattr(TodoTable, sort_field.value)
        order_fn = asc if params.sort_order == SortOrder.asc else desc
        stmt = stmt.order_by(order_fn(sort_column))

        stmt = stmt.offset((params.page - 1) * params.limit).limit(params.limit)

        result = await db.execute(stmt)
        todos = result.scalars().all()

        return PaginatedResponseSchema(
            status=True,
            data=todos,
            page=params.page,
            limit=params.limit,
            count=total,
        )

    async def get_single_todo(self, db: AsyncSession, id: str):
        result = await db.execute(select(TodoTable).where(TodoTable.id == id))
        todo = result.scalars().first()

        if todo:
            return ResponseSchema(
                status=True,
                data=todo,
            )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    async def update_single_todo(self, db: AsyncSession, id: str, data: TodoUpdate):
        result = await db.execute(select(TodoTable).where(TodoTable.id == id))

        todo = result.scalars().first()

        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found",
            )

        updated_todo = data.model_dump(exclude_unset=True)
        for field, value in updated_todo.items():
            setattr(todo, field, value)

        await db.commit()
        await db.refresh(todo)
        return ResponseSchema(
            status=True,
            data=todo,
        )

    async def delete_single_todo(self, db: AsyncSession, id: str):
        result = await db.execute(select(TodoTable).where(TodoTable.id == id))

        todo = result.scalars().first()

        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
            )

        await db.delete(todo)
        await db.commit()


todo_service = TodoService()
