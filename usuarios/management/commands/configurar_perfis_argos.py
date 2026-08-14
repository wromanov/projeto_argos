from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.db import transaction

from usuarios.admin_security import (
    ARGOS_ADMIN_GROUP_NAME,
    ARGOS_OPERATIONAL_GROUP_NAMES,
)


class Command(BaseCommand):
    help = "Configura os perfis e permissões padrão do ARGOS."

    @transaction.atomic
    def handle(self, *args, **options):
        camera_perms = Permission.objects.filter(content_type__app_label="cameras")
        consulta = ("view_camera", "view_atividadecamera", "view_eventoauditoria", "consultar_eventos", "view_substituicaocamera", "consultar_substituicoescamera")
        operacionais = consulta + ("add_camera", "change_camera", "add_atividadecamera", "change_atividadecamera", "desativar_camera", "reativar_camera", "alterar_situacao_camera", "registrar_substituicao_camera")
        monitoramento = camera_perms.filter(codename__in=consulta)
        operador = camera_perms.filter(codename__in=operacionais)
        administrador = camera_perms.exclude(codename__startswith="delete_").exclude(codename__in=("add_eventoauditoria", "change_eventoauditoria", "add_substituicaocamera", "change_substituicaocamera"))
        administrador = administrador | Permission.objects.filter(
            content_type__app_label="auth",
            codename__in=("view_user", "add_user", "change_user"),
        ) | Permission.objects.filter(
            content_type__app_label="usuarios",
            codename__in=("view_perfilusuario", "change_perfilusuario"),
        )
        perfis = (
            (ARGOS_OPERATIONAL_GROUP_NAMES[0], monitoramento),
            (ARGOS_OPERATIONAL_GROUP_NAMES[1], operador),
            (ARGOS_ADMIN_GROUP_NAME, administrador),
        )
        for nome, permissoes in perfis:
            grupo, _ = Group.objects.get_or_create(name=nome)
            grupo.permissions.set(permissoes)
        self.stdout.write(self.style.SUCCESS("Perfis ARGOS configurados com sucesso."))
