import logging
from uuid import UUID

from app.api.dto import RequestsApplication, ResponsesApplication
from app.database.models import Application, Technologles
from app.database.session import session
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

log = logging.getLogger(__name__)
routed = APIRouter()

@routed.get("/", response_model=dict[str, list[ResponsesApplication]])
async def _get_all(session: AsyncSession = Depends(session.get)):
    stmt = select(Application).options(selectinload(Application.technologies))
    result = await session.scalars(stmt)
    applications = result.all()

    if not applications:
        log.warning("No applications found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return {
        "items": [
            ResponsesApplication.model_validate(
                {
                    **application.__dict__,
                    "technologies": [t.name for t in application.technologies],
                }
            )
            for application in applications
        ]
    }


@routed.get("/{id}", response_model=ResponsesApplication)
async def _get_by_id(id: UUID, session: AsyncSession = Depends(session.get)):
    application = await session.get(Application, id)
    if not application:
        log.warning("Application not found: id=%s", id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ResponsesApplication.model_validate(
        {
            **application.__dict__,
            "technologies": [t.name for t in application.technologies],
        }
    )


@routed.post("/", status_code=status.HTTP_201_CREATED)
async def _create(
    application: RequestsApplication, session: AsyncSession = Depends(session.get)
):
    data = application.model_dump()
    technologies = data.pop("technologies")

    stmt = select(Technologles).where(Technologles.name.in_(technologies))

    app = Application(**data)
    app.technologies.extend((await session.scalars(stmt)).all())

    session.add(app)
    await session.commit()

    return {"message": "OK"}


@routed.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def _delete(id: UUID, session: AsyncSession = Depends(session.get)):
    app = await session.get(Application, id)
    if app is None:
        log.warning("Application not found for deletion: id=%s", id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await session.delete(app)
    await session.commit()

    return {"message": "OK"}
