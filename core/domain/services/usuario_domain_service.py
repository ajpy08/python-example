"""Usuario domain service."""

from core.domain.entities.usuario import Usuario


class UsuarioDomainService:
    """Domain service for Usuario business logic."""

    @staticmethod
    def puede_activar_usuario(usuario: Usuario) -> bool:
        """
        Valida si un usuario puede ser activado.

        Regla de negocio: Solo se puede activar un usuario que esté inactivo.

        Args:
            usuario: La entidad Usuario a validar.

        Returns:
            True si el usuario puede ser activado (activo=False), False en caso contrario.
        """
        return not usuario.activo

    @staticmethod
    def puede_desactivar_usuario(usuario: Usuario) -> bool:
        """
        Valida si un usuario puede ser desactivado.

        Regla de negocio: Solo se puede desactivar un usuario que esté activo.

        Args:
            usuario: La entidad Usuario a validar.

        Returns:
            True si el usuario puede ser desactivado (activo=True), False en caso contrario.
        """
        return usuario.activo

