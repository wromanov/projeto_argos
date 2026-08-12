from ipaddress import ip_address
from urllib.parse import urlsplit

from django.conf import settings
from django.core.exceptions import DisallowedHost
from django.http import HttpResponseForbidden
from django.urls import Resolver404, resolve
from django.utils.deprecation import MiddlewareMixin


SAFE_METHODS = frozenset({"GET", "HEAD", "OPTIONS"})
LOOPBACK_HOSTNAMES = frozenset({"localhost", "127.0.0.1", "::1"})


class VisualQAMiddleware(MiddlewareMixin):
    """Limits the dedicated local Visual QA identity to read-only requests."""

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not self._is_visual_qa(request):
            return None

        if not self._is_loopback_request(request):
            return HttpResponseForbidden(
                "Visual QA disponível somente em loopback."
            )

        if request.method in SAFE_METHODS or self._is_logout_request(request):
            return None

        return HttpResponseForbidden(
            "A identidade Visual QA é somente leitura."
        )

    @staticmethod
    def _is_visual_qa(request):
        if not settings.DEBUG or not settings.VISUAL_QA_ENABLED:
            return False
        user = getattr(request, "user", None)
        return bool(
            user
            and user.is_authenticated
            and settings.VISUAL_QA_USERNAME
            and user.get_username() == settings.VISUAL_QA_USERNAME
        )

    @classmethod
    def _is_loopback_request(cls, request):
        hostname = cls._request_hostname(request)
        remote_addr = request.META.get("REMOTE_ADDR")
        if hostname not in LOOPBACK_HOSTNAMES or not remote_addr:
            return False

        try:
            remote_ip = ip_address(remote_addr)
        except (TypeError, ValueError):
            return False
        return remote_ip.is_loopback

    @staticmethod
    def _request_hostname(request):
        try:
            host = request.get_host()
        except DisallowedHost:
            return None

        if not host:
            return None

        try:
            parsed = urlsplit(f"//{host}")
            if parsed.username or parsed.password:
                return None
            parsed.port
            hostname = parsed.hostname
        except ValueError:
            return None

        return (hostname or "").rstrip(".").lower() or None

    @staticmethod
    def _is_logout_request(request):
        if request.method != "POST":
            return False
        try:
            match = resolve(request.path_info)
        except Resolver404:
            return False
        return match.view_name == "usuarios:logout"
