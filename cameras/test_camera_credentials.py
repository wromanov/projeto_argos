import json
import logging
from unittest.mock import patch

from cryptography.fernet import Fernet
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Permission
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import HttpRequest
from django.test import Client, TestCase
from django.urls import reverse
from django.middleware.csrf import get_token

from cameras.integracao.configuration import save_connection_config
from cameras.integracao.credentials import (
    CredentialOperationError,
    credential_metadata,
    replace_camera_credential,
    reveal_camera_credential,
    revoke_camera_credential,
    rotate_camera_credential_key,
)
from cameras.integracao.key_provider import CredentialKeyProvider
from cameras.models import (
    Camera,
    CameraCapabilityProfile,
    CameraConnectionConfig,
    CameraCredential,
    CameraCredentialVersion,
    EventoAuditoria,
)


class CameraCredentialTests(TestCase):
    camera_password = "device-password-never-audit"
    camera_username = "device-username-never-audit"

    def setUp(self):
        user_model = get_user_model()
        self.technician = user_model.objects.create_user(username="credential-tech", password="actor-password")
        self.operator = user_model.objects.create_user(username="credential-operator", password="actor-password")
        self.monitor = user_model.objects.create_user(username="credential-monitor", password="actor-password")
        self.admin = user_model.objects.create_user(username="credential-admin", password="actor-password")
        permission_model = Permission.objects
        for user, codenames in (
            (self.technician, ("change_camera_credential", "view_camera_credential", "reveal_camera_credential", "change_camera_connection")),
            (self.operator, ("view_camera",)),
            (self.monitor, ("view_camera",)),
            (self.admin, ("change_camera_credential", "view_camera_credential", "reveal_camera_credential", "change_camera_connection")),
        ):
            user.user_permissions.add(*permission_model.filter(content_type__app_label="cameras", codename__in=codenames))
        self.camera = Camera.objects.create(
            nome="Credential Camera",
            fabricante="Fabricante",
            modelo="Modelo",
            ip="192.0.2.44",
        )
        self.key_version = "test-2026-01"
        self.key = Fernet.generate_key()
        self.provider = CredentialKeyProvider({self.key_version: self.key}, self.key_version)

    def replace(self, *, actor=None, username=None, password=None, provider=None):
        return replace_camera_credential(
            actor=actor or self.technician,
            camera_id=self.camera.pk,
            username=username or self.camera_username,
            password=password or self.camera_password,
            key_provider=provider or self.provider,
        )

    def test_creation_encrypts_both_fields_and_reveal_returns_only_on_explicit_call(self):
        credential = self.replace()
        version = credential.active_version
        version.refresh_from_db()
        self.assertEqual(version.state, CameraCredentialVersion.State.ACTIVE)
        self.assertEqual(version.key_version, self.key_version)
        self.assertNotIn(self.camera_password, version.ciphertext)
        self.assertNotIn(self.camera_username, version.ciphertext)
        self.assertEqual(
            reveal_camera_credential(
                actor=self.technician,
                camera_id=self.camera.pk,
                current_password="actor-password",
                key_provider=self.provider,
            ),
            {"username": self.camera_username, "password": self.camera_password, "version": 1},
        )

    def test_audit_and_normal_metadata_never_contain_camera_secret(self):
        self.replace()
        events = EventoAuditoria.objects.filter(camera=self.camera)
        self.assertEqual(events.count(), 1)
        serialized_events = json.dumps(list(events.values()), default=str)
        self.assertNotIn(self.camera_password, serialized_events)
        self.assertNotIn(self.camera_username, serialized_events)
        metadata = credential_metadata(actor=self.technician, camera_id=self.camera.pk, key_provider=self.provider)
        self.assertEqual(metadata["username"], self.camera_username)
        self.assertNotIn("password", metadata)
        self.assertNotIn("ciphertext", metadata)

    def test_unauthorized_roles_cannot_view_change_or_reveal(self):
        self.replace()
        for actor in (self.operator, self.monitor, AnonymousUser()):
            with self.subTest(actor=actor), self.assertRaises(PermissionDenied):
                credential_metadata(actor=actor, camera_id=self.camera.pk, key_provider=self.provider)
            with self.subTest(actor=actor), self.assertRaises(PermissionDenied):
                reveal_camera_credential(
                    actor=actor,
                    camera_id=self.camera.pk,
                    current_password="actor-password",
                    key_provider=self.provider,
                )
        for actor in (self.operator, self.monitor, AnonymousUser()):
            with self.subTest(actor=actor), self.assertRaises(PermissionDenied):
                self.replace(actor=actor, username="denied-user", password="denied-secret")

    def test_administrator_can_change_and_reveal(self):
        self.replace(actor=self.admin)
        result = reveal_camera_credential(
            actor=self.admin,
            camera_id=self.camera.pk,
            current_password="actor-password",
            key_provider=self.provider,
        )
        self.assertEqual(result["password"], self.camera_password)

    def test_replacement_is_atomic_and_keeps_only_one_active_version(self):
        self.replace()
        self.replace(username="new-camera-user", password="new-camera-password")
        credential = CameraCredential.objects.get(camera=self.camera)
        versions = list(credential.versions.order_by("version"))
        self.assertEqual([(v.version, v.state) for v in versions], [(1, "RETIRED"), (2, "ACTIVE")])
        self.assertEqual(credential.active_version_id, versions[1].pk)
        self.assertEqual(credential.versions.filter(state="ACTIVE").count(), 1)
        audit = json.dumps(list(EventoAuditoria.objects.filter(camera=self.camera).values()), default=str)
        for value in (self.camera_password, self.camera_username, "new-camera-password", "new-camera-user"):
            self.assertNotIn(value, audit)

    def test_missing_or_invalid_key_fails_closed_without_replacing_active_secret(self):
        credential = self.replace()
        prior = credential.active_version_id
        missing = CredentialKeyProvider()
        with self.assertRaisesRegex(CredentialOperationError, "KEY_MISSING"):
            self.replace(username="replacement", password="replacement-secret", provider=missing)
        invalid = CredentialKeyProvider({self.key_version: "bad-key"}, self.key_version)
        with self.assertRaisesRegex(CredentialOperationError, "KEY_INVALID"):
            self.replace(username="replacement", password="replacement-secret", provider=invalid)
        credential.refresh_from_db()
        self.assertEqual(credential.active_version_id, prior)
        self.assertEqual(credential.versions.count(), 1)

    def test_errors_and_captured_logs_do_not_contain_secret_values(self):
        handler = logging.Handler()
        messages = []
        handler.emit = lambda record: messages.append(record.getMessage())
        root_logger = logging.getLogger()
        root_logger.addHandler(handler)
        try:
            with self.assertRaises(CredentialOperationError) as raised:
                self.replace(provider=CredentialKeyProvider())
        finally:
            root_logger.removeHandler(handler)
        self.assertEqual(str(raised.exception), "KEY_MISSING")
        captured = "\n".join(messages)
        self.assertNotIn(self.camera_password, captured)
        self.assertNotIn(self.camera_username, captured)
        self.assertNotIn(self.camera_password, str(raised.exception))
        self.assertNotIn(self.camera_username, str(raised.exception))

    def test_unknown_key_version_and_tampered_ciphertext_fail_closed(self):
        credential = self.replace()
        version = credential.active_version
        with self.assertRaisesRegex(CredentialOperationError, "KEY_VERSION_UNKNOWN"):
            reveal_camera_credential(
                actor=self.technician,
                camera_id=self.camera.pk,
                current_password="actor-password",
                key_provider=CredentialKeyProvider({}, self.key_version),
            )
        CameraCredentialVersion.objects.filter(pk=version.pk).update(ciphertext="not-a-valid-fernet-token")
        with self.assertRaisesRegex(CredentialOperationError, "DECRYPT_FAILED"):
            reveal_camera_credential(
                actor=self.technician,
                camera_id=self.camera.pk,
                current_password="actor-password",
                key_provider=self.provider,
            )
        events = json.dumps(list(EventoAuditoria.objects.filter(camera=self.camera).values()), default=str)
        self.assertNotIn(self.camera_password, events)

    def test_reveal_reauthenticates_each_request_and_returns_no_store_response(self):
        self.replace()
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.technician)
        url = reverse("cameras:reveal_camera_credential", args=[self.camera.pk])
        response = client.post(url, {"current_password": "wrong-password"})
        self.assertEqual(response.status_code, 403)
        csrf_request = HttpRequest()
        csrf_request.META["SERVER_NAME"] = "testserver"
        csrf_token = get_token(csrf_request)
        client.cookies["csrftoken"] = csrf_request.META["CSRF_COOKIE"]
        with patch("cameras.integracao.credentials.get_environment_key_provider", return_value=self.provider):
            response = client.post(
                url,
                {"current_password": "wrong-password"},
                HTTP_X_CSRFTOKEN=csrf_token,
            )
        self.assertEqual(response.status_code, 403)
        self.assertIn("no-store", response["Cache-Control"])
        with patch("cameras.integracao.credentials.get_environment_key_provider", return_value=self.provider):
            response = client.post(
                url,
                {"current_password": "actor-password"},
                HTTP_X_CSRFTOKEN=csrf_token,
            )
        self.assertEqual(response.status_code, 200)
        self.assertIn("no-store", response["Cache-Control"])
        self.assertEqual(response.json()["password"], self.camera_password)
        self.assertNotIn(self.camera_password, response.wsgi_request.get_full_path())
        self.assertEqual(client.get(url).status_code, 405)
        outcomes = list(
            EventoAuditoria.objects.filter(camera=self.camera, codigo="camera.credential.revealed")
            .values_list("metadados__outcome", flat=True)
        )
        self.assertCountEqual(outcomes, ["REAUTHENTICATION_FAILED", "success"])

    def test_revoke_preserves_config_reference_but_fails_closed_without_active_version(self):
        credential = self.replace()
        profile = CameraCapabilityProfile.objects.get(profile_key="RTSP_DISCOVERY_V1", version=1)
        config = save_connection_config(
            actor=self.technician,
            camera_id=self.camera.pk,
            values={"profile": profile, "enabled": False, "credential_id": credential.pk},
            environment_allowed_ports={554},
        )
        revoke_camera_credential(actor=self.technician, camera_id=self.camera.pk)
        credential.refresh_from_db()
        config.refresh_from_db()
        self.assertIsNone(credential.active_version_id)
        self.assertEqual(credential.state, CameraCredential.State.INACTIVE)
        self.assertEqual(config.credential_id, credential.pk)
        self.assertEqual(credential.versions.get().state, CameraCredentialVersion.State.REVOKED)
        CameraCapabilityProfile.objects.filter(pk=profile.pk).update(credential_required=True)
        profile.refresh_from_db()
        config.enabled = True
        from cameras.integracao.configuration import validate_connection_config

        with self.assertRaises(ValidationError):
            validate_connection_config(config, environment_allowed_ports={554})
        with self.assertRaises(CredentialOperationError):
            reveal_camera_credential(
                actor=self.technician,
                camera_id=self.camera.pk,
                current_password="actor-password",
                key_provider=self.provider,
            )

    def test_normal_connection_resolution_never_returns_credential_material(self):
        from cameras.integracao.configuration import resolve_connection_config

        credential = self.replace()
        profile = CameraCapabilityProfile.objects.get(profile_key="RTSP_DISCOVERY_V1", version=1)
        save_connection_config(
            actor=self.technician,
            camera_id=self.camera.pk,
            values={"profile": profile, "enabled": True, "credential_id": credential.pk},
            environment_allowed_ports={554},
        )
        result = resolve_connection_config(camera_id=self.camera.pk, environment_allowed_ports={554})
        serialized = json.dumps(result, default=str)
        self.assertNotIn(self.camera_password, serialized)
        self.assertNotIn(self.camera_username, serialized)
        self.assertNotIn("ciphertext", result)
        self.assertNotIn("password", result)

    def test_key_rotation_reencrypts_every_version_with_the_new_active_key(self):
        credential = self.replace()
        self.replace(username="second-camera-user", password="second-camera-password")
        old_values = list(credential.versions.order_by("version").values_list("ciphertext", flat=True))
        new_version = "test-2026-02"
        new_key = Fernet.generate_key()
        rotated_provider = CredentialKeyProvider(
            {self.key_version: self.key, new_version: new_key},
            new_version,
        )
        rotate_camera_credential_key(
            actor=self.technician,
            camera_id=self.camera.pk,
            key_provider=rotated_provider,
        )
        versions = list(credential.versions.order_by("version"))
        self.assertTrue(all(version.key_version == new_version for version in versions))
        self.assertTrue(all(version.ciphertext != old for version, old in zip(versions, old_values)))
        revealed = reveal_camera_credential(
            actor=self.technician,
            camera_id=self.camera.pk,
            current_password="actor-password",
            key_provider=rotated_provider,
        )
        self.assertEqual(revealed["password"], "second-camera-password")

    def test_required_credential_must_be_active_and_same_camera(self):
        other = Camera.objects.create(nome="Other Camera", fabricante="F", modelo="M", ip="192.0.2.45")
        credential = self.replace()
        profile = CameraCapabilityProfile.objects.get(profile_key="RTSP_DISCOVERY_V1", version=1)
        CameraCapabilityProfile.objects.filter(pk=profile.pk).update(credential_required=True)
        profile.refresh_from_db()
        config = CameraConnectionConfig(camera=self.camera, profile=profile, enabled=True)
        config.credential = credential
        from cameras.integracao.configuration import validate_connection_config

        validate_connection_config(config, environment_allowed_ports={554})
        config.camera = other
        with self.assertRaises(ValidationError):
            validate_connection_config(config, environment_allowed_ports={554})
