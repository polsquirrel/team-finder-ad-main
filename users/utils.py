import random
from io import BytesIO

from django import forms
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

from users.constants import (
    AVATAR_COLORS,
    AVATAR_FONT_SIZE,
    AVATAR_SIZE,
    AVATAR_TEXT_COLOR,
    DUPLICATE_PHONE_MSG,
    PHONE_FORMAT_MSG,
    PHONE_REQUIRED_MSG,
)


def _normalize_russian_phone(raw_phone):
    if raw_phone.startswith("8"):
        return "+7" + raw_phone[1:]
    return raw_phone


def _is_valid_russian_phone(phone):
    return phone.startswith("+7") and len(phone) == 12 and phone[2:].isdigit()


def _validate_phone(phone_value, exclude_user_id=None):
    if not phone_value:
        raise forms.ValidationError(PHONE_REQUIRED_MSG)

    normalized = _normalize_russian_phone(phone_value.strip())
    if not _is_valid_russian_phone(normalized):
        raise forms.ValidationError(PHONE_FORMAT_MSG)

    user_model = get_user_model()
    phone_queryset = user_model.objects.filter(phone=normalized)
    if exclude_user_id is not None:
        phone_queryset = phone_queryset.exclude(id=exclude_user_id)
    if phone_queryset.exists():
        raise forms.ValidationError(DUPLICATE_PHONE_MSG)

    return normalized


def has_uploaded_avatar(user):
    if not user.avatar:
        return False
    return bool(getattr(user.avatar, "name", None))


def build_default_avatar(user):
    background_color = random.choice(AVATAR_COLORS)
    canvas = Image.new("RGB", (AVATAR_SIZE, AVATAR_SIZE), background_color)
    painter = ImageDraw.Draw(canvas)
    letter_font = _resolve_avatar_font()
    initial = user.name[0].upper() if user.name else "?"
    text_position = _calculate_text_position(painter, initial, letter_font)
    painter.text(text_position, initial, fill=AVATAR_TEXT_COLOR, font=letter_font)
    return _save_image_to_file(user, canvas)


def _resolve_avatar_font():
    try:
        return ImageFont.truetype("arial.ttf", AVATAR_FONT_SIZE)
    except Exception:
        return ImageFont.load_default()


def _calculate_text_position(painter, text, letter_font):
    bounds = painter.textbbox((0, 0), text, font=letter_font)
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    x_offset = (AVATAR_SIZE - width) // 2
    y_offset = (AVATAR_SIZE - height) // 2
    return (x_offset, y_offset)


def _save_image_to_file(user, canvas):
    image_buffer = BytesIO()
    canvas.save(image_buffer, format="PNG")
    image_buffer.seek(0)
    filename = f"avatar_{user.email}.png"
    return ContentFile(image_buffer.read(), name=filename)
