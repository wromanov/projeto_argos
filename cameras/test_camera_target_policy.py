from dataclasses import FrozenInstanceError
from unittest import TestCase

from cameras.integracao.target_policy import (
    TargetDecision,
    TargetPolicy,
    TargetPolicyError,
    sanitize_uri,
)


def policy(**overrides):
    settings = {
        "allowed_cidrs": ["10.42.0.0/24"],
        "denied_cidrs": ["10.42.0.128/25"],
        "ports_by_scheme": {"rtsp": [554, 8554], "http": [80]},
        "allowed_paths_by_scheme": {"rtsp": ["/stream1"]},
        "allowed_farms": ["FARM-A"],
    }
    settings.update(overrides)
    return TargetPolicy.from_mapping(settings)


class TargetPolicyTests(TestCase):
    def validate(self, uri="rtsp://10.42.0.10/stream1", **kwargs):
        profile = {"allowed_schemes": ("rtsp",), "allowed_ports": (554, 8554), "allowed_paths": ("/stream1",), "farm": "FARM-A"}
        profile.update(kwargs)
        return policy().validate("10.42.0.10", uri, **profile)

    def test_authorizes_canonical_ipv4_inside_allowed_cidr_and_profile(self):
        result = self.validate()
        self.assertEqual(result.decision, TargetDecision.AUTHORIZED_TARGET)
        self.assertEqual(str(result.ipv4), "10.42.0.10")
        self.assertEqual(result.port, 554)
        self.assertIsNotNone(result.request)
        self.assertEqual(
            (str(result.request.ipv4), result.request.port, result.request.scheme, result.request.path),
            ("10.42.0.10", 554, "rtsp", "/stream1"),
        )
        self.assertEqual(result.sanitized_uri, "rtsp://10.42.0.10:554")

    def test_invalid_ipv4_and_ambiguous_text_forms_are_rejected(self):
        for value in ("10.42.0.999", "010.42.0.10", "167903242", "10.42.10", "::ffff:10.42.0.10"):
            with self.subTest(value=value):
                self.assertEqual(
                    policy().validate(value, "rtsp://10.42.0.10/stream1", allowed_schemes=("rtsp",), allowed_ports=(554,), farm="FARM-A").decision,
                    TargetDecision.INVALID_TARGET,
                )

    def test_valid_cidr_and_invalid_cidr_configuration(self):
        parsed = policy()
        self.assertEqual(str(parsed.allowed_cidrs[0]), "10.42.0.0/24")
        with self.assertRaises(TargetPolicyError):
            TargetPolicy.from_mapping({
                "allowed_cidrs": ["10.42.0.1/24"],
                "ports_by_scheme": {"rtsp": [554]},
            })

    def test_empty_missing_or_invalid_policy_fails_closed_without_echoing_values(self):
        for settings in (
            {"ports_by_scheme": {"rtsp": [554]}},
            {"allowed_cidrs": [], "ports_by_scheme": {"rtsp": [554]}},
            {"allowed_cidrs": ["10.42.0.0/24"], "ports_by_scheme": {"rtsp": [70000]}},
            {"allowed_cidrs": ["10.42.0.0/24"], "ports_by_scheme": {"rtsp": [554]}, "denied_cidrs": ["not-a-cidr-secret"]},
        ):
            with self.subTest(settings=settings):
                with self.assertRaises(TargetPolicyError) as raised:
                    TargetPolicy.from_mapping(settings)
                self.assertNotIn("not-a-cidr-secret", str(raised.exception))

    def test_invalid_or_missing_policy_has_distinct_fail_closed_decision(self):
        args = {
            "camera_ip": "10.42.0.10",
            "uri": "rtsp://10.42.0.10/stream1",
            "allowed_schemes": ("rtsp",),
            "allowed_ports": (554,),
            "allowed_paths": ("/stream1",),
            "farm": "FARM-A",
        }
        missing = TargetPolicy.validate_settings(None, **args)
        invalid = TargetPolicy.validate_settings({"allowed_cidrs": [], "ports_by_scheme": {}}, **args)
        self.assertEqual(missing.decision, TargetDecision.MISCONFIGURED_POLICY)
        self.assertEqual(invalid.decision, TargetDecision.MISCONFIGURED_POLICY)

    def test_environment_parser_accepts_synthetic_values_and_fails_when_required_value_missing(self):
        parsed = TargetPolicy.from_environment({
            "ARGOS_CAMERA_ALLOWED_CIDRS": "10.42.0.0/24",
            "ARGOS_CAMERA_DENIED_CIDRS": "10.42.0.128/25",
            "ARGOS_CAMERA_ALLOWED_PORTS": "rtsp:554,8554;http:80",
            "ARGOS_CAMERA_ALLOWED_FARMS": "FARM-A",
        })
        self.assertIn("rtsp", parsed.ports_by_scheme)
        with self.assertRaises(TargetPolicyError):
            TargetPolicy.from_environment({})

    def test_policy_is_immutable(self):
        parsed = policy()
        with self.assertRaises((FrozenInstanceError, AttributeError)):
            parsed.allowed_cidrs = ()
        with self.assertRaises(TypeError):
            parsed.ports_by_scheme["rtsp"] = (554,)

    def test_denies_outside_and_explicitly_denied_cidrs(self):
        outside = policy().validate(
            "10.43.0.10", "rtsp://10.43.0.10/stream1",
            allowed_schemes=("rtsp",), allowed_ports=(554,), farm="FARM-A",
        )
        denied = policy().validate(
            "10.42.0.200", "rtsp://10.42.0.200/stream1",
            allowed_schemes=("rtsp",), allowed_ports=(554,), farm="FARM-A",
        )
        self.assertEqual(outside.decision, TargetDecision.DENIED_TARGET)
        self.assertEqual(denied.decision, TargetDecision.DENIED_TARGET)

    def test_denies_special_administrative_or_wrong_farm_targets(self):
        for address in (
            "127.0.0.1", "0.0.0.0", "169.254.169.254", "169.254.10.1",
            "100.100.100.200", "224.0.0.1", "255.255.255.255",
        ):
            with self.subTest(address=address):
                result = policy(allowed_cidrs=["0.0.0.0/0"]).validate(
                    address, f"rtsp://{address}/stream1",
                    allowed_schemes=("rtsp",), allowed_ports=(554,), farm="FARM-A",
                )
                self.assertEqual(result.decision, TargetDecision.DENIED_TARGET)
        for address in ("10.42.0.0", "10.42.0.255"):
            result = policy().validate(
                address, f"rtsp://{address}/stream1",
                allowed_schemes=("rtsp",), allowed_ports=(554,), allowed_paths=("/stream1",), farm="FARM-A",
            )
            self.assertEqual(result.decision, TargetDecision.DENIED_TARGET)
        wrong_farm = self.validate(farm="FARM-B")
        self.assertEqual(wrong_farm.decision, TargetDecision.DENIED_TARGET)

    def test_uri_host_must_equal_registered_camera_ip_and_dns_is_not_resolved(self):
        mismatch = self.validate("rtsp://10.42.0.11/stream1")
        dns = self.validate("rtsp://camera.example/stream1")
        self.assertEqual(mismatch.decision, TargetDecision.DENIED_TARGET)
        self.assertEqual(dns.decision, TargetDecision.DENIED_TARGET)

    def test_scheme_requires_environment_and_profile_approval(self):
        result = self.validate("http://10.42.0.10/stream1")
        self.assertEqual(result.decision, TargetDecision.DENIED_TARGET)

    def test_port_must_be_valid_and_allowed_by_both_policy_and_profile(self):
        allowed = self.validate("rtsp://10.42.0.10:8554/stream1")
        env_denied = self.validate("rtsp://10.42.0.10:8555/stream1")
        profile_denied = self.validate("rtsp://10.42.0.10:8554/stream1", allowed_ports=(554,))
        invalid = self.validate("rtsp://10.42.0.10:70000/stream1")
        self.assertEqual(allowed.decision, TargetDecision.AUTHORIZED_TARGET)
        self.assertEqual(env_denied.decision, TargetDecision.DENIED_TARGET)
        self.assertEqual(profile_denied.decision, TargetDecision.DENIED_TARGET)
        self.assertEqual(invalid.decision, TargetDecision.INVALID_TARGET)

    def test_missing_port_uses_rtsp_default_but_other_schemes_require_one(self):
        result = self.validate()
        self.assertEqual(result.port, 554)
        profile_override = self.validate(default_port=8554)
        self.assertEqual(profile_override.port, 8554)
        invalid_override = self.validate(default_port=0)
        self.assertEqual(invalid_override.decision, TargetDecision.MISCONFIGURED_POLICY)
        http_policy = policy(
            ports_by_scheme={"http": [80]},
            allowed_paths_by_scheme={"http": ["/stream1"]},
        )
        missing = http_policy.validate(
            "10.42.0.10", "http://10.42.0.10/stream1",
            allowed_schemes=("http",), allowed_ports=(80,), allowed_paths=("/stream1",), farm="FARM-A",
        )
        self.assertEqual(missing.decision, TargetDecision.INVALID_TARGET)

    def test_rejects_userinfo_query_fragment_and_noncanonical_authority(self):
        uris = (
            "rtsp://user:password@10.42.0.10/stream1",
            "rtsp://10.42.0.10/stream1?token=secret",
            "rtsp://10.42.0.10/stream1#secret",
            "rtsp://010.42.0.10/stream1",
            "rtsp://[::1]/stream1",
            "rtsp://10.42.0.10:/stream1",
        )
        for uri in uris:
            with self.subTest(uri=sanitize_uri(uri)):
                result = self.validate(uri)
                self.assertIn(result.decision, (TargetDecision.INVALID_TARGET, TargetDecision.DENIED_TARGET))
                self.assertNotIn("password", result.reason)
                self.assertNotIn("secret", result.reason)

    def test_uri_sanitization_drops_userinfo_path_query_and_fragment(self):
        result = sanitize_uri("rtsp://operator:super-secret@10.42.0.10/secret-path?token=secret#frag")
        self.assertEqual(result, "rtsp://10.42.0.10")
        for secret in ("operator", "super-secret", "secret-path", "token", "secret", "frag"):
            self.assertNotIn(secret, result)

    def test_path_must_match_profile_override(self):
        result = self.validate("rtsp://10.42.0.10/other")
        self.assertEqual(result.decision, TargetDecision.DENIED_TARGET)

    def test_profile_cannot_widen_policy_paths_or_fall_back_from_empty_paths(self):
        widened = self.validate(
            "rtsp://10.42.0.10/admin",
            allowed_paths=("/admin",),
        )
        empty_profile = self.validate(allowed_paths=())
        self.assertEqual(widened.decision, TargetDecision.DENIED_TARGET)
        self.assertEqual(empty_profile.decision, TargetDecision.MISCONFIGURED_POLICY)

    def test_invalid_profile_is_reported_without_opening_any_connection(self):
        result = policy().validate(
            "10.42.0.10", "rtsp://10.42.0.10/stream1",
            allowed_schemes=("ftp",), allowed_ports=(554,), farm="FARM-A",
        )
        self.assertEqual(result.decision, TargetDecision.MISCONFIGURED_POLICY)
