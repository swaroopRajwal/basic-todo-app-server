from fastapi import APIRouter, Depends, status
from app.schemas.todo import TodoResponse, TodoCreate, TodoUpdate
from app.schemas.api_response import ResponseSchema
from app.database.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.todos import todo_service

# /api/todo
router = APIRouter()


# @todoRouter.post("/", response_model=PaginatedResponseSchema[TodoResponse])
# async def get_all_todos(
#     params: PaginationParamsSchema,
#     db: AsyncSession = Depends(get_db),
# ):

#     pass


@router.post(
    "", response_model=ResponseSchema[TodoResponse], status_code=status.HTTP_201_CREATED
)
async def create_todo(data: TodoCreate, db: AsyncSession = Depends(get_db)):
    return await todo_service.create_todo(db, data)


@router.get("/{id}", response_model=ResponseSchema[TodoResponse])
async def get_single_todo(
    id: str,
    db: AsyncSession = Depends(get_db),
):
    return await todo_service.get_single_todo(db, id)


@router.put("/{id}", response_model=ResponseSchema[TodoResponse])
async def update_single_todo(
    id: str,
    data: TodoUpdate,
    db: AsyncSession = Depends(get_db),
):
    return await todo_service.update_single_todo(db, id, data)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_single_todo(
    id: str,
    db: AsyncSession = Depends(get_db),
):
    return await todo_service.delete_single_todo(db, id)
