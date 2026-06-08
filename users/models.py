import random
from io import BytesIO

from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageDraw, ImageFont

from users.constants import (
    AVATAR_COLORS,
    AVATAR_FONT_SIZE,
    AVATAR_SIZE,
    AVATAR_TEXT_COLOR,
    USER_ABOUT_MAX_LENGTH,
    USER_NAME_MAX_LENGTH,
    USER_PHONE_MAX_LENGTH,
    USER_SURNAME_MAX_LENGTH,
)
from users.managers import UserManager


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
        if self.pk is None and not self._has_uploaded_avatar():
            self.avatar = self._build_default_avatar()
        super().save(*args, **kwargs)

    def _has_uploaded_avatar(self):
        if not self.avatar:
            return False
        return bool(getattr(self.avatar, "name", None))

    def _build_default_avatar(self):
        background_color = random.choice(AVATAR_COLORS)
        canvas = Image.new("RGB", (AVATAR_SIZE, AVATAR_SIZE), background_color)
        painter = ImageDraw.Draw(canvas)
        letter_font = self._resolve_avatar_font()
        initial = self.name[0].upper() if self.name else "?"
        text_position = self._calculate_text_position(painter, initial, letter_font)
        painter.text(text_position, initial, fill=AVATAR_TEXT_COLOR, font=letter_font)
        return self._save_image_to_file(canvas)

    def _resolve_avatar_font(self):
        try:
            return ImageFont.truetype("arial.ttf", AVATAR_FONT_SIZE)
        except Exception:
            return ImageFont.load_default()

    def _calculate_text_position(self, painter, text, letter_font):
        bounds = painter.textbbox((0, 0), text, font=letter_font)
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        x_offset = (AVATAR_SIZE - width) // 2
        y_offset = (AVATAR_SIZE - height) // 2
        return (x_offset, y_offset)

    def _save_image_to_file(self, canvas):
        image_buffer = BytesIO()
        canvas.save(image_buffer, format="PNG")
        image_buffer.seek(0)
        filename = f"avatar_{self.email}.png"
        return ContentFile(image_buffer.read(), name=filename)
