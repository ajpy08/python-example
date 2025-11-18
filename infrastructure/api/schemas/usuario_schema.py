"""Usuario API schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


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

    nombre: str = Field(..., min_length=1, max_length=255, description="Nombre del usuario")
    email: EmailStr = Field(..., description="Email del usuario")
    activo: bool = Field(default=True, description="Estado activo del usuario")


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

    nombre: Optional[str] = Field(None, min_length=1, max_length=255, description="Nombre del usuario")
    email: Optional[EmailStr] = Field(None, description="Email del usuario")
    activo: Optional[bool] = Field(None, description="Estado activo del usuario")


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
        }
    )

    id: int = Field(..., description="ID del usuario")
    nombre: str = Field(..., description="Nombre del usuario")
    email: str = Field(..., description="Email del usuario")
    activo: bool = Field(..., description="Estado activo del usuario")
    fecha_creacion: datetime = Field(..., description="Fecha de creación")
    fecha_actualizacion: datetime = Field(..., description="Fecha de actualización")


class ErrorResponseSchema(BaseModel):
    """Schema for error responses."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "Error message here"
            }
        }
    )

    detail: str = Field(..., description="Error detail message")

