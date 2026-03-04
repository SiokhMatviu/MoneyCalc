from app.db.database import engine, Base


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


#async def drop_tables():
#    async with engine.begin() as conn:
#        await conn.execute(text("DROP SCHEMA public CASCADE"))
#        await conn.execute(text("CREATE SCHEMA public"))