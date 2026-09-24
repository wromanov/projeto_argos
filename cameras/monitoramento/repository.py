"""Adapter ORM local para o estado operacional do monitoramento.

O módulo é a única fronteira desta etapa que conhece Django.  Ele não executa
probes e não altera os campos legados ``Camera.status``, ``status_em`` ou
``ultima_verificacao``.
"""

from collections.abc import Callable, Iterable
from datetime import datetime, timedelta, timezone as datetime_timezone

from django.db import transaction
from django.db.models import DateTimeField, ExpressionWrapper, F, Q, Value
from django.db.models.functions import Now
from django.utils import timezone

from cameras.models import (
    Camera,
    EstadoMonitoramento,
    Indisponibilidade,
    TransicaoEstadoMonitoramento,
)

from .confirmation import ConfirmationMemory, ConfirmationPolicy, ProcessingDisposition, TechnicalDecision, TechnicalState
from .contracts import ProbeResult
from .schemas import CompletionDisposition, OwnershipLease, ScheduleCandidate


class DjangoMonitoringRepository:
    """Ports MON-05B sobre SQLite/Django, para uma única instância local."""

    def __init__(self, *, before_transition: Callable[[], None] | None = None) -> None:
        self._before_transition = before_transition

    @staticmethod
    def _utc_timestamp(value: datetime, field_name: str) -> datetime:
        if not isinstance(value, datetime):
            raise TypeError(f"{field_name} must be a datetime")
        if timezone.is_naive(value):
            raise ValueError(f"{field_name} must be timezone-aware")
        return value.astimezone(datetime_timezone.utc)

    @staticmethod
    def _validate_camera_boundary(expected_camera_id: int, actual_camera_id: int, field_name: str) -> None:
        if actual_camera_id != expected_camera_id:
            raise ValueError(f"{field_name} camera does not match monitoring state")

    @staticmethod
    def _eligible(camera: Camera) -> bool:
        return (
            camera.situacao_operacional == Camera.SituacaoOperacional.PRODUCAO
            and camera.cadastro_completo
        )

    @staticmethod
    def _state_memory(state: EstadoMonitoramento, policy: ConfirmationPolicy) -> ConfirmationMemory:
        if not state.em_escopo:
            return ConfirmationMemory.initial(policy.version)
        return ConfirmationMemory(
            state=TechnicalState(state.estado_estavel),
            positive_streak=state.sequencia_positiva,
            negative_streak=state.sequencia_negativa,
            last_observed_at=state.confirmacao_ultima_observacao_em,
            policy_version=state.versao_politica_confirmacao,
        )

    def list_due(self, now: datetime, limit: int) -> Iterable[ScheduleCandidate]:
        """Carrega no máximo ``limit`` candidatos sem histórico por leitura."""

        if limit <= 0:
            raise ValueError("limit must be positive")
        cameras = (
            Camera.objects.select_related("estado_monitoramento")
            .filter(situacao_operacional=Camera.SituacaoOperacional.PRODUCAO)
            .order_by("estado_monitoramento__proximo_vencimento_em", "pk")
        )
        candidates: list[ScheduleCandidate] = []
        for camera in cameras:
            if not self._eligible(camera):
                continue
            state = getattr(camera, "estado_monitoramento", None)
            if state is not None and not state.em_escopo:
                self.enter_scope(camera.pk, now)
                state.refresh_from_db()
            due_at = state.proximo_vencimento_em if state and state.proximo_vencimento_em else now
            candidates.append(ScheduleCandidate(camera.pk, due_at, config_generation=(state.ultima_geracao_configuracao if state else 1)))
            if len(candidates) == limit:
                break
        return tuple(candidates)

    def current_generation(self, camera_id: int) -> int:
        state = EstadoMonitoramento.objects.filter(camera_id=camera_id).only("ultima_geracao_configuracao").first()
        return state.ultima_geracao_configuracao if state else 1

    @staticmethod
    def _lease_expiry(lease_seconds: int) -> ExpressionWrapper:
        if isinstance(lease_seconds, bool) or not isinstance(lease_seconds, int) or lease_seconds <= 0:
            raise ValueError("lease_seconds must be a positive integer")
        return ExpressionWrapper(
            Now() + Value(timedelta(seconds=lease_seconds)),
            output_field=DateTimeField(),
        )

    def claim(self, camera_id: int, owner_id: str, lease_seconds: int) -> OwnershipLease | None:
        """Adquire uma lease por câmera com epoch monotônico no tempo do banco."""

        if isinstance(camera_id, bool) or not isinstance(camera_id, int) or camera_id <= 0:
            raise ValueError("camera_id must be a positive integer")
        if not isinstance(owner_id, str) or not owner_id.strip():
            raise ValueError("owner_id must be a non-empty string")
        expiry = self._lease_expiry(lease_seconds)
        with transaction.atomic():
            state, _ = EstadoMonitoramento.objects.get_or_create(camera_id=camera_id)
            updated = (
                EstadoMonitoramento.objects.filter(pk=state.pk)
                .filter(
                    Q(monitoring_owner_id__isnull=True, monitoring_lease_expires_at__isnull=True)
                    | Q(monitoring_lease_expires_at__lte=Now())
                )
                .update(
                    monitoring_owner_id=owner_id,
                    monitoring_lease_expires_at=expiry,
                    monitoring_ownership_epoch=F("monitoring_ownership_epoch") + 1,
                )
            )
            if updated != 1:
                return None
            state.refresh_from_db(fields=["monitoring_owner_id", "monitoring_ownership_epoch"])
            return OwnershipLease(state.monitoring_owner_id, state.monitoring_ownership_epoch)

    def release(self, camera_id: int, ownership: OwnershipLease) -> bool:
        """Libera somente a lease ainda pertencente ao caller/token informado."""

        if isinstance(camera_id, bool) or not isinstance(camera_id, int) or camera_id <= 0:
            raise ValueError("camera_id must be a positive integer")
        if not isinstance(ownership, OwnershipLease):
            raise TypeError("ownership must be an OwnershipLease")
        return (
            EstadoMonitoramento.objects.filter(
                camera_id=camera_id,
                monitoring_owner_id=ownership.owner_id,
                monitoring_ownership_epoch=ownership.epoch,
            ).update(
                monitoring_owner_id=None,
                monitoring_lease_expires_at=None,
            )
            == 1
        )

    def is_eligible(self, camera_id: int) -> bool:
        camera = Camera.objects.only(
            "id", "situacao_operacional", "nome", "fabricante", "modelo", "serial", "mac", "tipo", "terminal", "pavimento", "setor", "ambiente", "ip", "mascara_subrede", "gateway", "vlan", "farm", "retencao_esperada_dias", "codec"
        ).get(pk=camera_id)
        return self._eligible(camera)

    def load(self, candidate: ScheduleCandidate, policy: ConfirmationPolicy) -> ConfirmationMemory:
        state = EstadoMonitoramento.objects.filter(camera_id=candidate.camera_id).first()
        return ConfirmationMemory.initial(policy.version) if state is None else self._state_memory(state, policy)

    def store(
        self,
        candidate: ScheduleCandidate,
        result: ProbeResult,
        memory: ConfirmationMemory,
        decision: TechnicalDecision,
        next_due_at: datetime,
        ownership: OwnershipLease | None = None,
    ) -> bool | CompletionDisposition:
        """Persiste uma completion em uma transação curta e monotônica.

        ``False`` is returned when a newer persisted generation wins the
        compare-and-set boundary.  That is a known stale completion, not an
        operational repository failure.
        """

        with transaction.atomic():
            state, _ = EstadoMonitoramento.objects.select_for_update().get_or_create(
                camera_id=candidate.camera_id,
                defaults={"versao_politica_confirmacao": memory.policy_version},
            )
            self._validate_camera_boundary(candidate.camera_id, state.camera_id, "state")
            previous = TechnicalState(state.estado_estavel)
            changed = previous is not memory.state
            updates = {
                "estado_estavel": memory.state.value,
                "ultima_evidencia_util_em": (
                    result.observed_at
                    if decision.disposition is ProcessingDisposition.ACCEPTED
                    else state.ultima_evidencia_util_em
                ),
                "proximo_vencimento_em": next_due_at,
                "ultima_geracao_configuracao": candidate.config_generation,
                "sequencia_positiva": memory.positive_streak,
                "sequencia_negativa": memory.negative_streak,
                "confirmacao_ultima_observacao_em": memory.last_observed_at,
                "versao_politica_confirmacao": memory.policy_version,
                "em_escopo": True,
                "atualizado_em": timezone.now(),
            }
            if changed:
                updates["estado_alterado_em"] = decision.observed_at
            queryset = EstadoMonitoramento.objects.filter(pk=state.pk)
            if ownership is None:
                queryset = queryset.filter(ultima_geracao_configuracao__lte=candidate.config_generation)
            else:
                if not isinstance(ownership, OwnershipLease):
                    raise TypeError("ownership must be an OwnershipLease or None")
                queryset = queryset.filter(
                    monitoring_owner_id=ownership.owner_id,
                    monitoring_ownership_epoch=ownership.epoch,
                    ultima_geracao_configuracao=candidate.config_generation,
                )
                updates.update(
                    monitoring_owner_id=None,
                    monitoring_lease_expires_at=None,
                )
            updated = queryset.update(**updates)
            if updated != 1:
                if ownership is None:
                    return False
                state.refresh_from_db(
                    fields=[
                        "monitoring_owner_id",
                        "monitoring_ownership_epoch",
                        "monitoring_lease_expires_at",
                        "ultima_geracao_configuracao",
                    ]
                )
                owner_is_current = (
                    state.monitoring_owner_id == ownership.owner_id
                    and state.monitoring_ownership_epoch == ownership.epoch
                )
                return (
                    CompletionDisposition.CONFIG_CHANGED
                    if owner_is_current and state.ultima_geracao_configuracao != candidate.config_generation
                    else CompletionDisposition.OWNERSHIP_LOST
                )
            if changed:
                if self._before_transition is not None:
                    self._before_transition()
                transition = TransicaoEstadoMonitoramento.objects.create(
                    camera_id=candidate.camera_id,
                    estado_anterior=previous.value,
                    estado_atual=memory.state.value,
                    ocorrida_em=decision.observed_at,
                )
                self._validate_camera_boundary(state.camera_id, transition.camera_id, "transition")

                if memory.state is TechnicalState.OFFLINE:
                    if previous not in (TechnicalState.UNKNOWN, TechnicalState.ONLINE):
                        raise ValueError("unsupported transition into OFFLINE")
                    open_interval = (
                        Indisponibilidade.objects.select_for_update()
                        .filter(camera_id=state.camera_id, closed_at__isnull=True)
                        .first()
                    )
                    if open_interval is not None:
                        self._validate_camera_boundary(state.camera_id, open_interval.camera_id, "open interval")
                        raise ValueError("camera already has an open unavailability interval")
                    origin = (
                        Indisponibilidade.OrigemAbertura.INITIAL_OFFLINE
                        if previous is TechnicalState.UNKNOWN
                        else Indisponibilidade.OrigemAbertura.ONLINE_TO_OFFLINE
                    )
                    interval = Indisponibilidade.objects.create(
                        camera_id=state.camera_id,
                        opened_at=decision.observed_at,
                        open_origin=origin,
                        opening_transition=transition,
                    )
                    self._validate_camera_boundary(state.camera_id, interval.camera_id, "opened interval")
                    self._validate_camera_boundary(state.camera_id, interval.opening_transition.camera_id, "opening transition")
                elif memory.state is TechnicalState.ONLINE and previous is TechnicalState.OFFLINE:
                    open_interval = (
                        Indisponibilidade.objects.select_for_update()
                        .filter(camera_id=state.camera_id, closed_at__isnull=True)
                        .first()
                    )
                    if open_interval is None:
                        raise ValueError("offline state has no open unavailability interval")
                    self._validate_camera_boundary(state.camera_id, open_interval.camera_id, "open interval")
                    self._validate_camera_boundary(
                        state.camera_id,
                        open_interval.opening_transition.camera_id,
                        "opening transition",
                    )
                    open_interval.closed_at = decision.observed_at
                    open_interval.close_reason = Indisponibilidade.MotivoFechamento.RECUPERADA
                    open_interval.closing_transition = transition
                    open_interval.save(
                        update_fields=[
                            "closed_at",
                            "close_reason",
                            "closing_transition",
                            "updated_at",
                        ]
                    )
                elif not (previous is TechnicalState.UNKNOWN and memory.state is TechnicalState.ONLINE):
                    raise ValueError("unsupported stable monitoring transition")
        return CompletionDisposition.ACCEPTED if ownership is not None else True

    def leave_scope(self, camera_id: int, occurred_at: datetime) -> None:
        """Fecha o intervalo aberto e marca retirada administrativa atomicamente."""

        occurred_at = self._utc_timestamp(occurred_at, "occurred_at")
        with transaction.atomic():
            state, _ = EstadoMonitoramento.objects.select_for_update().get_or_create(camera_id=camera_id)
            self._validate_camera_boundary(camera_id, state.camera_id, "state")
            open_interval = (
                Indisponibilidade.objects.select_for_update()
                .filter(camera_id=state.camera_id, closed_at__isnull=True)
                .first()
            )
            if open_interval is not None:
                self._validate_camera_boundary(state.camera_id, open_interval.camera_id, "open interval")
                open_interval.closed_at = occurred_at
                open_interval.close_reason = Indisponibilidade.MotivoFechamento.SAIU_DO_ESCOPO
                open_interval.closing_transition = None
                open_interval.save(update_fields=["closed_at", "close_reason", "closing_transition", "updated_at"])
            if state.em_escopo:
                state.em_escopo = False
                state.save(update_fields=["em_escopo", "atualizado_em"])

    def enter_scope(self, camera_id: int, now: datetime | None = None) -> None:
        """Retorno ao escopo reinicia a verdade corrente como UNKNOWN."""

        now = timezone.now() if now is None else now
        with transaction.atomic():
            state, _ = EstadoMonitoramento.objects.select_for_update().get_or_create(camera_id=camera_id)
            state.estado_estavel = TechnicalState.UNKNOWN.value
            state.estado_alterado_em = now
            state.sequencia_positiva = 0
            state.sequencia_negativa = 0
            state.confirmacao_ultima_observacao_em = None
            state.ultima_evidencia_util_em = None
            state.em_escopo = True
            state.save()


def is_evidence_stale(last_usable_evidence_at: datetime | None, now: datetime, stale_after: timedelta) -> bool:
    """Freshness derivada; jamais grava ou converte o estado técnico."""

    if last_usable_evidence_at is None:
        return True
    return now - last_usable_evidence_at >= stale_after


__all__ = ["DjangoMonitoringRepository", "is_evidence_stale"]
