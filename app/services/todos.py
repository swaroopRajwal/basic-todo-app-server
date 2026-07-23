from app.schemas.api_response import ResponseSchema
from app.schemas.todo import TodoCreate, TodoUpdate
from sqlalchemy import select
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
