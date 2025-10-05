from datetime import datetime
import enum
from uuid import UUID
from pydantic import BaseModel, Field, EmailStr
from typing import Annotated
from pydantic_extra_types.phone_numbers import PhoneNumberValidator
from phonenumbers import PhoneNumberFormat

RE_NAME = r"^[\p{L}\s-]{5,50}+$"
RE_TELEGRAM = r"^[A-Za-z0-9_.]{5,}+$"
RE_TECHNOLOGIES = r"^[\p{L}0-9 +#\.]{2,50}$"


class ContactMethod(enum.Enum):
    EMAIL = "email"
    PHONE = "phone"
    TELEGRAM = "telegram"


class RequestsApplication(BaseModel):
    first_name: Annotated[str, Field(alias="ferstName", pattern=RE_NAME)]
    last_name: Annotated[str, Field(alias="lastName", pattern=RE_NAME)]
    contact_method: Annotated[ContactMethod, Field(alias="contactMethod")]
    phone: Annotated[str, PhoneNumberValidator("UA", "E164")]
    email: EmailStr
    telegram: Annotated[str, Field(pattern=RE_TELEGRAM)]
    technologies: list[Annotated[str, Field(pattern=RE_TECHNOLOGIES)]]

    model_config = {"populate_by_name": True}


class ResponsesApplication(RequestsApplication):
    id: UUID
    created_at: datetime
    updated_at: datetime
