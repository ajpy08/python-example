"""Usuario router."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.application.dto.usuario_dto import (
    CreateUsuarioDto,
    UpdateUsuarioDto,
)
from core.application.use_cases.create_usuario_use_case import (
    CreateUsuarioUseCase,
)
from core.application.use_cases.delete_usuario_use_case import (
    DeleteUsuarioUseCase,
)
from core.application.use_cases.get_usuario_use_case import (
    GetUsuarioUseCase,
)
from core.application.use_cases.list_usuarios_use_case import (
    ListUsuariosUseCase,
)
from core.application.use_cases.update_usuario_use_case import (
    UpdateUsuarioUseCase,
)
from infrastructure.adapters.repositories.usuario_repository_postgres_adapter import (
    UsuarioRepositoryPostgresAdapter,
)
from infrastructure.api.schemas.usuario_schema import (
    CreateUsuarioSchema,
    UpdateUsuarioSchema,
    UsuarioResponseSchema,
)
from infrastructure.database.session import get_db

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


def get_usuario_repository(
    db: Session = Depends(get_db),
) -> UsuarioRepositoryPostgresAdapter:
    """Get usuario repository adapter."""
    return UsuarioRepositoryPostgresAdapter(db)


@router.post(
    "",
    response_model=UsuarioResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new usuario",
    description="Create a new usuario with nombre, email, and activo status",
)
def create_usuario(
    schema: CreateUsuarioSchema,
    repository: UsuarioRepositoryPostgresAdapter = Depends(
        get_usuario_repository
    ),
) -> UsuarioResponseSchema:
    """Create a new usuario."""
    try:
        dto = CreateUsuarioDto(
            nombre=schema.nombre,
            email=schema.email,
            activo=schema.activo,
        )
        use_case = CreateUsuarioUseCase(repository)
        result = use_case.execute(dto)
        return UsuarioResponseSchema(**result.__dict__)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.get(
    "",
    response_model=List[UsuarioResponseSchema],
    summary="List all usuarios",
    description="Get a list of all usuarios with pagination support",
)
def list_usuarios(
    skip: int = 0,
    limit: int = 100,
    repository: UsuarioRepositoryPostgresAdapter = Depends(
        get_usuario_repository
    ),
) -> List[UsuarioResponseSchema]:
    """List all usuarios."""
    use_case = ListUsuariosUseCase(repository)
    results = use_case.execute(skip=skip, limit=limit)
    return [UsuarioResponseSchema(**result.__dict__) for result in results]


@router.get(
    "/{usuario_id}",
    response_model=UsuarioResponseSchema,
    summary="Get usuario by ID",
    description="Get a specific usuario by its ID",
)
def get_usuario(
    usuario_id: int,
    repository: UsuarioRepositoryPostgresAdapter = Depends(
        get_usuario_repository
    ),
) -> UsuarioResponseSchema:
    """Get usuario by id."""
    use_case = GetUsuarioUseCase(repository)
    result = use_case.execute(usuario_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario with id {usuario_id} not found",
        )
    return UsuarioResponseSchema(**result.__dict__)


@router.put(
    "/{usuario_id}",
    response_model=UsuarioResponseSchema,
    summary="Update usuario",
    description="Update an existing usuario by its ID",
)
def update_usuario(
    usuario_id: int,
    schema: UpdateUsuarioSchema,
    repository: UsuarioRepositoryPostgresAdapter = Depends(
        get_usuario_repository
    ),
) -> UsuarioResponseSchema:
    """Update usuario."""
    try:
        dto = UpdateUsuarioDto(
            nombre=schema.nombre,
            email=schema.email,
            activo=schema.activo,
        )
        use_case = UpdateUsuarioUseCase(repository)
        result = use_case.execute(usuario_id, dto)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario with id {usuario_id} not found",
            )
        return UsuarioResponseSchema(**result.__dict__)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.delete(
    "/{usuario_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete usuario",
    description="Delete a usuario by its ID",
)
def delete_usuario(
    usuario_id: int,
    repository: UsuarioRepositoryPostgresAdapter = Depends(
        get_usuario_repository
    ),
) -> None:
    """Delete usuario."""
    use_case = DeleteUsuarioUseCase(repository)
    deleted = use_case.execute(usuario_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario with id {usuario_id} not found",
        )
