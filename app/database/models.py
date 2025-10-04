from datetime import datetime
from uuid import UUID
from sqlalchemy import Table, ForeignKey, Column, Enum, Uuid, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import enum


class ContactMethod(enum.Enum):
    EMAIL = "email"
    PHONE = "phone"
    TELEGRAM = "telegram"


class CoreModel(DeclarativeBase):
    pass


class ID:
    id: Mapped[UUID] = mapped_column(Uuid(True), primary_key=True, index=True)


class Timestamp:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(True), server_default=func.now(), index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(True),
        server_default=func.now(),
        server_onupdate=func.now(),
        index=True,
    )


application_technology = Table(
    "application_technology",
    CoreModel.metadata,
    Column("application_id", ForeignKey("applications.id"), primary_key=True),
    Column("technology_id", ForeignKey("technologles.id"), primary_key=True),
)


class Applications(CoreModel, ID, Timestamp):
    __tablename__ = "applications"

    first_name: Mapped[str]
    last_name: Mapped[str]
    contact_method: Mapped[ContactMethod] = mapped_column(Enum(ContactMethod))
    phone: Mapped[str]
    email: Mapped[str]
    telegram: Mapped[str]

    technologies: Mapped[list["Technologles"]] = relationship(
        secondary=application_technology, back_populates="applications"
    )


class Technologles(CoreModel, ID, Timestamp):
    __tablename__ = "technologles"

    name: Mapped[str]
    description: Mapped[str]

    applications: Mapped[list[Applications]] = relationship(
        secondary=application_technology, back_populates="technologies"
    )
