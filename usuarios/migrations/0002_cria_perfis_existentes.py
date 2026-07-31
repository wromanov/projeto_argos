from django.conf import settings
from django.db import migrations


def criar_perfis_existentes(apps, schema_editor):
    app_label, model_name = settings.AUTH_USER_MODEL.split(".")
    User = apps.get_model(app_label, model_name)
    PerfilUsuario = apps.get_model("usuarios", "PerfilUsuario")
    usuarios_com_perfil = set(PerfilUsuario.objects.values_list("usuario_id", flat=True))
    perfis = [PerfilUsuario(usuario_id=usuario.pk) for usuario in User.objects.all() if usuario.pk not in usuarios_com_perfil]
    PerfilUsuario.objects.bulk_create(perfis, ignore_conflicts=True)


class Migration(migrations.Migration):
    dependencies = [("usuarios", "0001_initial")]
    operations = [migrations.RunPython(criar_perfis_existentes, reverse_code=migrations.RunPython.noop)]
