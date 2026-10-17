from html.parser import HTMLParser
from unittest.mock import patch

from cryptography.fernet import Fernet
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import Client, TestCase
from django.urls import reverse

from cameras.integracao.credentials import credential_configuration_status
from cameras.integracao.key_provider import CredentialKeyProvider
from cameras.models import Camera, CameraCredential, CameraCredentialVersion, EventoAuditoria


class _FormNestingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.nested = False
        self.ids = []
        self.section_ids = []
        self.credential_actions = []
        self.forms = []
        self.form_stack = []
        self.controls_by_form = {}

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.append(attributes["id"])
        if tag == "section" and attributes.get("id") in {
            "camera-network-section",
            "camera-credential-card",
            "camera-recording-section",
        }:
            self.section_ids.append(attributes["id"])
        if attributes.get("data-open-credential"):
            self.credential_actions.append(attributes["data-open-credential"])
        if tag == "form":
            form_id = attributes.get("id") or f"__form_{len(self.forms)}"
            self.forms.append({"id": form_id, "action": attributes.get("action", "")})
            self.form_stack.append(form_id)
            self.depth += 1
            if self.depth > 1:
                self.nested = True
        elif tag in {"input", "select", "textarea", "button"} and attributes.get("name"):
            owner = attributes.get("form") or (self.form_stack[-1] if self.form_stack else None)
            if owner:
                self.controls_by_form.setdefault(owner, set()).add(attributes["name"])

    def handle_endtag(self, tag):
        if tag == "form":
            self.depth -= 1
            if self.form_stack:
                self.form_stack.pop()


class CameraCredentialHttpTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.tech = user_model.objects.create_user(username="credential-http-tech", password="actor-password")
        permissions = Permission.objects.filter(
            content_type__app_label="cameras",
            codename__in=("change_camera", "view_camera_credential", "change_camera_credential", "reveal_camera_credential"),
        )
        self.tech.user_permissions.add(*permissions)
        self.camera = Camera.objects.create(
            nome="HTTP Credential Camera",
            fabricante="Fabricante",
            modelo="Modelo",
            ip="192.0.2.51",
        )
        self.key_version = "http-test"
        self.provider = CredentialKeyProvider({self.key_version: Fernet.generate_key()}, self.key_version)
        self.client = Client(enforce_csrf_checks=True)
        self.client.force_login(self.tech)
        self.edit_url = reverse("cameras:editar", args=[self.camera.pk])
        self.replace_url = reverse("cameras:replace_camera_credential", args=[self.camera.pk])
        self.revoke_url = reverse("cameras:revoke_camera_credential", args=[self.camera.pk])

    def csrf(self):
        self.client.get(self.edit_url)
        return self.client.cookies["csrftoken"].value

    def test_edit_page_has_minimal_metadata_and_valid_sibling_forms(self):
        with patch("cameras.integracao.credentials.get_environment_key_provider", return_value=self.provider):
            response = self.client.post(
                self.replace_url,
                {"username": "stored-user", "password": "stored-password", "confirm_unsaved_changes": "1"},
                HTTP_X_CSRFTOKEN=self.csrf(),
            )
        self.assertEqual(response.status_code, 302)
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("no-store", response["Cache-Control"])
        self.assertContains(response, "Configurada")
        for forbidden in ("stored-user", "stored-password", "ciphertext", "key_version", "credential_metadata"):
            self.assertNotContains(response, forbidden)
        parser = _FormNestingParser()
        parser.feed(response.content.decode())
        self.assertFalse(parser.nested)
        self.assertEqual(parser.depth, 0)
        self.assertEqual(
            parser.section_ids,
            ["camera-network-section", "camera-credential-card", "camera-recording-section"],
        )
        self.assertEqual(parser.credential_actions, ["reveal", "revoke", "replace"])
        self.assertEqual(len(parser.ids), len(set(parser.ids)))
        camera_controls = parser.controls_by_form["camera-form"]
        self.assertTrue({"nome", "ip", "farm"}.issubset(camera_controls))
        self.assertTrue({"username", "password"}.issubset(
            set().union(*(parser.controls_by_form.get(form["id"], set()) for form in parser.forms if "/credentials" in form["action"]))
        ))
        self.assertFalse({"username", "password", "current_password", "confirm_unsaved_changes"} & camera_controls)
        for form in parser.forms:
            if "/credentials" in form["action"]:
                self.assertFalse({"nome", "ip", "farm"} & parser.controls_by_form.get(form["id"], set()))
        self.assertContains(response, 'form="camera-form"')
        self.assertContains(response, "confirm_unsaved_changes")
        self.assertContains(response, ">Substituir credencial</h2>")
        self.assertContains(response, ">Confirmar substituição</button>")
        self.assertNotContains(response, ">Configurar credencial</h2>")
        self.assertEqual(credential_configuration_status(actor=self.tech, camera_id=self.camera.pk), {"configured": True})

    def test_empty_state_uses_configure_copy_and_semantic_section_order(self):
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        parser = _FormNestingParser()
        parser.feed(html)

        self.assertEqual(
            parser.section_ids,
            ["camera-network-section", "camera-credential-card", "camera-recording-section"],
        )
        self.assertFalse(parser.nested)
        self.assertEqual(parser.depth, 0)
        self.assertEqual(len(parser.ids), len(set(parser.ids)))
        self.assertEqual(parser.credential_actions, ["replace"])
        self.assertIn(">Configurar credencial</h2>", html)
        self.assertIn(">Confirmar configuração</button>", html)
        self.assertNotIn(">Substituir credencial</h2>", html)

    def test_edit_page_omits_entire_credential_panel_without_metadata_permission(self):
        reader = get_user_model().objects.create_user(username="camera-editor-without-credential-metadata")
        reader.user_permissions.add(
            Permission.objects.get(content_type__app_label="cameras", codename="change_camera")
        )
        client = Client()
        client.force_login(reader)
        response = client.get(self.edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "camera-credential-card")
        self.assertNotContains(response, "credential_configuration_status")

    def test_replace_is_post_only_csrf_protected_allowlisted_and_independent(self):
        original_name = self.camera.nome
        self.client.get(self.edit_url)
        with patch("cameras.integracao.credentials.get_environment_key_provider", return_value=self.provider):
            missing_csrf = self.client.post(
                self.replace_url,
                {"username": "new-user", "password": "new-password", "confirm_unsaved_changes": "1"},
            )
            self.assertEqual(missing_csrf.status_code, 403)
            csrf = self.client.cookies["csrftoken"].value
            invalid = self.client.post(
                self.replace_url,
                {"username": "new-user", "password": "new-password", "confirm_unsaved_changes": "1", "extra": "reject"},
                HTTP_X_CSRFTOKEN=csrf,
            )
            self.assertEqual(invalid.status_code, 400)
            response = self.client.post(
                self.replace_url,
                {"username": "new-user", "password": "new-password", "confirm_unsaved_changes": "1"},
                HTTP_X_CSRFTOKEN=csrf,
            )
        self.assertEqual(response.status_code, 302)
        self.assertIn("no-store", response["Cache-Control"])
        self.camera.refresh_from_db()
        self.assertEqual(self.camera.nome, original_name)
        self.assertEqual(CameraCredential.objects.get(camera=self.camera).versions.count(), 1)
        self.assertEqual(EventoAuditoria.objects.filter(camera=self.camera, codigo="camera.credential.created").count(), 1)
        self.assertEqual(self.client.get(self.replace_url).status_code, 405)

    def test_replace_requires_explicit_no_script_decision_and_maps_operational_failure(self):
        csrf = self.csrf()
        no_confirmation = self.client.post(
            self.replace_url,
            {"username": "new-user", "password": "new-password"},
            HTTP_X_CSRFTOKEN=csrf,
        )
        self.assertEqual(no_confirmation.status_code, 400)
        declined_confirmation = self.client.post(
            self.replace_url,
            {"username": "new-user", "password": "new-password", "confirm_unsaved_changes": "0"},
            HTTP_X_CSRFTOKEN=csrf,
        )
        self.assertEqual(declined_confirmation.status_code, 400)
        with patch("cameras.integracao.credentials.get_environment_key_provider", return_value=CredentialKeyProvider()):
            unavailable = self.client.post(
                self.replace_url,
                {"username": "new-user", "password": "new-password", "confirm_unsaved_changes": "1"},
                HTTP_X_CSRFTOKEN=csrf,
            )
        self.assertEqual(unavailable.status_code, 503)
        self.assertNotIn("new-password", unavailable.content.decode())
        self.assertFalse(CameraCredential.objects.filter(camera=self.camera).exists())

    def test_permission_and_missing_camera_errors_are_sanitized(self):
        csrf = self.csrf()
        denied_user = get_user_model().objects.create_user(username="credential-http-denied")
        denied_user.user_permissions.add(
            Permission.objects.get(content_type__app_label="cameras", codename="change_camera")
        )
        denied_client = Client(enforce_csrf_checks=True)
        denied_client.force_login(denied_user)
        denied_client.cookies["csrftoken"] = csrf
        denied = denied_client.post(
            self.replace_url,
            {"username": "secret-user", "password": "secret-password", "confirm_unsaved_changes": "1"},
            HTTP_X_CSRFTOKEN=csrf,
        )
        self.assertEqual(denied.status_code, 403)
        self.assertNotIn("secret-password", denied.content.decode())

        missing_url = reverse("cameras:replace_camera_credential", args=[self.camera.pk + 10000])
        missing = self.client.post(
            missing_url,
            {"username": "secret-user", "password": "secret-password", "confirm_unsaved_changes": "1"},
            HTTP_X_CSRFTOKEN=csrf,
        )
        self.assertEqual(missing.status_code, 404)
        self.assertNotIn("secret-password", missing.content.decode())

    def test_http_double_replace_is_a_new_serialized_operation_not_idempotent(self):
        csrf = self.csrf()
        payload = {"username": "new-user", "password": "new-password", "confirm_unsaved_changes": "1"}
        with patch("cameras.integracao.credentials.get_environment_key_provider", return_value=self.provider):
            first = self.client.post(self.replace_url, payload, HTTP_X_CSRFTOKEN=csrf)
            second = self.client.post(self.replace_url, payload, HTTP_X_CSRFTOKEN=csrf)
        self.assertEqual((first.status_code, second.status_code), (302, 302))
        credential = CameraCredential.objects.get(camera=self.camera)
        self.assertEqual(credential.versions.count(), 2)
        self.assertEqual(credential.active_version.version, 2)
        self.assertEqual(EventoAuditoria.objects.filter(camera=self.camera, codigo="camera.credential.created").count(), 1)
        self.assertEqual(EventoAuditoria.objects.filter(camera=self.camera, codigo="camera.credential.replaced").count(), 1)

    def test_revoke_requires_confirmation_and_repeated_post_returns_conflict(self):
        csrf = self.csrf()
        with patch("cameras.integracao.credentials.get_environment_key_provider", return_value=self.provider):
            self.client.post(
                self.replace_url,
                {"username": "new-user", "password": "new-password", "confirm_unsaved_changes": "1"},
                HTTP_X_CSRFTOKEN=csrf,
            )
        no_confirmation = self.client.post(self.revoke_url, {}, HTTP_X_CSRFTOKEN=csrf)
        self.assertEqual(no_confirmation.status_code, 400)
        revoked = self.client.post(
            self.revoke_url,
            {"confirm_unsaved_changes": "1"},
            HTTP_X_CSRFTOKEN=csrf,
        )
        self.assertEqual(revoked.status_code, 302)
        duplicate = self.client.post(
            self.revoke_url,
            {"confirm_unsaved_changes": "1"},
            HTTP_X_CSRFTOKEN=csrf,
        )
        self.assertEqual(duplicate.status_code, 409)
        credential = CameraCredential.objects.get(camera=self.camera)
        self.assertIsNone(credential.active_version_id)
        self.assertEqual(credential.versions.get().state, CameraCredentialVersion.State.REVOKED)

    def test_revoke_audit_failure_returns_no_success_and_rolls_back(self):
        csrf = self.csrf()
        with patch("cameras.integracao.credentials.get_environment_key_provider", return_value=self.provider):
            self.client.post(
                self.replace_url,
                {"username": "new-user", "password": "new-password", "confirm_unsaved_changes": "1"},
                HTTP_X_CSRFTOKEN=csrf,
            )
        with patch("cameras.auditoria.registrar_evento", side_effect=RuntimeError("audit unavailable")):
            response = self.client.post(
                self.revoke_url,
                {"confirm_unsaved_changes": "1"},
                HTTP_X_CSRFTOKEN=csrf,
            )
        self.assertEqual(response.status_code, 500)
        self.assertNotIn("audit unavailable", response.content.decode())
        credential = CameraCredential.objects.get(camera=self.camera)
        self.assertIsNotNone(credential.active_version_id)
        self.assertEqual(credential.active_version.state, CameraCredentialVersion.State.ACTIVE)
        self.assertEqual(EventoAuditoria.objects.filter(camera=self.camera).count(), 1)
