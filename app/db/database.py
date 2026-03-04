from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.db.settings import settings


engine = create_async_engine(
    url=settings.database_url,
#    echo=True
)


async_session = async_sessionmaker(engine)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session