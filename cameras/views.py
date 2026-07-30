from django.shortcuts import render

from .models import Camera


def lista_cameras(request):
    cameras = Camera.objects.all()

    contexto = {
        "cameras": cameras,
    }

    return render(request, "cameras/lista.html", contexto, )
