"""Regras de segurança para a administração de usuários no Django Admin."""


ARGOS_ADMIN_GROUP_NAME = "Administrador ARGOS"
ARGOS_OPERATIONAL_GROUP_NAMES = (
    "Monitoramento ARGOS",
    "Operador ARGOS",
    "Técnico ARGOS",
)


def is_argos_admin(actor):
    """Retorna se o ator é um administrador operacional do ARGOS."""

    return bool(
        getattr(actor, "is_authenticated", False)
        and actor.groups.filter(name=ARGOS_ADMIN_GROUP_NAME).exists()
    )


def is_protected_user(target):
    """Classifica contas que não podem ser administradas pelo perfil ARGOS."""

    if not getattr(target, "pk", None):
        return True

    return bool(
        target.is_superuser
        or target.is_staff
        or target.user_permissions.exists()
        or target.groups.exclude(name__in=ARGOS_OPERATIONAL_GROUP_NAMES).exists()
    )


def can_manage_user(actor, target):
    """Aplica a política conservadora de administração de usuários."""

    if getattr(actor, "is_superuser", False):
        return True

    if not is_argos_admin(actor):
        return False

    if not target or actor.pk == target.pk:
        return False

    return not is_protected_user(target)
