import asyncio
import logging

import orjson

from app.core.settings import config
from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

log = logging.getLogger(__name__)


class SessionManager:
    def __init__(self, url):
        self.engine = create_async_engine(
            url,
            pool_size=10,
            max_overflow=20,
            json_serializer=orjson.dumps,
            json_deserializer=orjson.loads,
            future=True,
        )
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
        except Exception as e:
            log.error("error in session: %s", e)
            await session.rollback()
            raise
        finally:
            await session.close()
            await self.scoped_session.remove()


session = SessionManager(config.database.url.encoded_string())
