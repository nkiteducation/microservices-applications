import asyncio

from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from app.core.settings import config


class SessionManager:
    def __init__(self, url):
        self.engine = create_async_engine(url)
        self.session_factory = async_sessionmaker(
            self.engine,
            autoflush=False,
            expire_on_commit=False,
        )
        self.scoped_session = async_scoped_session(
            self.session_factory, asyncio.current_task
        )

    async def get(self):
        session = self.scoped_session()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
            await self.scoped_session.remove()


session = SessionManager(config.database.url.encoded_string())
