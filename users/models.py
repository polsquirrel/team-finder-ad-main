from django.contrib.auth.models import AbstractUser
from django.db import models

from users.constants import (
    USER_ABOUT_MAX_LENGTH,
    USER_NAME_MAX_LENGTH,
    USER_PHONE_MAX_LENGTH,
    USER_SURNAME_MAX_LENGTH,
)
from users.managers import UserManager
from users.utils import build_default_avatar, has_uploaded_avatar


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name="Email")
    name = models.CharField(max_length=USER_NAME_MAX_LENGTH, verbose_name="Имя")
    surname = models.CharField(max_length=USER_SURNAME_MAX_LENGTH, verbose_name="Фамилия")
    avatar = models.ImageField(upload_to="avatars/", verbose_name="Аватар")
    phone = models.CharField(max_length=USER_PHONE_MAX_LENGTH, verbose_name="Телефон")
    github_url = models.URLField(blank=True, verbose_name="GitHub")
    about = models.TextField(max_length=USER_ABOUT_MAX_LENGTH, blank=True, verbose_name="О себе")
    skills = models.ManyToManyField("projects.Skill", related_name="users", blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]
    objects = UserManager()

    def __str__(self):
        return f"{self.name} {self.surname}"

    def save(self, *args, **kwargs):
        if self.pk is None and not has_uploaded_avatar(self):
            self.avatar = build_default_avatar(self)
        super().save(*args, **kwargs)
