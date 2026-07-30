from django.contrib import admin

from .models import Camera


@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "ip",
        "mascara_subrede",
        "vlan",
        "fabricante",
        "modelo",
        "tipo",
    )

    search_fields = (
        "nome",
        "ip",
        "fabricante",
        "modelo",
    )

    list_filter = (
        "tipo",
        "fabricante",
        "vlan",
    )