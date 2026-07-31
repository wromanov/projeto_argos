from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cameras/", include("cameras.urls")),
    path("eventos/", include("cameras.urls_eventos")),
    path("", include("usuarios.urls")),
    path("", include("core.urls")),
]
