"""Email address value object."""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class EmailAddress:
    """Value object representing an email address."""

    value: str

    def __post_init__(self) -> None:
        """Validate email format."""
        if not self.value:
            raise ValueError("Email cannot be empty")
        if not self._is_valid_email(self.value):
            raise ValueError(f"Invalid email format: {self.value}")

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Validate email format using regex."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    def __str__(self) -> str:
        """Return email as string."""
        return self.value

