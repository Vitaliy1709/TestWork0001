from fastapi import APIRouter, Depends, HTTPException, status as http_status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.crud_task import crud_task
from app.db.models import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, StatusEnum
from app.api.deps import get_current_user
from app.db.session import get_db
from sqlalchemy import or_, cast, Date

from datetime import datetime

router = APIRouter()


# Create a new task
@router.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=http_status.HTTP_201_CREATED,
    summary="Create a new task",
)
async def create_task(
        task_in: TaskCreate,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(get_current_user),
):
    task = await crud_task.create(db, task_in, owner_id=current_user.id)
    return task


# Updating a task
@router.put(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Update a task with id.",
)
async def update_task(
        task_id: int,
        task_in: TaskUpdate,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(get_current_user),
):
    result = await db.execute(select(Task).where(Task.id == task_id, Task.owner_id == current_user.id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for var, value in task_in.model_dump(exclude_unset=True).items():
        setattr(task, var, value)

    await db.commit()
    await db.refresh(task)
    return task


# Getting a list of tasks with filtering
@router.get(
    "/tasks",
    response_model=List[TaskResponse],
    summary="Get a list of tasks filtered by status, priority, and creation date."
)
async def get_tasks(
        task_status: Optional[StatusEnum] = None,
        priority: Optional[int] = None,
        created_at: Optional[str] = None,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(get_current_user),
):
    # Form a request to receive tasks for the current user
    query = select(Task).where(Task.owner_id == current_user.id)

    # Add filters to search by status, priority and creation date
    if task_status:
        query = query.where(Task.status == task_status)
    if priority is not None:
        query = query.where(Task.priority == priority)
    if created_at:
        try:
            # Convert a string to a datetime object (date only, no time)
            created_at_date = datetime.strptime(created_at, "%Y-%m-%d").date()
            query = query.where(cast(Task.created_at, Date) == created_at_date)

        except ValueError:
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format. Use YYYY-MM-DD."
            )

    # Query the database
    result = await db.execute(query)
    tasks = result.scalars().all()

    # Returning a list of tasks
    return tasks


# Search tasks by title or description
@router.get(
    "/tasks/search",
    response_model=List[TaskResponse],
    summary="Search for tasks that contain the specified substring in the name or description."
)
async def search_tasks(
        q: str,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(get_current_user),
):
    query = select(Task).where(
        Task.owner_id == current_user.id,
        or_(
            Task.title.ilike(f"%{q}%"),
            Task.description.ilike(f"%{q}%")
        )
    )

    result = await db.execute(query)
    tasks = result.scalars().all()
    return tasks
