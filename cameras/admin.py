from django.contrib import admin

from .models import Camera


@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "status",
        "status_em",
        "tipo",
        "ip",
        "mascara_subrede",
        "vlan",
        "fabricante",
        "modelo",
    )

    search_fields = (
        "nome",
        "ip",
        "fabricante",
        "modelo",
    )

    list_filter = (
        "status",
        "tipo",
        "fabricante",
        "vlan",
    )