from django import forms

from .catalogos import (
    FARM_CHOICES,
    FARMS_CATALOGO,
    VALOR_PERSONALIZADO,
)
from .models import AtividadeCamera, Camera
from .validadores import normalizar_mac, normalizar_texto_cadastral


CAMPOS_CAMERA = (
    "patrimonio", "nome", "fabricante", "modelo", "serial", "mac", "tipo",
    "terminal", "pavimento", "setor", "ambiente", "descricao_detalhada",
    "ponto_referencia", "ip", "mascara_subrede", "gateway", "vlan", "farm",
    "retencao_esperada_dias", "codec", "origem_cadastro", "observacoes",
)


class EscolhaTextoNormalizadaField(forms.ChoiceField):
    """
    ChoiceField que normaliza texto antes de validar as choices.

    Mantem compatibilidade com entradas legadas contendo
    espacos nas extremidades ou diferenca de caixa.
    """

    def clean(self, value):
        if value not in self.empty_values:
            value = normalizar_texto_cadastral(value)

        return super().clean(value)


class CameraBaseForm(forms.ModelForm):
    farm_personalizado = forms.CharField(
        required=False,
        label="Farm personalizada",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autocomplete": "off",
            }
        ),
    )
    class Meta:
        model = Camera
        fields = CAMPOS_CAMERA
        widgets = {
            campo: forms.Textarea(attrs={"class": "form-control", "rows": 4})
            if campo in ("descricao_detalhada", "observacoes")
            else forms.Select(attrs={"class": "form-control"})
            if campo in ("tipo", "origem_cadastro")
            else forms.NumberInput(attrs={"class": "form-control"})
            if campo in ("vlan", "retencao_esperada_dias")
            else forms.TextInput(attrs={"class": "form-control"})
            for campo in CAMPOS_CAMERA
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["farm"] = EscolhaTextoNormalizadaField(
            required=False,
            label="Farm",
            choices=FARM_CHOICES,
            widget=forms.Select(
                attrs={
                    "class": "form-control",
                    "data-farm-select": "",
                    "aria-controls": (
                        "farm-personalizado-container"
                    ),
                }
            ),
        )

        if self.is_bound:
            return

        valor_atual = normalizar_texto_cadastral(
            self.initial.get("farm")
        )

        if not valor_atual:
            self.initial["farm"] = ""
            self.initial["farm_personalizado"] = ""
            return

        if valor_atual in FARMS_CATALOGO:
            self.initial["farm"] = valor_atual
            self.initial["farm_personalizado"] = ""
            return

        self.initial["farm"] = VALOR_PERSONALIZADO
        self.initial["farm_personalizado"] = valor_atual

    def clean_mac(self):
        return normalizar_mac(self.cleaned_data.get("mac"))

    def clean(self):
        cleaned = super().clean()

        farm_selecionada = cleaned.get("farm")

        if farm_selecionada == VALOR_PERSONALIZADO:
            farm_personalizada = normalizar_texto_cadastral(
                cleaned.get("farm_personalizado")
            )

            if not farm_personalizada:
                self.add_error(
                    "farm_personalizado",
                    "Informe a farm personalizada.",
                )
                cleaned["farm"] = ""

            elif farm_personalizada == "PERSONALIZADO":
                self.add_error(
                    "farm_personalizado",
                    "Informe o nome real da farm.",
                )
                cleaned["farm"] = ""

            else:
                cleaned["farm"] = farm_personalizada

        elif farm_selecionada is not None:
            cleaned["farm"] = normalizar_texto_cadastral(
                farm_selecionada
            )

        for campo in Camera.CAMPOS_CAIXA_ALTA:
            if campo not in cleaned:
                continue

            valor = normalizar_texto_cadastral(
                cleaned[campo]
            )

            if (
                campo in ("patrimonio", "serial")
                and valor == ""
            ):
                valor = None

            cleaned[campo] = valor

        if not self.errors:
            for campo, valor in cleaned.items():
                if hasattr(self.instance, campo):
                    setattr(self.instance, campo, valor)

            situacao = cleaned.get(
                "situacao_operacional",
                self.instance.situacao_operacional,
            )

            faltantes = self.instance.campos_incompletos(
                situacao
            )

            if faltantes:
                rotulos = ", ".join(
                    str(
                        self.instance
                        ._meta
                        .get_field(campo)
                        .verbose_name
                    )
                    for campo in faltantes
                )

                raise forms.ValidationError(
                    "Complete os seguintes campos "
                    f"antes de continuar: {rotulos}."
                )

        return cleaned


class CameraCriacaoForm(CameraBaseForm):
    situacao_operacional = forms.ChoiceField(
        choices=(
            (Camera.SituacaoOperacional.PRODUCAO, "Produção"),
            (Camera.SituacaoOperacional.ESTOQUE, "Estoque"),
        ),
        label="Situação operacional",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta(CameraBaseForm.Meta):
        fields = ("situacao_operacional",) + CAMPOS_CAMERA


class CameraEdicaoForm(CameraBaseForm):
    pass


CameraForm = CameraEdicaoForm


class DesativarCameraForm(forms.Form):
    motivo = forms.CharField(label="Motivo da desativação", min_length=10, max_length=500, strip=True, widget=forms.Textarea(attrs={"class": "form-control", "rows": 5}))


class ReativarCameraForm(forms.Form):
    destino = forms.ChoiceField(choices=((Camera.SituacaoOperacional.PRODUCAO, "Produção"), (Camera.SituacaoOperacional.ESTOQUE, "Estoque")), widget=forms.Select(attrs={"class": "form-control"}))
    justificativa = forms.CharField(min_length=10, max_length=500, strip=True, widget=forms.Textarea(attrs={"class": "form-control", "rows": 5}))


class AlterarSituacaoCameraForm(forms.Form):
    destino = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}))
    justificativa = forms.CharField(min_length=10, max_length=500, strip=True, widget=forms.Textarea(attrs={"class": "form-control", "rows": 5}))

    def __init__(self, *args, camera=None, **kwargs):
        super().__init__(*args, **kwargs)
        if camera is None or camera.situacao_operacional == Camera.SituacaoOperacional.DESATIVADA:
            self.fields["destino"].choices = ()
        elif camera.situacao_operacional == Camera.SituacaoOperacional.PRODUCAO:
            self.fields["destino"].choices = ((Camera.SituacaoOperacional.ESTOQUE, "Estoque"),)
        else:
            self.fields["destino"].choices = ((Camera.SituacaoOperacional.PRODUCAO, "Produção"),)


