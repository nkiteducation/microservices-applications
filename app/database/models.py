from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Table, Uuid, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.core.enum import ContactMethod


class CoreModel(DeclarativeBase, AsyncAttrs):
    pass


class ID:
    id: Mapped[UUID] = mapped_column(
        Uuid(True), primary_key=True, index=True, default=uuid4
    )


class Timestamp:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(True),
        server_default=func.now(),
        server_onupdate=func.now(),
    )


application_technology = Table(
    "application_technology",
    CoreModel.metadata,
    Column(
        "application_id",
        ForeignKey("applications.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "technology_id",
        ForeignKey("technologles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Application(CoreModel, ID, Timestamp):
    __tablename__ = "applications"

    first_name: Mapped[str]
    last_name: Mapped[str]
    contact_method: Mapped[ContactMethod] = mapped_column(
        Enum(ContactMethod, name="contactmethod", native_enum=True)
    )
    phone: Mapped[str | None] = mapped_column(default=None)
    email: Mapped[str | None] = mapped_column(default=None)
    telegram: Mapped[str | None] = mapped_column(default=None)

    technologies: Mapped[list["Technologles"]] = relationship(
        secondary=application_technology,
        back_populates="applications",
    )


class Technologles(CoreModel, ID, Timestamp):
    __tablename__ = "technologles"

    name: Mapped[str] = mapped_column(index=True)
    description: Mapped[str]

    applications: Mapped[list[Application]] = relationship(
        secondary=application_technology,
        back_populates="technologies",
    )
