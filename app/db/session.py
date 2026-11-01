from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from app.core.config import settings

engine = create_async_engine(
    url=settings.database_url,
    echo=False
)

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db_session()-> AsyncGenerator[AsyncSession, None] :
    async with async_session_factory() as session:
        yield session