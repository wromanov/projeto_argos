from django.contrib.auth.forms import AuthenticationForm


class ArgosAuthenticationForm(AuthenticationForm):
    error_messages = {"invalid_login": "Usuário ou senha inválidos.", "inactive": "Usuário ou senha inválidos."}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Usuário"
        self.fields["username"].widget.attrs.update({"class": "auth-input", "autocomplete": "username", "autofocus": True, "placeholder": "Usuário"})
        self.fields["password"].label = "Senha"
        self.fields["password"].widget.attrs.update({"class": "auth-input", "autocomplete": "current-password", "placeholder": "Senha"})
