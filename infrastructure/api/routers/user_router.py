"""User router."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.application.dto.user_dto import (
    CreateUserDto,
    UpdateUserDto,
)
from core.application.use_cases.create_user_use_case import (
    CreateUserUseCase,
)
from core.application.use_cases.delete_user_use_case import (
    DeleteUserUseCase,
)
from core.application.use_cases.get_user_use_case import (
    GetUserUseCase,
)
from core.application.use_cases.list_users_use_case import (
    ListUsersUseCase,
)
from core.application.use_cases.update_user_use_case import (
    UpdateUserUseCase,
)
from infrastructure.adapters.repositories.user_repository_postgres_adapter import (  # noqa: E501
    UserRepositoryPostgresAdapter,
)
from infrastructure.api.schemas.user_schema import (
    CreateUserSchema,
    UpdateUserSchema,
    UserResponseSchema,
)
from infrastructure.database.session import get_db

router = APIRouter(prefix="/users", tags=["users"])


def get_user_repository(
    db: Session = Depends(get_db),
) -> UserRepositoryPostgresAdapter:
    """Get user repository adapter."""
    return UserRepositoryPostgresAdapter(db)


@router.post(
    "",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user with name, email, and active status",
)
def create_user(
    schema: CreateUserSchema,
    repository: UserRepositoryPostgresAdapter = Depends(
        get_user_repository
    ),
) -> UserResponseSchema:
    """Create a new user."""
    try:
        dto = CreateUserDto(
            name=schema.name,
            email=schema.email,
            active=schema.active,
        )
        use_case = CreateUserUseCase(repository)
        result = use_case.execute(dto)
        return UserResponseSchema(**result.__dict__)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.get(
    "",
    response_model=List[UserResponseSchema],
    summary="List all users",
    description="Get a list of all users with pagination support",
)
def list_users(
    skip: int = 0,
    limit: int = 100,
    repository: UserRepositoryPostgresAdapter = Depends(
        get_user_repository
    ),
) -> List[UserResponseSchema]:
    """List all users."""
    use_case = ListUsersUseCase(repository)
    results = use_case.execute(skip=skip, limit=limit)
    return [UserResponseSchema(**result.__dict__) for result in results]


@router.get(
    "/{user_id}",
    response_model=UserResponseSchema,
    summary="Get user by ID",
    description="Get a specific user by its ID",
)
def get_user(
    user_id: int,
    repository: UserRepositoryPostgresAdapter = Depends(
        get_user_repository
    ),
) -> UserResponseSchema:
    """Get user by id."""
    use_case = GetUserUseCase(repository)
    result = use_case.execute(user_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    return UserResponseSchema(**result.__dict__)


@router.put(
    "/{user_id}",
    response_model=UserResponseSchema,
    summary="Update user",
    description="Update an existing user by its ID",
)
def update_user(
    user_id: int,
    schema: UpdateUserSchema,
    repository: UserRepositoryPostgresAdapter = Depends(
        get_user_repository
    ),
) -> UserResponseSchema:
    """Update user."""
    try:
        dto = UpdateUserDto(
            name=schema.name,
            email=schema.email,
            active=schema.active,
        )
        use_case = UpdateUserUseCase(repository)
        result = use_case.execute(user_id, dto)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found",
            )
        return UserResponseSchema(**result.__dict__)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description="Delete a user by its ID",
)
def delete_user(
    user_id: int,
    repository: UserRepositoryPostgresAdapter = Depends(
        get_user_repository
    ),
) -> None:
    """Delete user."""
    use_case = DeleteUserUseCase(repository)
    deleted = use_case.execute(user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
