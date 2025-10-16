import logging
from contextlib import asynccontextmanager

from app.api.endpoin import routed
from app.core import logger
from app.core.settings import config
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

logger.setup_logging()
log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("start...")
    yield
    log.info("stop...")


app = FastAPI(
    lifespan=lifespan, default_response_class=ORJSONResponse, root_path=config.root_path
)
app.include_router(routed)
