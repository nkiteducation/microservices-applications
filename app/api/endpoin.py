from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.session import session
from app.database.models import Application
from app.api.dto import RequestsApplication, ResponsesApplication
from fastapi import APIRouter, Depends

routed = APIRouter(prefix="/applications")


@routed.get("/", response_model=dict[str, list[RequestsApplication] | None])
async def get(session: AsyncSession = Depends(session.get)):
    stmt = select(Application)
    result = await session.scalars(stmt)
    applications = result.all()

    return {
        "items": [
            ResponsesApplication.model_validate(application)
            for application in applications
        ]
    }
