"""Fernet key custody boundary for camera credentials.

Keys are delivered outside Django's database and source tree. Tests should
inject an in-memory provider instead of setting process-wide key material.
"""

import json
import os

from cryptography.fernet import Fernet


class CredentialKeyError(Exception):
    """Safe, non-secret-bearing key configuration error."""

    def __init__(self, code):
        self.code = code
        super().__init__(code)


class CredentialKeyProvider:
    """Supplies key versions and the active Fernet key to credential services."""

    def __init__(self, keys=None, active_key_version=None):
        self._keys = dict(keys or {})
        self.active_key_version = active_key_version

    def active_key(self):
        if not self.active_key_version:
            raise CredentialKeyError("KEY_MISSING")
        key = self._keys.get(self.active_key_version)
        if key is None:
            raise CredentialKeyError("KEY_MISSING")
        return self._validated_key(key), self.active_key_version

    def key_for_version(self, version):
        if version not in self._keys:
            raise CredentialKeyError("KEY_VERSION_UNKNOWN")
        return self._validated_key(self._keys[version])

    @staticmethod
    def _validated_key(key):
        try:
            # Instantiate here so malformed material fails before encrypt/decrypt.
            Fernet(key.encode("ascii") if isinstance(key, str) else key)
        except (TypeError, ValueError, UnicodeEncodeError):
            raise CredentialKeyError("KEY_INVALID") from None
        return key.encode("ascii") if isinstance(key, str) else key


def get_environment_key_provider():
    """Build the local provider from externally delivered process secrets."""
    serialized_keys = os.environ.get("ARGOS_CAMERA_CREDENTIAL_KEYS")
    active_version = os.environ.get("ARGOS_CAMERA_CREDENTIAL_ACTIVE_KEY_VERSION")
    if not serialized_keys and not active_version:
        return CredentialKeyProvider()
    try:
        keys = json.loads(serialized_keys or "{}")
    except (TypeError, ValueError):
        raise CredentialKeyError("KEY_INVALID") from None
    if not isinstance(keys, dict) or any(
        not isinstance(version, str) or not isinstance(key, str) for version, key in keys.items()
    ):
        raise CredentialKeyError("KEY_INVALID") from None
    return CredentialKeyProvider(keys=keys, active_key_version=active_version)
