"""Usuario API schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict

ACTIVO_DESCRIPTION = "Estado activo del usuario"
USER_NAME_DESCRIPTION = "Nombre del usuario"
USER_EMAIL_DESCRIPTION = "Email del usuario"


class CreateUsuarioSchema(BaseModel):
    """Schema for creating a usuario."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nombre": "Juan Pérez",
                "email": "juan.perez@example.com",
                "activo": True,
            }
        }
    )

    nombre: str = Field(
        ..., min_length=1, max_length=255, description=USER_NAME_DESCRIPTION
    )
    email: EmailStr = Field(..., description=USER_EMAIL_DESCRIPTION)
    activo: bool = Field(default=True, description=ACTIVO_DESCRIPTION)


class UpdateUsuarioSchema(BaseModel):
    """Schema for updating a usuario."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nombre": "Juan Pérez Actualizado",
                "email": "juan.perez.nuevo@example.com",
                "activo": False,
            }
        }
    )

    nombre: Optional[str] = Field(
        None, min_length=1, max_length=255, description=USER_NAME_DESCRIPTION
    )
    email: Optional[EmailStr] = Field(None, description=USER_EMAIL_DESCRIPTION)
    activo: Optional[bool] = Field(None, description=ACTIVO_DESCRIPTION)


class UsuarioResponseSchema(BaseModel):
    """Schema for usuario response."""

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "nombre": "Juan Pérez",
                "email": "juan.perez@example.com",
                "activo": True,
                "fecha_creacion": "2024-01-01T00:00:00",
                "fecha_actualizacion": "2024-01-01T00:00:00",
            }
        },
    )

    id: int = Field(..., description="ID del usuario")
    nombre: str = Field(..., description=USER_NAME_DESCRIPTION)
    email: str = Field(..., description=USER_EMAIL_DESCRIPTION)
    activo: bool = Field(..., description=ACTIVO_DESCRIPTION)
    fecha_creacion: datetime = Field(..., description="Fecha de creación")
    fecha_actualizacion: datetime = Field(
        ..., description="Fecha de actualización"
    )


class ErrorResponseSchema(BaseModel):
    """Schema for error responses."""

    model_config = ConfigDict(
        json_schema_extra={"example": {"detail": "Error message here"}}
    )

    detail: str = Field(..., description="Error detail message")
