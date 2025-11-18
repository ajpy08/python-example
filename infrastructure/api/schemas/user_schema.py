"""User API schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict

ACTIVE_DESCRIPTION = "User active status"
USER_NAME_DESCRIPTION = "User name"
USER_EMAIL_DESCRIPTION = "User email"


class CreateUserSchema(BaseModel):
    """Schema for creating a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "active": True,
            }
        }
    )

    name: str = Field(
        ..., min_length=1, max_length=255, description=USER_NAME_DESCRIPTION
    )
    email: EmailStr = Field(..., description=USER_EMAIL_DESCRIPTION)
    active: bool = Field(default=True, description=ACTIVE_DESCRIPTION)


class UpdateUserSchema(BaseModel):
    """Schema for updating a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "John Doe Updated",
                "email": "john.doe.new@example.com",
                "active": False,
            }
        }
    )

    name: Optional[str] = Field(
        None, min_length=1, max_length=255, description=USER_NAME_DESCRIPTION
    )
    email: Optional[EmailStr] = Field(None, description=USER_EMAIL_DESCRIPTION)
    active: Optional[bool] = Field(None, description=ACTIVE_DESCRIPTION)


class UserResponseSchema(BaseModel):
    """Schema for user response."""

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "John Doe",
                "email": "john.doe@example.com",
                "active": True,
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00",
            }
        },
    )

    id: int = Field(..., description="User ID")
    name: str = Field(..., description=USER_NAME_DESCRIPTION)
    email: str = Field(..., description=USER_EMAIL_DESCRIPTION)
    active: bool = Field(..., description=ACTIVE_DESCRIPTION)
    created_at: datetime = Field(..., description="Creation date")
    updated_at: datetime = Field(..., description="Last update date")


class ErrorResponseSchema(BaseModel):
    """Schema for error responses."""

    model_config = ConfigDict(
        json_schema_extra={"example": {"detail": "Error message here"}}
    )

    detail: str = Field(..., description="Error detail message")
