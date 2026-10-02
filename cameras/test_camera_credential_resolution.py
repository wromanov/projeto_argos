import json
import pickle
from dataclasses import FrozenInstanceError, fields
from unittest.mock import patch

from cryptography.fernet import Fernet
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied
from django.test import TestCase

from cameras.authorization import require_camera_permission
from cameras.integracao.credentials import (
    CredentialOperationError,
    ResolvedCameraCredential,
    replace_camera_credential,
    resolve_active_credential_for_execution,
)
from cameras.integracao.key_provider import CredentialKeyError, CredentialKeyProvider
from cameras.models import (
    Camera,
    CameraCapabilityProfile,
    CameraConnectionConfig,
    CameraCredential,
    CameraCredentialVersion,
    EventoAuditoria,
)


class CameraCredentialResolutionTests(TestCase):
    username = "resolution-device-user"
    password = "resolution-device-password"

    def setUp(self):
        user_model = get_user_model()
        self.actor = user_model.objects.create_user(username="resolution-tech", password="actor-password")
        permission = Permission.objects.get(content_type__app_label="cameras", codename="change_camera_credential")
        self.actor.user_permissions.add(permission)
        self.camera = self._camera("Resolution Camera", "192.0.2.70")
        self.profile = CameraCapabilityProfile.objects.get(profile_key="RTSP_DISCOVERY_V1", version=1)
        self.key_version = "resolution-key-v1"
        self.key = Fernet.generate_key()
        self.provider = CredentialKeyProvider({self.key_version: self.key}, self.key_version)
        self.credential = self._replace()
        self.config = self._config(self.camera, self.credential)

    def _camera(self, name, ip):
        return Camera.objects.create(nome=name, fabricante="Fabricante", modelo="Modelo", ip=ip)

    def _replace(self, *, camera=None, provider=None, username=None, password=None):
        camera = camera or self.camera
        return replace_camera_credential(
            actor=self.actor,
            camera_id=camera.pk,
            username=username or self.username,
            password=password or self.password,
            key_provider=provider or self.provider,
        )

    def _config(self, camera, credential):
        return CameraConnectionConfig.objects.create(
            camera=camera,
            profile=self.profile,
            credential=credential,
            enabled=True,
        )

    def _resolve(self, provider=None, config=None):
        with patch(
            "cameras.integracao.credentials.get_environment_key_provider",
            return_value=provider or self.provider,
        ):
            return resolve_active_credential_for_execution(config=config or self.config)

    def _assert_code(self, code, *, config=None, provider=None):
        with self.assertRaises(CredentialOperationError) as raised:
            self._resolve(provider=provider, config=config)
        self.assertEqual(raised.exception.code, code)
        self.assertEqual(str(raised.exception), code)
        return raised.exception

    def test_resolves_only_active_secret_as_frozen_sanitized_value_object(self):
        audit_count = EventoAuditoria.objects.count()
        credential_state = self.credential.state
        version_ciphertext = self.credential.active_version.ciphertext

        result = self._resolve()

        self.assertIsInstance(result, ResolvedCameraCredential)
        self.assertEqual((result.username, result.password), (self.username, self.password))
        self.assertEqual({field.name for field in fields(result)}, {"username", "password"})
        self.assertNotIn(self.password, repr(result))
        self.assertNotIn(self.username, repr(result))
        self.assertNotIn(self.password, str(result))
        self.assertNotIn(self.username, str(result))
        self.assertNotIn("ciphertext", vars(result))
        self.assertNotIn("provider", vars(result))
        with self.assertRaises(FrozenInstanceError):
            result.password = "changed"
        with self.assertRaises(TypeError):
            json.dumps(result)
        with self.assertRaisesRegex(TypeError, "cannot be serialized"):
            pickle.dumps(result)
        self.credential.refresh_from_db()
        self.assertEqual(self.credential.state, credential_state)
        self.assertEqual(self.credential.active_version.ciphertext, version_ciphertext)
        self.assertEqual(EventoAuditoria.objects.count(), audit_count)

    def test_rtsp_and_http_consumer_fakes_share_api_without_crypto_access(self):
        def fake_port(resolved_credential):
            self.assertIsInstance(resolved_credential, ResolvedCameraCredential)
            self.assertEqual(resolved_credential.username, self.username)
            self.assertEqual(resolved_credential.password, self.password)
            return "accepted"

        # Neither future consumer requires a Django User or a crypto helper.
        for consumer_kind in ("rtsp", "http_snapshot"):
            with self.subTest(consumer_kind=consumer_kind):
                result = self._resolve()
                self.assertEqual(fake_port(result), "accepted")
                self.assertFalse(hasattr(result, "ciphertext"))
                self.assertFalse(hasattr(result, "key_provider"))

    def test_manual_use_case_permission_denial_happens_before_resolution(self):
        for permission in ("run_camera_connection_test", "capture_camera_image"):
            with self.subTest(permission=permission), patch(
                "cameras.integracao.credentials.resolve_active_credential_for_execution"
            ) as resolver:
                with self.assertRaises(PermissionDenied):
                    require_camera_permission(
                        actor=self.actor,
                        permission_codename=permission,
                        camera_id=self.camera.pk,
                    )
                resolver.assert_not_called()

    def test_config_must_be_persisted_current_and_unmodified(self):
        unsaved = CameraConnectionConfig(camera=self.camera, profile=self.profile, credential=self.credential)
        self._assert_code("CONFIGURATION_NOT_ALLOWED", config=unsaved)

        changed_input = CameraConnectionConfig.objects.get(pk=self.config.pk)
        changed_input.enabled = False
        self._assert_code("CONFIGURATION_NOT_ALLOWED", config=changed_input)

        CameraConnectionConfig.objects.filter(pk=self.config.pk).update(config_version=2)
        self._assert_code("CONFIGURATION_NOT_ALLOWED")

    def test_missing_configured_credential_fails_closed(self):
        CameraConnectionConfig.objects.filter(pk=self.config.pk).update(credential=None)
        self.config.refresh_from_db()
        self._assert_code("CREDENTIAL_NOT_CONFIGURED", config=self.config)

    def test_credential_for_another_camera_fails_closed(self):
        other_camera = self._camera("Other Camera", "192.0.2.71")
        other_credential = self._replace(camera=other_camera)
        CameraConnectionConfig.objects.filter(pk=self.config.pk).update(credential=other_credential)
        self.config.refresh_from_db()
        self._assert_code("CROSS_CAMERA_REFERENCE", config=self.config)

    def test_inactive_owner_and_missing_active_pointer_fail_closed(self):
        CameraCredential.objects.filter(pk=self.credential.pk).update(state=CameraCredential.State.INACTIVE)
        self._assert_code("VERSION_NOT_ALLOWED")

        CameraCredential.objects.filter(pk=self.credential.pk).update(
            state=CameraCredential.State.ACTIVE,
            active_version=None,
        )
        self._assert_code("NO_ACTIVE_VERSION")

    def test_retired_revoked_and_inconsistent_active_pointer_are_rejected(self):
        version = self.credential.active_version
        for state in (CameraCredentialVersion.State.RETIRED, CameraCredentialVersion.State.REVOKED):
            with self.subTest(state=state):
                CameraCredentialVersion.objects.filter(pk=version.pk).update(state=state)
                self._assert_code("VERSION_NOT_ALLOWED")
                CameraCredentialVersion.objects.filter(pk=version.pk).update(
                    state=CameraCredentialVersion.State.ACTIVE
                )

        self._replace(username="new-user", password="new-password")
        first_version = self.credential.versions.order_by("version").first()
        CameraCredential.objects.filter(pk=self.credential.pk).update(active_version=first_version)
        self._assert_code("VERSION_NOT_ALLOWED")

    def test_active_pointer_only_no_fallback_to_decryptable_retired_version(self):
        first_key = self.key
        second_key = Fernet.generate_key()
        second_provider = CredentialKeyProvider(
            {self.key_version: first_key, "resolution-key-v2": second_key},
            "resolution-key-v2",
        )
        self._replace(username="rotated-user", password="rotated-password", provider=second_provider)
        old_only_provider = CredentialKeyProvider({self.key_version: first_key}, self.key_version)

        self._assert_code("KEY_VERSION_UNKNOWN", provider=old_only_provider)

    def test_key_provider_failures_are_sanitized_and_fail_closed(self):
        # An empty published provider has the factual KEY_VERSION_UNKNOWN
        # behavior; a provider-level missing-material response maps to the
        # separate KEY_MISSING contract code.
        self._assert_code("KEY_VERSION_UNKNOWN", provider=CredentialKeyProvider())
        self._assert_code(
            "KEY_VERSION_UNKNOWN",
            provider=CredentialKeyProvider({}, self.key_version),
        )
        invalid = CredentialKeyProvider({self.key_version: "invalid-key"}, self.key_version)
        self._assert_code("KEY_INVALID", provider=invalid)

        class MissingMaterialProvider:
            def key_for_version(self, version):
                raise CredentialKeyError("KEY_MISSING")

        self._assert_code("KEY_MISSING", provider=MissingMaterialProvider())
        with patch(
            "cameras.integracao.credentials.get_environment_key_provider",
            side_effect=CredentialKeyError("KEY_MISSING"),
        ):
            with self.assertRaises(CredentialOperationError) as raised:
                resolve_active_credential_for_execution(config=self.config)
        self.assertEqual(raised.exception.code, "KEY_MISSING")

    def test_tampered_active_payload_fails_without_returning_ciphertext_or_plaintext(self):
        CameraCredentialVersion.objects.filter(pk=self.credential.active_version_id).update(
            ciphertext="not-valid-ciphertext"
        )
        error = self._assert_code("DECRYPT_FAILED")
        self.assertNotIn(self.password, str(error))
        self.assertNotIn("not-valid-ciphertext", str(error))

    def test_resolution_never_invokes_human_reveal_or_creates_reveal_audit(self):
        with patch("cameras.integracao.credentials.authenticate") as authenticate:
            self._resolve()
        authenticate.assert_not_called()
        self.assertFalse(
            EventoAuditoria.objects.filter(
                camera=self.camera,
                codigo="camera.credential.revealed",
            ).exists()
        )
