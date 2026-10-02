"""Persistência e resolução segura da configuração não secreta da câmera."""

import ipaddress
from urllib.parse import unquote, urlsplit, urlunsplit

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from django.utils import timezone

from cameras.authorization import require_camera_permission
from cameras.models import Camera, CameraCapabilityProfile, CameraConnectionConfig, CameraCredentialVersion, EstadoMonitoramento, EventoAuditoria
from .capabilities import compatibility_status, require_automatic_compatibility

_CONFIG_FIELDS = {"profile", "enabled", "rtsp_uri", "http_endpoint_override", "http_port_override", "transport", "credential_id"}


def _normalized_ipv4(value):
    try:
        address = ipaddress.ip_address(value)
    except ValueError as exc:
        raise ValidationError("A câmera precisa ter um IPv4 válido cadastrado.") from exc
    if address.version != 4:
        raise ValidationError("O destino deve ser IPv4.")
    return str(address)


def _validate_relative_path(path):
    if not path:
        return ""
    if not path.startswith("/") or path.startswith("//") or "\\" in path:
        raise ValidationError("Endpoint deve ser um path relativo controlado pelo perfil.")
    decoded_path = unquote(path)
    if any(part == ".." for part in decoded_path.split("/")) or "?" in path or "#" in path:
        raise ValidationError("Endpoint contém componente não permitido.")
    return path


def validate_rtsp_uri(*, camera, profile, uri, environment_allowed_ports):
    if not uri:
        return ""
    if profile.adapter_key != CameraCapabilityProfile.Adapter.RTSP:
        raise ValidationError("URI RTSP exige perfil RTSP.")
    try:
        parsed = urlsplit(uri)
        port = parsed.port
    except ValueError as exc:
        raise ValidationError("URI RTSP inválida.") from exc
    if parsed.scheme not in profile.allowed_schemes:
        raise ValidationError("Scheme não permitido pelo perfil.")
    if parsed.username is not None or parsed.password is not None:
        raise ValidationError("URI não pode conter userinfo ou credenciais.")
    if parsed.query or parsed.fragment:
        raise ValidationError("URI não pode conter query nem fragmento.")
    host = _normalized_ipv4(parsed.hostname or "")
    if host != _normalized_ipv4(camera.ip or ""):
        raise ValidationError("Host da URI deve corresponder ao IPv4 cadastrado da câmera.")
    if port is None:
        if 554 in profile.allowed_ports:
            effective_port = 554
        elif len(profile.allowed_ports) == 1:
            effective_port = profile.allowed_ports[0]
        else:
            raise ValidationError("Porta não especificada e perfil sem porta default inequívoca.")
    else:
        effective_port = port
    if effective_port not in profile.allowed_ports or effective_port not in set(environment_allowed_ports):
        raise ValidationError("Porta não permitida simultaneamente pelo perfil e pela policy do ambiente.")
    if profile.endpoint_policy == CameraCapabilityProfile.EndpointPolicy.PROFILE_FIXED:
        if len(profile.allowed_ports) != 1:
            raise ValidationError("Perfil de endpoint fixo precisa declarar uma única porta.")
        if parsed.path != profile.default_path or (port is not None and port != profile.allowed_ports[0]):
            raise ValidationError("URI diverge do endpoint fixo do perfil.")
    else:
        if parsed.path and parsed.path != profile.default_path and "path" not in profile.allowed_override_fields:
            raise ValidationError("Perfil não autoriza override de path.")
        if port is not None and "port" not in profile.allowed_override_fields:
            raise ValidationError("Perfil não autoriza override de porta.")
    _validate_relative_path(parsed.path)
    netloc = host if port is None else f"{host}:{port}"
    return urlunsplit((parsed.scheme, netloc, parsed.path, "", ""))


def validate_connection_config(config, *, environment_allowed_ports):
    profile = config.profile
    if not profile.active:
        raise ValidationError({"profile": "Perfil inativo impede novas configurações."})
    if config.enabled and profile.credential_required:
        credential = config.credential
        if (
            credential is None
            or credential.camera_id != config.camera_id
            or credential.state != "ACTIVE"
            or credential.active_version_id is None
            or credential.active_version.state != CameraCredentialVersion.State.ACTIVE
        ):
            raise ValidationError({"credential_id": "Configuração exige credencial ativa vinculada à mesma câmera."})
    if config.credential_id is not None and config.credential.camera_id != config.camera_id:
        raise ValidationError({"credential_id": "Credencial deve pertencer à mesma câmera."})
    _validate_relative_path(profile.default_path)
    config.full_clean(exclude=["camera"])
    if config.rtsp_uri:
        config.rtsp_uri = validate_rtsp_uri(camera=config.camera, profile=profile, uri=config.rtsp_uri, environment_allowed_ports=environment_allowed_ports)
    if config.http_endpoint_override:
        if profile.adapter_key != CameraCapabilityProfile.Adapter.HTTP_SNAPSHOT:
            raise ValidationError({"http_endpoint_override": "Override HTTP exige perfil HTTP_SNAPSHOT."})
        if profile.endpoint_policy != CameraCapabilityProfile.EndpointPolicy.TECHNICIAN_OVERRIDE or "path" not in profile.allowed_override_fields:
            raise ValidationError({"http_endpoint_override": "Perfil não autoriza override de endpoint."})
        config.http_endpoint_override = _validate_relative_path(config.http_endpoint_override)
    if config.http_port_override is not None:
        if profile.adapter_key != CameraCapabilityProfile.Adapter.HTTP_SNAPSHOT or "port" not in profile.allowed_override_fields:
            raise ValidationError({"http_port_override": "Perfil não autoriza override de porta HTTP."})
        if config.http_port_override not in profile.allowed_ports or config.http_port_override not in set(environment_allowed_ports):
            raise ValidationError({"http_port_override": "Porta não permitida pelo perfil e pela policy do ambiente."})
    if profile.adapter_key == CameraCapabilityProfile.Adapter.RTSP and config.transport != CameraConnectionConfig.Transport.AUTO:
        if "transport" not in profile.allowed_override_fields:
            raise ValidationError({"transport": "Perfil não autoriza override de transporte."})
    return config


