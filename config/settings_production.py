from django.core.exceptions import ImproperlyConfigured
from .environment import get_env_bool, get_env_int, get_env_list, get_required_secret
from .settings import *  # noqa: F403,F401

DEBUG = False
validate_visual_qa_configuration(DEBUG, VISUAL_QA_ENABLED)
SECRET_KEY = get_required_secret("ARGOS_SECRET_KEY", minimum_length=50)
ALLOWED_HOSTS = get_env_list("ARGOS_ALLOWED_HOSTS")
if not ALLOWED_HOSTS: raise ImproperlyConfigured("ARGOS_ALLOWED_HOSTS deve possuir ao menos um host.")
CSRF_TRUSTED_ORIGINS = get_env_list("ARGOS_CSRF_TRUSTED_ORIGINS")
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "Lax"
SECURE_SSL_REDIRECT = get_env_bool("ARGOS_SECURE_SSL_REDIRECT", True)
SECURE_HSTS_SECONDS = get_env_int("ARGOS_SECURE_HSTS_SECONDS", 31536000, minimum=0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = get_env_bool("ARGOS_SECURE_HSTS_INCLUDE_SUBDOMAINS", True)
SECURE_HSTS_PRELOAD = get_env_bool("ARGOS_SECURE_HSTS_PRELOAD", False)
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"
# Ative somente quando um proxy reverso confiável sobrescrever este cabeçalho.
if get_env_bool("ARGOS_TRUST_PROXY_SSL_HEADER", False): SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