class SubstituirCameraForm(forms.Form):
    camera_substituta = forms.ModelChoiceField(queryset=Camera.objects.none(), widget=forms.Select(attrs={"class": "form-control"}))
    motivo = forms.CharField(min_length=10, max_length=1000, strip=True, widget=forms.Textarea(attrs={"class": "form-control", "rows": 5}))
    observacoes = forms.CharField(required=False, strip=True, widget=forms.Textarea(attrs={"class": "form-control", "rows": 4}))

    def __init__(self, *args, camera_anterior=None, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = Camera.objects.filter(situacao_operacional=Camera.SituacaoOperacional.ESTOQUE).order_by("nome")
        if camera_anterior is not None:
            queryset = queryset.exclude(pk=camera_anterior.pk)
        self.fields["camera_substituta"].queryset = queryset


class AtividadeCameraForm(forms.ModelForm):
    class Meta:
        model = AtividadeCamera
        fields = ("tipo", "titulo", "descricao", "ocorrida_em", "responsavel")
        widgets = {
            "tipo": forms.Select(attrs={"class": "form-control"}),
            "titulo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Resumo da atividade"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 6, "placeholder": "Descreva o que aconteceu com a câmera"}),
            "ocorrida_em": forms.DateTimeInput(format="%Y-%m-%dT%H:%M", attrs={"class": "form-control", "type": "datetime-local"}),
            "responsavel": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nome do responsável, equipe ou empresa"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ocorrida_em"].input_formats = ["%Y-%m-%dT%H:%M"]