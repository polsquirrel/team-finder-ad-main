from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

from projects.forms import BaseGithubForm

UserModel = get_user_model()

DUPLICATE_EMAIL_MSG = "Пользователь с таким email уже существует"
DUPLICATE_PHONE_MSG = "Этот номер телефона уже используется"
PHONE_FORMAT_MSG = "Номер телефона должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX"
PHONE_REQUIRED_MSG = "Телефон обязателен для заполнения"


def _normalize_russian_phone(raw_phone):
    if raw_phone.startswith("8"):
        return "+7" + raw_phone[1:]
    return raw_phone


def _is_valid_russian_phone(phone):
    return (
        phone.startswith("+7")
        and len(phone) == 12
        and phone[2:].isdigit()
    )


def _validate_phone(phone_value, exclude_user_id=None):
    if not phone_value:
        raise forms.ValidationError(PHONE_REQUIRED_MSG)

    normalized = _normalize_russian_phone(phone_value.strip())
    if not _is_valid_russian_phone(normalized):
        raise forms.ValidationError(PHONE_FORMAT_MSG)

    phone_queryset = UserModel.objects.filter(phone=normalized)
    if exclude_user_id is not None:
        phone_queryset = phone_queryset.exclude(id=exclude_user_id)
    if phone_queryset.exists():
        raise forms.ValidationError(DUPLICATE_PHONE_MSG)

    return normalized


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
