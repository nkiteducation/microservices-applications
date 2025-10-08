from datetime import datetime
from typing import Annotated
from uuid import UUID

from app.utils.enum import ContactMethod
from pydantic import BaseModel, EmailStr, Field, model_validator
from pydantic_core import PydanticCustomError
from pydantic_extra_types.phone_numbers import PhoneNumberValidator

RE_NAME = r"^[\p{L}\s-]{5,50}+$"
RE_TELEGRAM = r"^[A-Za-z0-9_.]{5,}+$"
RE_TECHNOLOGIES = r"^[\p{L}0-9\s+#\.]{2,50}$"


class RequestsApplication(BaseModel):
    first_name: Annotated[str, Field(alias="ferstName", pattern=RE_NAME)] = "firstName"
    last_name: Annotated[str, Field(alias="lastName", pattern=RE_NAME)] = "lastName"
    contact_method: Annotated[ContactMethod, Field(alias="contactMethod")] = (
        ContactMethod.EMAIL
    )
    phone: Annotated[str, PhoneNumberValidator("UA", "E164")] | None = None
    email: EmailStr | None = None
    telegram: Annotated[str, Field(pattern=RE_TELEGRAM)] | None = None
    technologies: list[Annotated[str, Field(pattern=RE_TECHNOLOGIES)]] = [
        "Python",
        "FastAPI",
        "SQLalchemy",
    ]

    model_config = {"populate_by_name": True, "from_attributes": True}

    @model_validator(mode="after")
    def check_contact_method(self):
        method = self.contact_method.value
        if not getattr(self, method):
            raise PydanticCustomError(
                "missing_contact_value",
                f"The “{method}” field must be filled in.",
            )

        return self


class ResponsesApplication(RequestsApplication):
    id: UUID
    created_at: datetime
    updated_at: datetime
