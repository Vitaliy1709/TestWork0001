from typing import Any, Sequence

from sqlalchemy import select, or_, Row, RowMapping
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.task import Task
from app.schemas.task import TaskCreate


class CRUDTask:

    async def create(self, db: AsyncSession, task_in: TaskCreate, owner_id: int) -> Task:
        new_task = Task(
            title=task_in.title,
            description=task_in.description,
            status=task_in.status,
            priority=task_in.priority,
            owner_id=owner_id,
        )
        db.add(new_task)
        await db.commit()
        await db.refresh(new_task)
        return new_task

    async def search(self, db: AsyncSession, owner_id: int, q: str) -> Sequence[Row[Any] | RowMapping | Any]:
        query = select(Task).where(
            Task.owner_id == owner_id,
            or_(
                Task.title.ilike(f"%{q}%"),
                Task.description.ilike(f"%{q}%")
            )
        )
        result: Result = await db.execute(query)
        tasks = result.scalars().all()
        return tasks


crud_task = CRUDTask()
