"""User domain service."""

from core.domain.entities.user import User


class UserDomainService:
    """Domain service for User business logic."""

    @staticmethod
    def can_activate_user(user: User) -> bool:
        """
        Validate if a user can be activated.

        Business rule: A user can only be activated if they are inactive.

        Args:
            user: The User entity to validate.

        Returns:
            True if the user can be activated (active=False), False otherwise.
        """
        return not user.active

    @staticmethod
    def can_deactivate_user(user: User) -> bool:
        """
        Validate if a user can be deactivated.

        Business rule: A user can only be deactivated if they are active.

        Args:
            user: The User entity to validate.

        Returns:
            True if the user can be deactivated (active=True), False otherwise.
        """
        return user.active
