import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.api.endpoin import routed

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("start...")
    yield
    log.info("stop...")


app = FastAPI(lifespan=lifespan, default_response_class=ORJSONResponse)
app.include_router(routed)
