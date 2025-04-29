from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


class CRUDUser:
    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:
        """Get the user by email."""
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        return user

    async def get_by_id(self, db: AsyncSession, user_id: int) -> User | None:
        """Get a user by ID."""
        result = await db.execute(select(User).where(User.id == int(user_id)))
        user = result.scalars().first()
        return user

    async def create(self, db: AsyncSession, user_in: UserCreate) -> User:
        """Create a new user."""
        hashed_password = get_password_hash(user_in.password)
        db_user = User(
            name=user_in.name,
            email=user_in.email,
            password_hash=hashed_password,
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user


crud_user = CRUDUser()
