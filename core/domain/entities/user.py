"""User entity."""

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Optional

from core.domain.value_objects.email_address import EmailAddress


@dataclass
class User:
    """User domain entity."""

    id: Optional[int]
    name: str
    email: EmailAddress
    active: bool
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        """Validate entity invariants."""
        if not self.name or not self.name.strip():
            raise ValueError("Name cannot be empty")
        if len(self.name) > 255:
            raise ValueError("Name cannot exceed 255 characters")

    def activate(self) -> None:
        """Activate the user."""
        from core.domain.services.user_domain_service import (
            UserDomainService,
        )

        if not UserDomainService.can_activate_user(self):
            raise ValueError("User is already active")
        self.active = True
        self.updated_at = datetime.now(UTC)

    def deactivate(self) -> None:
        """Deactivate the user."""
        from core.domain.services.user_domain_service import (
            UserDomainService,
        )

        if not UserDomainService.can_deactivate_user(self):
            raise ValueError("User is already inactive")
        self.active = False
        self.updated_at = datetime.now(UTC)

    def update_name(self, new_name: str) -> None:
        """Update user name."""
        if not new_name or not new_name.strip():
            raise ValueError("Name cannot be empty")
        if len(new_name) > 255:
            raise ValueError("Name cannot exceed 255 characters")
        self.name = new_name.strip()
        self.updated_at = datetime.now(UTC)
