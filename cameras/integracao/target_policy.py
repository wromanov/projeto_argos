"""Fail-closed target validation for camera integration adapters.

This module deliberately does not perform DNS resolution or open sockets. It
validates persisted camera targets against trusted, environment-scoped policy
data so a future adapter can consume only a canonical IPv4 request.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from ipaddress import IPv4Address, IPv4Network, ip_address, ip_network
from types import MappingProxyType
from typing import Mapping
from urllib.parse import urlsplit, urlunsplit


class TargetDecision(StrEnum):
    AUTHORIZED_TARGET = "AUTHORIZED_TARGET"
    DENIED_TARGET = "DENIED_TARGET"
    INVALID_TARGET = "INVALID_TARGET"
    MISCONFIGURED_POLICY = "MISCONFIGURED_POLICY"


@dataclass(frozen=True, slots=True)
class AuthorizedTargetRequest:
    """Minimal adapter input produced only after all policy checks pass."""

    ipv4: IPv4Address
    port: int
    scheme: str
    path: str


@dataclass(frozen=True, slots=True)
class TargetValidation:
    decision: TargetDecision
    request: AuthorizedTargetRequest | None = None
    ipv4: IPv4Address | None = None
    port: int | None = None
    scheme: str | None = None
    path: str | None = None
    sanitized_uri: str | None = None
    reason: str = ""

    @property
    def authorized(self) -> bool:
        return self.decision is TargetDecision.AUTHORIZED_TARGET


class TargetPolicyError(ValueError):
    """Raised for invalid trusted policy configuration, without echoing input."""

    def __init__(self, reason: str = "Target policy configuration is invalid") -> None:
        super().__init__(reason)


def sanitize_uri(value: str) -> str:
    """Return a URI without userinfo, path, query, or fragment material."""
    try:
        parsed = urlsplit(value)
        if not parsed.scheme or not parsed.netloc or not parsed.hostname:
            return "[invalid-uri]"
        try:
            port = parsed.port
        except ValueError:
            port = None
        host = parsed.hostname
        netloc = host if port is None else f"{host}:{port}"
        return urlunsplit((parsed.scheme.lower(), netloc, "", "", ""))
    except (TypeError, ValueError, UnicodeError):
        return "[invalid-uri]"


def _parse_ipv4(value: object) -> IPv4Address:
    if not isinstance(value, str) or not value or value.strip() != value:
        raise TargetPolicyError()
    try:
        parsed = ip_address(value)
    except ValueError as exc:
        raise TargetPolicyError() from exc
    if not isinstance(parsed, IPv4Address) or str(parsed) != value:
        raise TargetPolicyError()
    return parsed


def _parse_network(value: object) -> IPv4Network:
    if not isinstance(value, str) or not value or value.strip() != value:
        raise TargetPolicyError()
    try:
        network = ip_network(value, strict=True)
    except ValueError as exc:
        raise TargetPolicyError() from exc
    if not isinstance(network, IPv4Network) or str(network) != value:
        raise TargetPolicyError()
    return network


@dataclass(frozen=True, slots=True)
class TargetPolicy:
    """Immutable allow/deny policy loaded from trusted environment settings."""

    allowed_cidrs: tuple[IPv4Network, ...]
    ports_by_scheme: Mapping[str, tuple[int, ...]]
    denied_cidrs: tuple[IPv4Network, ...] = ()
    allowed_farms: frozenset[str] | None = None
    allowed_paths_by_scheme: Mapping[str, tuple[str, ...]] | None = None

    def __post_init__(self) -> None:
        try:
            allowed = tuple(_parse_network(str(value)) for value in self.allowed_cidrs)
            denied = tuple(_parse_network(str(value)) for value in self.denied_cidrs)
            ports: dict[str, tuple[int, ...]] = {}
            for scheme, values in dict(self.ports_by_scheme).items():
                normalized_scheme = _validate_scheme(scheme)
                normalized_ports = tuple(values)
                if not normalized_ports or any(type(port) is not int or not 1 <= port <= 65535 for port in normalized_ports):
                    raise TargetPolicyError()
                ports[normalized_scheme] = normalized_ports
            paths = {
                _validate_scheme(scheme): tuple(_validate_path(path) for path in values)
                for scheme, values in dict(self.allowed_paths_by_scheme or {}).items()
            }
            if not allowed or not ports:
                raise TargetPolicyError()
            if any(scheme not in ports for scheme in paths):
                raise TargetPolicyError()
            if self.allowed_farms is not None and any(not isinstance(farm, str) or not farm.strip() for farm in self.allowed_farms):
                raise TargetPolicyError()
        except (TypeError, AttributeError, KeyError) as exc:
            raise TargetPolicyError() from exc

        object.__setattr__(self, "allowed_cidrs", allowed)
        object.__setattr__(self, "denied_cidrs", denied)
        object.__setattr__(self, "ports_by_scheme", MappingProxyType(ports))
        object.__setattr__(self, "allowed_paths_by_scheme", MappingProxyType(paths))
        if self.allowed_farms is not None:
            object.__setattr__(self, "allowed_farms", frozenset(self.allowed_farms))

    @classmethod
    def from_mapping(cls, settings: Mapping[str, object]) -> "TargetPolicy":
        """Parse trusted settings; missing and malformed values fail closed."""
        try:
            allowed = settings["allowed_cidrs"]
            ports = settings["ports_by_scheme"]
            if not isinstance(allowed, (list, tuple)) or not isinstance(ports, Mapping):
                raise TargetPolicyError()
            denied = settings.get("denied_cidrs", ())
            farms = settings.get("allowed_farms")
            paths = settings.get("allowed_paths_by_scheme", {})
            if not isinstance(denied, (list, tuple)) or not isinstance(paths, Mapping):
                raise TargetPolicyError()
            if farms is not None and not isinstance(farms, (set, frozenset, list, tuple)):
                raise TargetPolicyError()
            return cls(
                allowed_cidrs=tuple(_parse_network(item) for item in allowed),
                ports_by_scheme={key: tuple(value) for key, value in ports.items()},
                denied_cidrs=tuple(_parse_network(item) for item in denied),
                allowed_farms=None if farms is None else frozenset(farms),
                allowed_paths_by_scheme={key: tuple(value) for key, value in paths.items()},
            )
        except (KeyError, TypeError, ValueError) as exc:
            if isinstance(exc, TargetPolicyError):
                raise
            raise TargetPolicyError() from exc

    @classmethod
    def from_environment(cls, environ: Mapping[str, str]) -> "TargetPolicy":
        """Load explicit ARGOS variables; no real production values are embedded."""
        try:
            allowed = _split_csv(environ["ARGOS_CAMERA_ALLOWED_CIDRS"])
            denied = _split_csv(environ.get("ARGOS_CAMERA_DENIED_CIDRS", ""))
            ports: dict[str, tuple[int, ...]] = {}
            for item in environ["ARGOS_CAMERA_ALLOWED_PORTS"].split(";"):
                scheme, raw_ports = item.split(":", 1)
                ports[scheme] = tuple(int(port) for port in _split_csv(raw_ports))
            farms = _split_csv(environ.get("ARGOS_CAMERA_ALLOWED_FARMS", ""))
            return cls.from_mapping({
                "allowed_cidrs": allowed,
                "denied_cidrs": denied,
                "ports_by_scheme": ports,
                "allowed_farms": farms or None,
            })
        except (KeyError, TypeError, ValueError) as exc:
            raise TargetPolicyError() from exc

    def validate(
        self,
        camera_ip: str,
        uri: str,
        *,
        allowed_schemes: tuple[str, ...] | None = None,
        allowed_ports: tuple[int, ...] | None = None,
        default_port: int | None = None,
        allowed_paths: tuple[str, ...] | None = None,
        farm: str | None = None,
    ) -> TargetValidation:
        """Validate a persisted URI against camera IP, policy and profile values."""
        try:
            ip = _parse_ipv4(camera_ip)
        except TargetPolicyError:
            return _result(TargetDecision.INVALID_TARGET, "Invalid camera IPv4 address")
        if _is_special_or_admin(ip):
            return _result(TargetDecision.DENIED_TARGET, "Camera target is not permitted")
        if any(
            ip in network
            and network.prefixlen < 31
            and ip in (network.network_address, network.broadcast_address)
            for network in self.allowed_cidrs
        ):
            return _result(TargetDecision.DENIED_TARGET, "Camera target is not permitted")
        if any(ip in network for network in self.denied_cidrs):
            return _result(TargetDecision.DENIED_TARGET, "Camera target is not permitted")
        if not any(ip in network for network in self.allowed_cidrs):
            return _result(TargetDecision.DENIED_TARGET, "Camera target is not permitted")
        if self.allowed_farms is not None and farm not in self.allowed_farms:
            return _result(TargetDecision.DENIED_TARGET, "Camera farm is not permitted")

        try:
            if not isinstance(uri, str) or not uri or uri.strip() != uri or "\\" in uri or any(ord(char) < 32 for char in uri):
                return _result(TargetDecision.INVALID_TARGET, "URI is invalid")
            parts = urlsplit(uri)
            if parts.username is not None or parts.password is not None:
                return _result(TargetDecision.INVALID_TARGET, "URI userinfo is not permitted")
            scheme = parts.scheme.lower()
            if not parts.scheme or parts.scheme != scheme or not parts.netloc or parts.hostname is None:
                return _result(TargetDecision.INVALID_TARGET, "URI is invalid")
            if "?" in uri or "#" in uri:
                return _result(TargetDecision.INVALID_TARGET, "URI query and fragment are not permitted")
            if not parts.path.startswith("/") or any(ord(char) < 32 for char in parts.path):
                return _result(TargetDecision.INVALID_TARGET, "URI path is invalid")
            if parts.hostname != str(ip):
                return _result(TargetDecision.DENIED_TARGET, "URI host does not match camera IPv4")
            if parts.netloc.count(":") > 1 or parts.netloc.startswith("["):
                return _result(TargetDecision.INVALID_TARGET, "Only canonical IPv4 targets are permitted")
            if parts.netloc.endswith(":"):
                return _result(TargetDecision.INVALID_TARGET, "URI port is invalid")
            try:
                host_ip = _parse_ipv4(parts.hostname)
                explicit_port = parts.port
            except (TargetPolicyError, ValueError):
                return _result(TargetDecision.INVALID_TARGET, "URI host or port is invalid")
            if host_ip != ip:
                return _result(TargetDecision.DENIED_TARGET, "URI host does not match camera IPv4")
        except (TypeError, ValueError, UnicodeError):
            return _result(TargetDecision.INVALID_TARGET, "URI is invalid")

        try:
            profile_schemes = tuple(_validate_scheme(value) for value in (allowed_schemes or ()))
        except TargetPolicyError:
            return _result(TargetDecision.MISCONFIGURED_POLICY, "Target profile is invalid")
        if not profile_schemes or scheme not in profile_schemes or scheme not in self.ports_by_scheme:
            return _result(TargetDecision.DENIED_TARGET, "URI scheme is not permitted")
        port = explicit_port
        if port is None:
            if default_port is not None and (type(default_port) is not int or not 1 <= default_port <= 65535):
                return _result(TargetDecision.MISCONFIGURED_POLICY, "Target profile is invalid")
            port = default_port
            if port is None and scheme == "rtsp":
                port = 554
            if port is None:
                return _result(TargetDecision.INVALID_TARGET, "URI port is required")
        if not 1 <= port <= 65535:
            return _result(TargetDecision.INVALID_TARGET, "URI port is invalid")
        try:
            profile_ports = tuple(allowed_ports or ())
        except TypeError:
            return _result(TargetDecision.MISCONFIGURED_POLICY, "Target profile is invalid")
        if not profile_ports or any(type(value) is not int or not 1 <= value <= 65535 for value in profile_ports):
            return _result(TargetDecision.MISCONFIGURED_POLICY, "Target profile is invalid")
        if port not in self.ports_by_scheme[scheme] or port not in profile_ports:
            return _result(TargetDecision.DENIED_TARGET, "URI port is not permitted")
        configured_paths = self.allowed_paths_by_scheme.get(scheme, ())
        try:
            profile_paths = (
                None
                if allowed_paths is None
                else tuple(_validate_path(value) for value in allowed_paths)
            )
        except (TypeError, TargetPolicyError):
            return _result(TargetDecision.MISCONFIGURED_POLICY, "Target profile is invalid")
        if profile_paths is not None and not profile_paths:
            return _result(TargetDecision.MISCONFIGURED_POLICY, "Target profile path is missing")
        if profile_paths is None:
            effective_paths = configured_paths
            if not effective_paths:
                return _result(TargetDecision.MISCONFIGURED_POLICY, "Target policy path is missing")
        elif configured_paths:
            effective_paths = tuple(path for path in profile_paths if path in configured_paths)
        else:
            effective_paths = profile_paths
        if parts.path not in effective_paths:
            return _result(TargetDecision.DENIED_TARGET, "URI path is not permitted")

        sanitized = urlunsplit((scheme, f"{ip}:{port}", "", "", ""))
        return TargetValidation(
            decision=TargetDecision.AUTHORIZED_TARGET,
            request=AuthorizedTargetRequest(ipv4=ip, port=port, scheme=scheme, path=parts.path),
            ipv4=ip,
            port=port,
            scheme=scheme,
            path=parts.path,
            sanitized_uri=sanitized,
            reason="Target is authorized",
        )

    @classmethod
    def validate_settings(
        cls,
        settings: Mapping[str, object] | None,
        camera_ip: str,
        uri: str,
        **profile: object,
    ) -> TargetValidation:
        """Evaluate raw configuration while preserving a fail-closed result."""
        try:
            if settings is None:
                raise TargetPolicyError()
            target_policy = cls.from_mapping(settings)
        except TargetPolicyError:
            return _result(TargetDecision.MISCONFIGURED_POLICY, "Target policy is unavailable or invalid")
        try:
            return target_policy.validate(camera_ip, uri, **profile)
        except TypeError:
            return _result(TargetDecision.MISCONFIGURED_POLICY, "Target profile is invalid")


def _result(decision: TargetDecision, reason: str) -> TargetValidation:
    return TargetValidation(decision=decision, reason=reason)


def _validate_scheme(value: object) -> str:
    if not isinstance(value, str) or not value or not value.isascii() or not value.replace("+", "").replace("-", "").replace(".", "").isalnum():
        raise TargetPolicyError()
    normalized = value.lower()
    if normalized != value or normalized not in {"rtsp", "rtsps", "http", "https"}:
        raise TargetPolicyError()
    return normalized


def _validate_path(value: object) -> str:
    if not isinstance(value, str) or not value.startswith("/") or "\\" in value or any(ord(char) < 32 for char in value):
        raise TargetPolicyError()
    return value


def _is_special_or_admin(ip: IPv4Address) -> bool:
    metadata_addresses = {
        IPv4Address("169.254.169.254"),
        IPv4Address("100.100.100.200"),
    }
    return (
        ip.is_loopback
        or ip.is_unspecified
        or ip.is_link_local
        or ip.is_multicast
        or ip == IPv4Address("255.255.255.255")
        or ip in metadata_addresses
        or ip in IPv4Network("0.0.0.0/8")
        or ip in IPv4Network("127.0.0.0/8")
        or ip in IPv4Network("224.0.0.0/4")
        or ip in IPv4Network("240.0.0.0/4")
    )


def _split_csv(value: object) -> tuple[str, ...]:
    if not isinstance(value, str):
        raise TargetPolicyError()
    return tuple(item.strip() for item in value.split(",") if item.strip())
