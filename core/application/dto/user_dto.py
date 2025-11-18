"""User DTOs."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CreateUserDto:
    """DTO for creating a user."""

    name: str
    email: str
    active: bool = True


@dataclass
class UpdateUserDto:
    """DTO for updating a user."""

    name: Optional[str] = None
    email: Optional[str] = None
    active: Optional[bool] = None


@dataclass
class UserResponseDto:
    """DTO for user response."""

    id: int
    name: str
    email: str
    active: bool
    created_at: datetime
    updated_at: datetime
