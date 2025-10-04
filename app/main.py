from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from contextlib import asynccontextmanager
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("app")

@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("start...")
    yield
    log.info("stop...")

app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse
)