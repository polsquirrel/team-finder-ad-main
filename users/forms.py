from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

from projects.forms import BaseGithubForm
from users.utils import _validate_phone 
from users.constants import (
    DUPLICATE_EMAIL_MSG,
)

UserModel = get_user_model()

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    class Meta:
        model = UserModel
        fields = ("name", "surname", "email", "phone", "password")

    def clean_email(self):
        email_value = self.cleaned_data.get("email")
        if UserModel.objects.filter(email=email_value).exists():
            raise forms.ValidationError(DUPLICATE_EMAIL_MSG)
        return email_value

    def clean_phone(self):
        return _validate_phone(self.cleaned_data.get("phone"))


class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Email"


class ProfileEditForm(BaseGithubForm):
    class Meta:
        model = UserModel
        fields = ("name", "surname", "avatar", "about", "phone", "github_url")
        widgets = {"about": forms.Textarea(attrs={"rows": 4})}

    def clean_phone(self):
        return _validate_phone(
            self.cleaned_data.get("phone"),
            exclude_user_id=self.instance.id,
        )
