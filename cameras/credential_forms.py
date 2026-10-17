"""Allowlisted forms for camera credential mutations."""

from django import forms


class CameraCredentialReplaceForm(forms.Form):
    username = forms.CharField(max_length=255, strip=False)
    password = forms.CharField(max_length=1024, strip=False, widget=forms.PasswordInput(render_value=False))


class CameraCredentialRevokeFallbackForm(forms.Form):
    confirm_unsaved_changes = forms.BooleanField(required=True)
