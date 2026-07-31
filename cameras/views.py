from django.shortcuts import get_object_or_404, render

from .models import Camera


def lista_cameras(request):
    cameras = Camera.objects.all()

    contexto = {
        "cameras": cameras,
    }

    return render(request, "cameras/lista.html", contexto)


def detalhe_camera(request, pk):
    camera = get_object_or_404(Camera, pk=pk)

    contexto = {
        "camera": camera,
    }

    return render(
        request,
        "cameras/detalhe.html",
        contexto,
    )
