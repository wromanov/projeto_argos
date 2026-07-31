from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .models import PerfilUsuario


class ArgosAuthenticationForm(AuthenticationForm):
    error_messages = {"invalid_login": "Usuário ou senha inválidos.", "inactive": "Usuário ou senha inválidos."}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Usuário"
        self.fields["username"].widget.attrs.update({"class": "auth-input", "autocomplete": "username", "autofocus": True, "placeholder": "Usuário"})
        self.fields["password"].label = "Senha"
        self.fields["password"].widget.attrs.update({"class": "auth-input", "autocomplete": "current-password", "placeholder": "Senha"})


class DadosPessoaisForm(forms.ModelForm):
    first_name = forms.CharField(label="Nome", required=True, widget=forms.TextInput(attrs={"class": "profile-input", "autocomplete": "given-name"}))
    last_name = forms.CharField(label="Sobrenome", required=True, widget=forms.TextInput(attrs={"class": "profile-input", "autocomplete": "family-name"}))
    email = forms.EmailField(label="E-mail", required=True, widget=forms.EmailInput(attrs={"class": "profile-input", "autocomplete": "email"}))

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email")

    def clean_first_name(self):
        valor = self.cleaned_data["first_name"].strip()
        if not valor: raise forms.ValidationError("Informe o nome.")
        return valor

    def clean_last_name(self):
        valor = self.cleaned_data["last_name"].strip()
        if not valor: raise forms.ValidationError("Informe o sobrenome.")
        return valor

    def clean_email(self):
        valor = self.cleaned_data["email"].strip().lower()
        if not valor: raise forms.ValidationError("Informe o e-mail.")
        return valor


class PerfilProprioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ("telefone", "ramal")
        widgets = {"telefone": forms.TextInput(attrs={"class": "profile-input", "autocomplete": "tel", "placeholder": "Telefone para contato"}), "ramal": forms.TextInput(attrs={"class": "profile-input", "autocomplete": "off", "placeholder": "Ramal corporativo"})}

    def clean_telefone(self): return self.cleaned_data["telefone"].strip()
    def clean_ramal(self): return self.cleaned_data["ramal"].strip()


class ArgosPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        configuracao = {"old_password": ("Senha atual", "current-password"), "new_password1": ("Nova senha", "new-password"), "new_password2": ("Confirmar nova senha", "new-password")}
        for campo, (label, autocomplete) in configuracao.items():
            self.fields[campo].label = label
            self.fields[campo].widget.attrs.update({"class": "profile-input", "autocomplete": autocomplete})
