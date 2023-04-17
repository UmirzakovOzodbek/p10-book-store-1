from django import forms
from django.contrib.auth.forms import UsernameField
from django.utils.translation import gettext_lazy as _

from account.models import User


class CustomAuthenticationForm(forms.Form):
    username = UsernameField(
        widget=forms.TextInput(attrs={"autofocus": True})
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))
    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
        "username_unique": _("Username already taken."),
    }

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean(self):
        data = self.cleaned_data
        username = self.cleaned_data.get("username")
        if username and self._meta.model.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(self.error_messages.get("username_unique"))
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError(self.error_messages.get("password_mismatch"))
        return data


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "phone_number", "birth_date", "profile_picture")
