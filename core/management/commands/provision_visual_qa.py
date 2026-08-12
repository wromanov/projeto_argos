from hashlib import sha256

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


VISUAL_QA_PERMISSION_SPECS = (
    ("cameras", "camera", "view_camera"),
    ("cameras", "camera", "add_camera"),
    ("cameras", "camera", "change_camera"),
    ("cameras", "camera", "desativar_camera"),
    ("cameras", "camera", "reativar_camera"),
    ("cameras", "camera", "alterar_situacao_camera"),
    ("cameras", "camera", "registrar_substituicao_camera"),
    ("cameras", "eventoauditoria", "consultar_eventos"),
    ("cameras", "substituicaocamera", "consultar_substituicoescamera"),
)
VISUAL_QA_MARKER_DOMAIN = "visual-qa.invalid"


class Command(BaseCommand):
    help = "Provisiona a identidade local de QA visual do ARGOS."

    def _configuration(self):
        if not settings.DEBUG:
            raise CommandError(
                "O Visual QA exige DEBUG ativo e não pode ser provisionado fora do desenvolvimento."
            )
        if not settings.VISUAL_QA_ENABLED:
            raise CommandError(
                "ARGOS_VISUAL_QA_ENABLED não está habilitado."
            )

        username = settings.VISUAL_QA_USERNAME.strip()
        if not username:
            raise CommandError(
                "ARGOS_VISUAL_QA_USERNAME deve ser configurado."
            )

        password = settings.VISUAL_QA_PASSWORD
        if not password or not password.strip():
            raise CommandError(
                "ARGOS_VISUAL_QA_PASSWORD deve ser configurado."
            )
        return username, password

    @staticmethod
    def _permissions():
        permissions = []
        for app_label, model, codename in VISUAL_QA_PERMISSION_SPECS:
            try:
                permission = Permission.objects.get(
                    content_type__app_label=app_label,
                    content_type__model=model,
                    codename=codename,
                )
            except Permission.DoesNotExist as error:
                raise CommandError(
                    f"Permissão necessária não encontrada: {app_label}.{codename}."
                ) from error
            permissions.append(permission)
        return permissions

    @staticmethod
    def _identity_marker(username):
        digest = sha256(username.encode("utf-8")).hexdigest()
        return f"argos-visual-qa-{digest}@{VISUAL_QA_MARKER_DOMAIN}"

    @classmethod
    def _is_recognized_identity(cls, user, username):
        return user.email == cls._identity_marker(username)

    @transaction.atomic
    def handle(self, *args, **options):
        username, password = self._configuration()
        permissions = self._permissions()
        user_model = get_user_model()
        try:
            user = user_model.objects.get(username=username)
        except user_model.DoesNotExist:
            user = user_model(username=username)
            created = True
        else:
            created = False
            if not self._is_recognized_identity(user, username):
                raise CommandError(
                    f"Já existe um usuário com o username {username!r}; "
                    "a identidade não foi reconhecida como Visual QA e não foi alterada."
                )

        user.email = self._identity_marker(username)
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        user.set_password(password)
        fields = [
            "email",
            "password",
            "is_active",
            "is_staff",
            "is_superuser",
        ]
        if created:
            user.save()
        else:
            user.save(update_fields=fields)
        user.groups.clear()
        user.user_permissions.set(permissions)

        action = "criado" if created else "atualizado"
        self.stdout.write(
            self.style.SUCCESS(
                f"Usuário Visual QA {action}: {username}."
            )
        )
