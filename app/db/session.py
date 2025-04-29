from typing import Any, AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import DATABASE_URL

# Creating an asynchronous database connection engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True
)

# Asynchronous Session Factory
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# Dependency for FastAPI
async def get_db() -> AsyncGenerator[Any, Any]:
    async with async_session() as session:
        yield session
