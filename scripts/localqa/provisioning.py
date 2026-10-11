"""Provisionamento limitado às identidades do banco local de QA."""

from hashlib import sha256

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import ImproperlyConfigured
from django.db import transaction


VISUAL_QA_PERMISSIONS = frozenset(
    {
        "view_camera",
        "add_camera",
        "change_camera",
        "consultar_eventos",
        "consultar_substituicoescamera",
    }
)
OPERATIONAL_QA_PERMISSIONS = VISUAL_QA_PERMISSIONS | frozenset(
    {"add_cameraimagerecord", "add_atividadecamera"}
)
OPERATIONAL_QA_USERNAME = "qa-operacional-hom01"


def identity_marker(username, role):
    digest = sha256(username.encode("utf-8")).hexdigest()
    return f"argos-{role}-qa-{digest}@visual-qa.invalid"


def _user_permissions(user):
    return frozenset(user.user_permissions.values_list("codename", flat=True))


def preflight_operational_qa_user(username=OPERATIONAL_QA_USERNAME):
    """Check ownership and required permissions before seeding other QA data."""
    user = get_user_model().objects.filter(username=username).first()
    if user is not None and user.email != identity_marker(username, "operational"):
        raise ImproperlyConfigured(
            f"O usuário {username!r} já existe sem marcador do seed local; nenhuma alteração foi feita."
        )
    permission_objects = Permission.objects.filter(
        content_type__app_label="cameras",
        codename__in=OPERATIONAL_QA_PERMISSIONS,
    )
    if permission_objects.count() != len(OPERATIONAL_QA_PERMISSIONS):
        raise ImproperlyConfigured("Uma ou mais permissões do perfil QA operacional não existem.")
    return user


def validate_visual_qa_user():
    """Validate the existing visual account without writing to it."""
    user_model = get_user_model()
    username = settings.VISUAL_QA_USERNAME
    try:
        user = user_model.objects.get(username=username)
    except user_model.DoesNotExist as error:
        raise ImproperlyConfigured(
            "A conta visual QA esperada não existe; ela não será criada nem alterada nesta atividade."
        ) from error

    if user.email != identity_marker(username, "visual"):
        raise ImproperlyConfigured(
            "A conta visual QA não tem o marcador reconhecido; ela foi preservada sem alterações."
        )
    if (
        not user.is_active
        or user.is_staff
        or user.is_superuser
        or user.groups.exists()
        or _user_permissions(user) != VISUAL_QA_PERMISSIONS
    ):
        raise ImproperlyConfigured(
            "A conta visual QA não corresponde às permissões esperadas; ela foi preservada sem alterações."
        )
    return user


@transaction.atomic
def provision_operational_qa_user(password, username=OPERATIONAL_QA_USERNAME):
    if not password or len(password) < 24:
        raise ImproperlyConfigured("A senha operacional QA deve ser aleatória e ter ao menos 24 caracteres.")

    user_model = get_user_model()
    marker = identity_marker(username, "operational")
    user = preflight_operational_qa_user(username)
    if user is None:
        user = user_model(username=username, email=marker)
        created = True
    else:
        created = False
    permission_objects = Permission.objects.filter(
        content_type__app_label="cameras",
        codename__in=OPERATIONAL_QA_PERMISSIONS,
    )

    user.email = marker
    user.is_active = True
    user.is_staff = False
    user.is_superuser = False
    user.set_password(password)
    if created:
        user.save()
    else:
        user.save(
            update_fields=("email", "is_active", "is_staff", "is_superuser", "password")
        )
    user.groups.clear()
    user.user_permissions.set(permission_objects)
    if _user_permissions(user) != OPERATIONAL_QA_PERMISSIONS:
        raise ImproperlyConfigured("As permissões do usuário QA operacional não foram reconciliadas exatamente.")
    return user, created
