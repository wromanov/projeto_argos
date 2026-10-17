"""Explicit, no-store HTTP surfaces for camera credential operations."""

import logging

from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

from cameras.authorization import require_camera_permission
from cameras.credential_forms import CameraCredentialReplaceForm
from cameras.integracao.credentials import (
    CredentialOperationError,
    replace_camera_credential,
    reveal_camera_credential,
    revoke_camera_credential,
)
from cameras.models import Camera


logger = logging.getLogger(__name__)


def _no_store(response):
    response["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    return response


def _safe_error(status, message):
    response = HttpResponse(message, status=status, content_type="text/plain; charset=utf-8")
    return _no_store(response)


def _authorized_camera(request, camera_id):
    require_camera_permission(
        actor=request.user,
        permission_codename="change_camera_credential",
        camera_id=camera_id,
    )
    return get_object_or_404(Camera, pk=camera_id)


@never_cache
@require_POST
@csrf_protect
def replace_camera_credential_view(request, camera_id):
    try:
        camera = _authorized_camera(request, camera_id)
        form = CameraCredentialReplaceForm(request.POST)
        allowed = {"username", "password", "confirm_unsaved_changes", "csrfmiddlewaretoken"}
        if set(request.POST.keys()) - allowed:
            return _safe_error(400, "Dados inválidos para configurar a credencial.")
        if any(len(request.POST.getlist(key)) != 1 for key in ("username", "password", "confirm_unsaved_changes")):
            return _safe_error(400, "Dados inválidos para configurar a credencial.")
        if request.POST.get("confirm_unsaved_changes") != "1":
            return _safe_error(400, "Confirme como deseja tratar alterações cadastrais não salvas.")
        if not form.is_valid():
            return _safe_error(400, "Informe usuário e senha válidos para a credencial.")
        replace_camera_credential(
            actor=request.user,
            camera_id=camera.pk,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
            request=request,
        )
    except PermissionDenied:
        return _safe_error(403, "Acesso não autorizado.")
    except ValidationError:
        return _safe_error(400, "Informe usuário e senha válidos para a credencial.")
    except Http404:
        return _safe_error(404, "Câmera não encontrada.")
    except CredentialOperationError as exc:
        if exc.code in {"KEY_MISSING", "KEY_INVALID", "KEY_VERSION_UNKNOWN", "DECRYPT_FAILED"}:
            return _safe_error(503, "O serviço de credenciais está indisponível.")
        return _safe_error(409, "Não foi possível concluir a alteração da credencial.")
    except Exception:
        # Do not log the exception: request and form locals can contain secrets.
        logger.error("Falha inesperada ao substituir credencial de câmera.")
        return _safe_error(500, "Não foi possível concluir a operação.")
    messages.success(request, "Credencial atualizada.")
    return _no_store(redirect("cameras:editar", pk=camera.pk))


@never_cache
@require_POST
@csrf_protect
def revoke_camera_credential_view(request, camera_id):
    try:
        camera = _authorized_camera(request, camera_id)
        allowed = {"csrfmiddlewaretoken", "confirm_unsaved_changes"}
        if set(request.POST.keys()) - allowed:
            return _safe_error(400, "Dados inválidos para revogar a credencial.")
        # In the no-JavaScript SSR fallback this required confirmation records
        # the user's explicit decision about any independent camera edits.
        if request.POST.getlist("confirm_unsaved_changes") != ["1"]:
            return _safe_error(400, "Confirme como deseja tratar alterações cadastrais não salvas.")
        revoke_camera_credential(actor=request.user, camera_id=camera.pk, request=request)
    except PermissionDenied:
        return _safe_error(403, "Acesso não autorizado.")
    except Http404:
        return _safe_error(404, "Câmera não encontrada.")
    except CredentialOperationError as exc:
        if exc.code == "CREDENTIAL_NOT_CONFIGURED":
            return _safe_error(409, "O estado da credencial mudou. Atualize a página.")
        if exc.code in {"KEY_MISSING", "KEY_INVALID", "KEY_VERSION_UNKNOWN", "DECRYPT_FAILED"}:
            return _safe_error(503, "O serviço de credenciais está indisponível.")
        return _safe_error(409, "Não foi possível concluir a revogação da credencial.")
    except Exception:
        logger.error("Falha inesperada ao revogar credencial de câmera.")
        return _safe_error(500, "Não foi possível concluir a operação.")
    messages.success(request, "Credencial revogada.")
    return _no_store(redirect("cameras:editar", pk=camera.pk))


@never_cache
@require_POST
@csrf_protect
def reveal_camera_credential_view(request, camera_id):
    """Reauthenticate this request and return a credential only on explicit reveal."""
    if not getattr(request.user, "is_authenticated", False):
        return _no_store(JsonResponse({"error": "PERMISSION_DENIED"}, status=403))
    try:
        result = reveal_camera_credential(
            actor=request.user,
            camera_id=camera_id,
            current_password=request.POST.get("current_password", ""),
            request=request,
        )
    except PermissionDenied:
        response = JsonResponse({"error": "PERMISSION_DENIED"}, status=403)
    except CredentialOperationError as exc:
        status = 404 if exc.code == "CREDENTIAL_NOT_CONFIGURED" else (403 if exc.code == "REAUTHENTICATION_FAILED" else 400)
        response = JsonResponse({"error": exc.code}, status=status)
    else:
        response = JsonResponse(result)
    return _no_store(response)
