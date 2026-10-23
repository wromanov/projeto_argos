from dataclasses import dataclass

from django.db.models import Q, QuerySet
from django.http import QueryDict

from .governanca import q_camera_completa, q_camera_incompleta
from .models import Camera
from .validadores import normalizar_texto_cadastral


ORDENACOES_PERMITIDAS = {
    "nome", "-nome", "status", "-status", "ip", "-ip",
    "atualizado_em", "-atualizado_em",
}
STATUS_INVENTARIO_PERMITIDOS = {"ONLINE", "OFFLINE", "NAO_VERIFICADO"}
COMPLETUDES_PERMITIDAS = {"COMPLETO", "INCOMPLETO"}


def _valores_get_unicos(params, nome, normalizar=False):
    valores = []
    for bruto in params.getlist(nome):
        valor = bruto.strip()
        if not valor:
            continue
        if normalizar:
            valor = normalizar_texto_cadastral(valor)
        if valor and valor not in valores:
            valores.append(valor)
    return tuple(valores)


@dataclass(frozen=True)
class FiltrosInventario:
    q: str
    status: tuple[str, ...]
    situacao_operacional: tuple[str, ...]
    completude: tuple[str, ...]
    terminal: tuple[str, ...]
    tipo: tuple[str, ...]
    fabricante: tuple[str, ...]
    vlan: tuple[str, ...]
    farm: tuple[str, ...]
    ordenacao: str
    incluir_ordenacao_na_url: bool

    @classmethod
    def de_parametros(cls, params):
        status = tuple(
            valor for valor in _valores_get_unicos(params, "status")
            if valor in STATUS_INVENTARIO_PERMITIDOS
        )
        situacoes = tuple(
            valor for valor in _valores_get_unicos(params, "situacao_operacional")
            if valor in Camera.SituacaoOperacional.values
        )
        completudes = tuple(
            valor for valor in _valores_get_unicos(params, "completude")
            if valor in COMPLETUDES_PERMITIDAS
        )
        terminais = _valores_get_unicos(params, "terminal", normalizar=True)
        tipos = tuple(
            valor for valor in _valores_get_unicos(params, "tipo")
            if valor in Camera.TipoCamera.values
        )
        fabricantes = _valores_get_unicos(params, "fabricante", normalizar=True)
        farms = _valores_get_unicos(params, "farm", normalizar=True)

        vlans = []
        for valor in _valores_get_unicos(params, "vlan"):
            try:
                vlan = int(valor)
            except (TypeError, ValueError):
                continue
            if 1 <= vlan <= 4094:
                canonica = str(vlan)
                if canonica not in vlans:
                    vlans.append(canonica)

        ordenacao_solicitada = params.get("ordenacao", "nome")
        ordenacao_valida = ordenacao_solicitada in ORDENACOES_PERMITIDAS
        return cls(
            q=params.get("q", "").strip(),
            status=status,
            situacao_operacional=situacoes,
            completude=completudes,
            terminal=terminais,
            tipo=tipos,
            fabricante=fabricantes,
            vlan=tuple(vlans),
            farm=farms,
            ordenacao=ordenacao_solicitada if ordenacao_valida else "nome",
            incluir_ordenacao_na_url=ordenacao_valida and "ordenacao" in params,
        )

    def aplicar(self, queryset=None) -> QuerySet:
        queryset = Camera.objects.all() if queryset is None else queryset
        if self.q:
            queryset = queryset.filter(
                Q(nome__icontains=self.q) | Q(patrimonio__icontains=self.q)
                | Q(ip__icontains=self.q) | Q(serial__icontains=self.q)
                | Q(mac__icontains=self.q) | Q(fabricante__icontains=self.q)
                | Q(modelo__icontains=self.q) | Q(terminal__icontains=self.q)
                | Q(pavimento__icontains=self.q) | Q(setor__icontains=self.q)
                | Q(ambiente__icontains=self.q) | Q(farm__icontains=self.q)
            )

        if self.status:
            filtro_status = Q()
            status_diretos = [v for v in self.status if v in {"ONLINE", "OFFLINE"}]
            if status_diretos:
                filtro_status |= Q(status__in=status_diretos)
            if "NAO_VERIFICADO" in self.status:
                filtro_status |= Q(status__isnull=True) | Q(status="")
            queryset = queryset.filter(filtro_status)

        if self.situacao_operacional:
            queryset = queryset.filter(situacao_operacional__in=self.situacao_operacional)

        if self.completude:
            filtro_completude = Q()
            if "COMPLETO" in self.completude:
                filtro_completude |= q_camera_completa()
            if "INCOMPLETO" in self.completude:
                filtro_completude |= q_camera_incompleta()
            queryset = queryset.filter(filtro_completude)

        if self.terminal:
            queryset = queryset.filter(terminal__in=self.terminal)
        if self.tipo:
            queryset = queryset.filter(tipo__in=self.tipo)
        if self.fabricante:
            queryset = queryset.filter(fabricante__in=self.fabricante)
        if self.vlan:
            queryset = queryset.filter(vlan__in=[int(valor) for valor in self.vlan])
        if self.farm:
            queryset = queryset.filter(farm__in=self.farm)
        return queryset.order_by(self.ordenacao, "pk")

    def para_querydict(self):
        query = QueryDict(mutable=True)
        parametros = {
            "q": self.q,
            "status": self.status,
            "situacao_operacional": self.situacao_operacional,
            "completude": self.completude,
            "terminal": self.terminal,
            "tipo": self.tipo,
            "fabricante": self.fabricante,
            "vlan": self.vlan,
            "farm": self.farm,
            "ordenacao": self.ordenacao if self.incluir_ordenacao_na_url else (),
        }
        for nome, valores in parametros.items():
            if not isinstance(valores, (list, tuple)):
                valores = (valores,)
            for valor in valores:
                if valor != "":
                    query.appendlist(nome, str(valor))
        return query

    def resumo(self):
        partes = []
        if self.q:
            partes.append("pesquisa textual aplicada")
        if self.status:
            partes.append("status: " + ", ".join(self.status))
        if self.situacao_operacional:
            rotulos = dict(Camera.SituacaoOperacional.choices)
            partes.append("situação operacional: " + ", ".join(rotulos[v] for v in self.situacao_operacional))
        if self.completude:
            partes.append("completude: " + ", ".join(self.completude))
        for rotulo, valores in (
            ("terminal", self.terminal), ("tipo", self.tipo),
            ("fabricante", self.fabricante), ("VLAN", self.vlan), ("farm", self.farm),
        ):
            if valores:
                partes.append(f"{rotulo}: " + ", ".join(valores))
        return tuple(partes)
