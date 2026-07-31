from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CameraForm
from .models import Camera


def lista_cameras(request):
    cameras = Camera.objects.all()

    contexto = {
        "cameras": cameras,
    }

    return render(request, "cameras/lista.html", contexto)


def criar_camera(request):
    if request.method == "POST":
        form = CameraForm(request.POST)
        if form.is_valid():
            camera = form.save(commit=False)
            if request.user.is_authenticated:
                camera.criado_por = request.user
                camera.atualizado_por = request.user
            camera.save()
            messages.success(request, "Câmera cadastrada com sucesso.")
            return redirect("cameras:detalhe", pk=camera.pk)
    else:
        form = CameraForm()

    contexto = {
        "form": form,
        "titulo_pagina": "Nova câmera",
    }

    return render(request, "cameras/formulario.html", contexto)


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
