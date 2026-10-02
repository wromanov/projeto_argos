"""Guards de autorização para operações futuras sobre câmeras."""

from django.core.exceptions import PermissionDenied


CAMERA_AUTHORIZATION_PERMISSIONS = frozenset(
    {
        "view_camera_connection",
        "change_camera_connection",
        "manage_camera_capability",
        "view_camera_credential",
        "change_camera_credential",
        "reveal_camera_credential",
        "run_camera_connection_test",
        "view_camera_diagnostic",
        "capture_camera_image",
        "manage_camera_target_policy",
        "manage_monitoring_runtime",
    }
)


def require_camera_permission(*, actor, permission_codename, camera_id):
    """Exige uma permissão contratada antes de um serviço operar uma câmera.

    ``camera_id`` é obrigatório para que cada consumidor autorize a operação
    no contexto do recurso que pretende acessar. O baseline Django atual
    configura permissões por modelo, sem escopo de objeto/tenant.
    """

    if permission_codename not in CAMERA_AUTHORIZATION_PERMISSIONS:
        raise ValueError("Permissão de câmera não consta no contrato BC-AUTH.")
    if camera_id is None:
        raise ValueError("camera_id é obrigatório para autorizar a operação.")
    if not getattr(actor, "is_authenticated", False) or not actor.has_perm(
        f"cameras.{permission_codename}"
    ):
        raise PermissionDenied
