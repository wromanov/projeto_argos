from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = "Configura os perfis e permissões padrão do ARGOS."

    @transaction.atomic
    def handle(self, *args, **options):
        camera_perms = Permission.objects.filter(content_type__app_label="cameras")
        monitoramento = camera_perms.filter(codename__in=("view_camera", "view_atividadecamera"))
        operador = camera_perms.filter(codename__in=("view_camera", "add_camera", "change_camera", "view_atividadecamera", "add_atividadecamera", "change_atividadecamera"))
        administrador = camera_perms.exclude(codename__startswith="delete_") | Permission.objects.filter(content_type__app_label="auth", codename__in=("view_user", "add_user", "change_user", "view_group", "add_group", "change_group", "view_permission"))
        for nome, permissoes in (("Monitoramento ARGOS", monitoramento), ("Operador ARGOS", operador), ("Administrador ARGOS", administrador)):
            grupo, _ = Group.objects.get_or_create(name=nome)
            grupo.permissions.set(permissoes)
        self.stdout.write(self.style.SUCCESS("Perfis ARGOS configurados com sucesso."))