def _increment_config_generation(camera_id):
    state, _ = EstadoMonitoramento.objects.get_or_create(camera_id=camera_id)
    EstadoMonitoramento.objects.filter(pk=state.pk).update(ultima_geracao_configuracao=F("ultima_geracao_configuracao") + 1, atualizado_em=timezone.now())
    state.refresh_from_db(fields=["ultima_geracao_configuracao"])
    return state.ultima_geracao_configuracao


def invalidate_target_config_generation_if_ip_changed(*, camera_id, previous_ip, current_ip):
    """Fence prior target resolutions when the persisted camera IPv4 changes."""
    if previous_ip == current_ip:
        return None
    return _increment_config_generation(camera_id)


@transaction.atomic
def save_connection_config(*, actor, camera_id, values, environment_allowed_ports, request=None):
    """Valida, salva, atualiza fencing de geração e audita atomicamente."""
    require_camera_permission(actor=actor, permission_codename="change_camera_connection", camera_id=camera_id)
    unknown = set(values) - _CONFIG_FIELDS
    if unknown:
        raise ValidationError("Campo de configuração não previsto no contrato.")
    camera = Camera.objects.select_for_update().get(pk=camera_id)
    config = CameraConnectionConfig.objects.select_for_update().filter(camera_id=camera_id).first()
    created = config is None
    if created:
        config = CameraConnectionConfig(camera=camera)
    previous_profile_id = config.profile_id if not created else None
    before = {name: getattr(config, name) for name in values if name != "profile"}
    for name, value in values.items():
        setattr(config, name, value)
    if config.profile_id is None:
        raise ValidationError({"profile": "Perfil é obrigatório."})
    validate_connection_config(config, environment_allowed_ports=environment_allowed_ports)
    changed_fields = [name for name in values if name == "profile" and previous_profile_id != config.profile_id]
    changed_fields += [name for name in values if name != "profile" and before.get(name) != getattr(config, name)]
    if created:
        changed_fields = sorted(set(values))
    if not changed_fields:
        return config
    config.config_version = 1 if created else config.config_version + 1
    config.updated_by = actor
    config.save()
    generation = _increment_config_generation(camera_id)
    from cameras.auditoria import registrar_evento

    registrar_evento(
        codigo="camera.connection.created" if created else "camera.connection.updated",
        resumo="Configuração técnica da câmera alterada.",
        categoria=EventoAuditoria.Categoria.CAMERA,
        request=request,
        usuario=actor,
        camera=camera,
        entidade=config,
        alteracoes={"campos": {"anterior": [], "atual": sorted(set(changed_fields))}},
        metadados={"config_version": config.config_version, "config_generation": generation},
    )
    return config


def resolve_connection_config(*, camera_id, environment_allowed_ports, automatic=False):
    config = CameraConnectionConfig.objects.select_related("camera", "profile").get(camera_id=camera_id)
    if not config.enabled:
        raise ValidationError("Configuração técnica desabilitada.")
    validate_connection_config(config, environment_allowed_ports=environment_allowed_ports)
    status = compatibility_status(config.camera, config.profile)
    if automatic:
        require_automatic_compatibility(config.camera, config.profile)
    rtsp_uri = config.rtsp_uri
    if config.profile.adapter_key == CameraCapabilityProfile.Adapter.RTSP:
        host = _normalized_ipv4(config.camera.ip or "")
        if not rtsp_uri:
            path = config.profile.default_path
            schemes = config.profile.allowed_schemes
            scheme = "rtsp" if "rtsp" in schemes else (schemes[0] if len(schemes) == 1 else None)
        else:
            parsed = urlsplit(rtsp_uri)
            path = parsed.path
            schemes = config.profile.allowed_schemes
            scheme = parsed.scheme
        if 554 in config.profile.allowed_ports:
            port = 554
        elif len(config.profile.allowed_ports) == 1:
            port = config.profile.allowed_ports[0]
        else:
            raise ValidationError("Perfil sem porta default inequívoca.")
        if scheme is None:
            raise ValidationError("Perfil sem scheme default inequívoco.")
        if port not in set(environment_allowed_ports):
            raise ValidationError("Porta default bloqueada pela policy do ambiente.")
        rtsp_uri = urlunsplit((scheme, f"{host}:{port}", path, "", ""))
    http_endpoint = config.http_endpoint_override or config.profile.default_path
    http_port = config.http_port_override
    if config.profile.adapter_key == CameraCapabilityProfile.Adapter.HTTP_SNAPSHOT:
        if http_port is None:
            if len(config.profile.allowed_ports) != 1:
                raise ValidationError("Perfil sem porta HTTP default inequívoca.")
            http_port = config.profile.allowed_ports[0]
        if http_port not in set(environment_allowed_ports):
            raise ValidationError("Porta default bloqueada pela policy do ambiente.")
    return {
        "camera_id": config.camera_id,
        "profile_key": config.profile.profile_key,
        "profile_version": config.profile.version,
        "adapter_key": config.profile.adapter_key,
        "rtsp_uri": rtsp_uri,
        "http_endpoint_override": http_endpoint,
        "http_port_override": http_port,
        "transport": config.transport,
        "config_version": config.config_version,
        "compatibility": status,
    }
