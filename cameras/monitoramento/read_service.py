"""Camada canônica, somente leitura, do monitoramento técnico.

Este módulo projeta dados persistidos para consumo de apresentação. Ele não
executa probes, persiste estado, consulta auditoria ou expõe detalhes de
configuração técnica.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum
from django.db.models import BooleanField, Case, CharField, Count, Exists, F, OuterRef, Q, Subquery, Value, When
from django.db.models.functions import Coalesce
from django.db.models.query import QuerySet
from django.utils import timezone

from cameras.governanca import q_camera_completa
from cameras.models import Camera, EstadoMonitoramento, Indisponibilidade

from .repository import is_evidence_stale
from .schemas import MonitoringConfig


class MonitoringFreshness(StrEnum):
    FRESH = "fresh"
    STALE = "stale"


class MonitoringEffectiveState(StrEnum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    UNKNOWN = "UNKNOWN"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"


class MonitoringScopeReason(StrEnum):
    OUT_OF_SCOPE = "OUT_OF_SCOPE"
    INCOMPLETE_CONFIGURATION = "INCOMPLETE_CONFIGURATION"


@dataclass(frozen=True, slots=True)
class OpenOutageProjection:
    """Allowlist da indisponibilidade atualmente aberta."""

    id: int
    opened_at: datetime
    open_origin: str


@dataclass(frozen=True, slots=True)
class OutageHistoryProjection:
    """Allowlist paginável do histórico técnico por câmera."""

    id: int
    opened_at: datetime
    closed_at: datetime | None
    open_origin: str
    close_reason: str | None

    @property
    def duration(self) -> timedelta | None:
        if self.closed_at is None:
            return None
        return self.closed_at - self.opened_at


@dataclass(frozen=True, slots=True)
class MonitoringProjection:
    """Contrato visual mínimo para o estado atual de uma câmera."""

    camera_id: int
    stable_state: str
    freshness: MonitoringFreshness
    em_escopo: bool
    effective_state: MonitoringEffectiveState
    evidence_at: datetime | None
    state_since: datetime | None
    scope_reason: MonitoringScopeReason | None
    open_outage: OpenOutageProjection | None

    @property
    def is_stale(self) -> bool:
        return self.freshness is MonitoringFreshness.STALE


@dataclass(frozen=True, slots=True)
class MonitoringAggregate:
    """Agregados canônicos calculados pelo banco."""

    total: int
    in_scope: int
    out_of_scope: int
    online: int
    offline: int
    unknown: int
    fresh: int
    stale: int
    open_outages: int


@dataclass(frozen=True, slots=True)
class OutageHistoryPage:
    items: tuple[OutageHistoryProjection, ...]
    total: int
    limit: int
    offset: int


class MonitoringReadService:
    """Boundary ORM de leitura canônica do monitoramento.

    A query de câmeras sempre carrega o estado 1:1 e projeta, por subquery,
    apenas a indisponibilidade aberta mais recente. Nenhum método deste
    serviço altera o banco.
    """

    MAX_HISTORY_LIMIT = 100

    def __init__(self, *, config: MonitoringConfig | None = None, now=None) -> None:
        self.config = config or MonitoringConfig()
        self._now = now or timezone.now

    @property
    def stale_after(self) -> timedelta:
        return timedelta(seconds=self.config.stale_after_seconds)

    @staticmethod
    def _open_outages() -> QuerySet:
        return Indisponibilidade.objects.filter(
            camera_id=OuterRef("pk"), closed_at__isnull=True
        ).order_by("-opened_at", "-pk")

    @classmethod
    def camera_queryset(cls, queryset: QuerySet | None = None) -> QuerySet:
        """Retorna câmeras anotadas para uma leitura batched e segura."""

        queryset = Camera.objects.all() if queryset is None else queryset
        open_outages = cls._open_outages()
        return queryset.select_related("estado_monitoramento").annotate(
            monitoring_open_outage_id=Subquery(open_outages.values("pk")[:1]),
            monitoring_opened_at=Subquery(open_outages.values("opened_at")[:1]),
            monitoring_open_origin=Subquery(open_outages.values("open_origin")[:1]),
        )

    def project(self, camera: Camera) -> MonitoringProjection:
        """Converte uma câmera já carregada pela ``camera_queryset``."""

        state = self._state_from_camera(camera)
        eligible = (
            camera.situacao_operacional == Camera.SituacaoOperacional.PRODUCAO
            and camera.cadastro_completo
        )
        state_in_scope = True if state is None else state.em_escopo
        em_escopo = eligible and state_in_scope

        if not eligible:
            scope_reason = (
                MonitoringScopeReason.INCOMPLETE_CONFIGURATION
                if camera.situacao_operacional == Camera.SituacaoOperacional.PRODUCAO
                else MonitoringScopeReason.OUT_OF_SCOPE
            )
        elif not state_in_scope:
            scope_reason = MonitoringScopeReason.OUT_OF_SCOPE
        else:
            scope_reason = None

        stable_state = (
            state.estado_estavel if state is not None else EstadoMonitoramento.EstadoEstavel.UNKNOWN
        )
        evidence_at = state.ultima_evidencia_util_em if state is not None else None
        freshness = (
            MonitoringFreshness.STALE
            if is_evidence_stale(evidence_at, self._now(), self.stale_after)
            else MonitoringFreshness.FRESH
        )
        if not em_escopo:
            effective_state = MonitoringEffectiveState.OUT_OF_SCOPE
        elif freshness is MonitoringFreshness.STALE:
            effective_state = MonitoringEffectiveState.UNKNOWN
        else:
            effective_state = MonitoringEffectiveState(stable_state)
        open_outage = self._open_outage_from_annotation(camera) if em_escopo else None

        return MonitoringProjection(
            camera_id=camera.pk,
            stable_state=str(stable_state),
            freshness=freshness,
            em_escopo=em_escopo,
            effective_state=effective_state,
            evidence_at=evidence_at,
            state_since=state.estado_alterado_em if state is not None else None,
            scope_reason=scope_reason,
            open_outage=open_outage,
        )

    def projections(self, queryset: QuerySet) -> tuple[MonitoringProjection, ...]:
        """Materializa somente as câmeras da página já limitada pelo chamador."""

        return tuple(self.project(camera) for camera in self.camera_queryset(queryset))

    def current(self, camera_id: int, queryset: QuerySet | None = None) -> MonitoringProjection:
        camera = self.camera_queryset(queryset).get(pk=camera_id)
        return self.project(camera)

    @staticmethod
    def _history_queryset(camera_id: int) -> QuerySet:
        """Query ordenada interna, sem carregar todo o histórico."""

        return Indisponibilidade.objects.filter(camera_id=camera_id).only(
            "pk", "camera_id", "opened_at", "closed_at", "open_origin", "close_reason"
        ).order_by("-opened_at", "-pk")

    def history_page(self, camera_id: int, *, limit: int = 5, offset: int = 0) -> OutageHistoryPage:
        if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= self.MAX_HISTORY_LIMIT:
            raise ValueError(f"limit must be between 1 and {self.MAX_HISTORY_LIMIT}")
        if isinstance(offset, bool) or not isinstance(offset, int) or offset < 0:
            raise ValueError("offset must be a non-negative integer")
        queryset = self._history_queryset(camera_id)
        rows = queryset[offset:offset + limit]
        items = tuple(
            OutageHistoryProjection(
                id=row.pk,
                opened_at=row.opened_at,
                closed_at=row.closed_at,
                open_origin=row.open_origin,
                close_reason=row.close_reason,
            )
            for row in rows
        )
        return OutageHistoryPage(items=items, total=queryset.count(), limit=limit, offset=offset)

    def aggregate(self, queryset: QuerySet | None = None, *, now: datetime | None = None) -> MonitoringAggregate:
        """Calcula contadores canônicos em uma agregação SQL, sem materializar câmeras."""

        queryset = self.camera_queryset(queryset)
        state = EstadoMonitoramento.objects.filter(camera_id=OuterRef("pk"))
        open_outages = self._open_outages()
        queryset = queryset.annotate(
            monitoring_stable_state=Coalesce(
                Subquery(state.values("estado_estavel")[:1]),
                Value(EstadoMonitoramento.EstadoEstavel.UNKNOWN),
                output_field=CharField(max_length=7),
            ),
            monitoring_state_in_scope=Coalesce(
                Subquery(state.values("em_escopo")[:1]),
                Value(True),
                output_field=BooleanField(),
            ),
            monitoring_evidence_at=Subquery(state.values("ultima_evidencia_util_em")[:1]),
            monitoring_has_open_outage=Exists(open_outages),
        )
        eligible = Q(situacao_operacional=Camera.SituacaoOperacional.PRODUCAO) & q_camera_completa()
        # As Cases são avaliadas pelo banco para manter a semântica fora do
        # escopo separada do stable state persistido.
        queryset = queryset.annotate(
            monitoring_in_scope=Case(
                When(eligible & Q(monitoring_state_in_scope=True), then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
            monitoring_freshness=Case(
                When(monitoring_evidence_at__isnull=True, then=Value(MonitoringFreshness.STALE)),
                When(
                    monitoring_evidence_at__lte=(now or self._now()) - self.stale_after,
                    then=Value(MonitoringFreshness.STALE),
                ),
                default=Value(MonitoringFreshness.FRESH),
                output_field=CharField(max_length=5),
            ),
            monitoring_effective_state=Case(
                When(monitoring_in_scope=False, then=Value(MonitoringEffectiveState.OUT_OF_SCOPE)),
                When(
                    monitoring_freshness=MonitoringFreshness.FRESH,
                    then=F("monitoring_stable_state"),
                ),
                default=Value(MonitoringEffectiveState.UNKNOWN),
                output_field=CharField(max_length=12),
            ),
        )
        values = queryset.aggregate(
            total=Count("pk"),
            in_scope=Count("pk", filter=Q(monitoring_in_scope=True)),
            out_of_scope=Count("pk", filter=Q(monitoring_in_scope=False)),
            online=Count("pk", filter=Q(monitoring_effective_state=MonitoringEffectiveState.ONLINE)),
            offline=Count("pk", filter=Q(monitoring_effective_state=MonitoringEffectiveState.OFFLINE)),
            unknown=Count("pk", filter=Q(monitoring_effective_state=MonitoringEffectiveState.UNKNOWN)),
            fresh=Count("pk", filter=Q(monitoring_in_scope=True, monitoring_freshness=MonitoringFreshness.FRESH)),
            stale=Count("pk", filter=Q(monitoring_in_scope=True, monitoring_freshness=MonitoringFreshness.STALE)),
            open_outages=Count("pk", filter=Q(monitoring_in_scope=True, monitoring_has_open_outage=True)),
        )
        return MonitoringAggregate(**{field: values[field] or 0 for field in MonitoringAggregate.__dataclass_fields__})

    @staticmethod
    def _state_from_camera(camera: Camera) -> EstadoMonitoramento | None:
        try:
            return camera.estado_monitoramento
        except EstadoMonitoramento.DoesNotExist:
            return None

    @staticmethod
    def _open_outage_from_annotation(camera: Camera) -> OpenOutageProjection | None:
        opened_at = getattr(camera, "monitoring_opened_at", None)
        outage_id = getattr(camera, "monitoring_open_outage_id", None)
        if outage_id is None or opened_at is None:
            return None
        return OpenOutageProjection(
            id=outage_id,
            opened_at=opened_at,
            open_origin=getattr(camera, "monitoring_open_origin"),
        )


__all__ = [
    "MonitoringAggregate",
    "MonitoringEffectiveState",
    "MonitoringFreshness",
    "MonitoringProjection",
    "MonitoringReadService",
    "MonitoringScopeReason",
    "OpenOutageProjection",
    "OutageHistoryPage",
    "OutageHistoryProjection",
]
