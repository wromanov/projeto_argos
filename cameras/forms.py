from django import forms

from .models import AtividadeCamera, Camera


class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = (
            "patrimonio",
            "nome",
            "fabricante",
            "modelo",
            "serial",
            "mac",
            "tipo",
            "ativo",
            "terminal",
            "pavimento",
            "setor",
            "ambiente",
            "descricao_detalhada",
            "ponto_referencia",
            "ip",
            "mascara_subrede",
            "gateway",
            "vlan",
            "farm",
            "retencao_esperada_dias",
            "codec",
            "origem_cadastro",
            "observacoes",
        )
        widgets = {
            "patrimonio": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex.: PAT-CFTV-0002"}),
            "nome": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex.: EST-TPS2-CM80"}),
            "fabricante": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex.: Axis"}),
            "modelo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex.: P3265-LVE"}),
            "serial": forms.TextInput(attrs={"class": "form-control", "placeholder": "Número de série"}),
            "mac": forms.TextInput(attrs={"class": "form-control", "placeholder": "AA:BB:CC:DD:EE:FF"}),
            "tipo": forms.Select(attrs={"class": "form-control"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "terminal": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex.: TPS2"}),
            "pavimento": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex.: Embarque"}),
            "setor": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex.: Check-in"}),
            "ambiente": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex.: Saguão"}),
            "descricao_detalhada": forms.Textarea(attrs={"class": "form-control", "placeholder": "Descreva a instalação", "rows": 4}),
            "ponto_referencia": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex.: Próxima ao balcão 20"}),
            "ip": forms.TextInput(attrs={"class": "form-control", "placeholder": "10.20.78.20"}),
            "mascara_subrede": forms.TextInput(attrs={"class": "form-control", "placeholder": "255.255.255.0"}),
            "gateway": forms.TextInput(attrs={"class": "form-control", "placeholder": "10.20.78.1"}),
            "vlan": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Ex.: 210"}),
            "farm": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex.: FARM-TPS2-01"}),
            "retencao_esperada_dias": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Ex.: 30"}),
            "codec": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex.: H.264"}),
            "origem_cadastro": forms.Select(attrs={"class": "form-control"}),
            "observacoes": forms.Textarea(attrs={"class": "form-control", "placeholder": "Informações complementares", "rows": 4}),
        }

    def clean_mac(self):
        mac = self.cleaned_data.get("mac")
        if not mac:
            return mac
        return mac.strip().upper()


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
