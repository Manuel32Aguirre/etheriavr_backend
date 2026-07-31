"""
Capa de autorización para prevenir ataques IDOR
(Insecure Direct Object Reference).

Regla fundamental: un usuario solo puede acceder a sus propios recursos.
Cuando el `user_id` indicado NO coincide con el usuario autenticado,
se responde 404 (en lugar de 403) para evitar confirmar la existencia
de recursos o usuarios ajenos.
"""

from fastapi import HTTPException, status
from models.entities.User import User


def require_owner(
    requested_user_id: int,
    current_user: User,
    *,
    entity_name: str = "recurso",
) -> User:
    """
    Valida que el ``requested_user_id`` sea el mismo que el del usuario
    autenticado (``current_user``).

    Diseñado para usarse dentro de un controlador donde ya se obtuvo el
    ``current_user`` vía ``Depends(get_current_user)``.

    - Si coinciden: devuelve el ``current_user`` para encadenar el flujo.
    - Si no coinciden: lanza HTTP 404 (no 403) para no filtrar la
      existencia del recurso/objetivo.
    """
    if current_user.id != requested_user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El {entity_name} solicitado no existe o no tienes permiso para acceder a él.",
        )
    return current_user


def same_user(
    current_user: User,
    resource_owner_id: int,
    *,
    entity_name: str = "recurso",
) -> bool:
    """
    Compara de forma booleana si un recurso pertenece al usuario autenticado.
    Útil para validaciones de propiedad en servicios o consultas.
    """
    return current_user.id == resource_owner_id
