"""Explicit, no-store HTTP reveal surface for camera credentials."""

from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

from cameras.integracao.credentials import CredentialOperationError, reveal_camera_credential


def _no_store(response):
    response["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    return response


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
