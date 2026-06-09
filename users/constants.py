# Ограничения длины полей профиля
USER_NAME_MAX_LENGTH = 124
USER_SURNAME_MAX_LENGTH = 124
USER_PHONE_MAX_LENGTH = 12
USER_ABOUT_MAX_LENGTH = 256

# Пагинация списка участников
USERS_PER_PAGE = 12

# Лимит подсказок при поиске навыков
SKILL_AUTOCOMPLETE_LIMIT = 10

# Параметры генерации аватара
AVATAR_SIZE = 200
AVATAR_FONT_SIZE = 100
AVATAR_TEXT_COLOR = "#FFFFFF"

RED = "#FF6B6B"
TEAL = "#4ECDC4"
SKY_BLUE = "#45B7D1"
MINT_GREEN = "#96CEB4"
LIGHT_YELLOW = "#FFEAA7"
PLUM = "#DDA0DD"
SEAFOAM = "#98D8C8"
GOLDEN_YELLOW = "#F7DC6F"
LAVENDER_PURPLE = "#BB8FCE"
CORNFLOWER_BLUE = "#85C1E2"

# Палитра фона для аватара

AVATAR_COLORS = (
    RED,
    TEAL,
    SKY_BLUE,
    MINT_GREEN,
    LIGHT_YELLOW,
    PLUM,
    SEAFOAM,
    GOLDEN_YELLOW,
    LAVENDER_PURPLE,
    CORNFLOWER_BLUE,
)

DUPLICATE_EMAIL_MSG = "Пользователь с таким email уже существует"
DUPLICATE_PHONE_MSG = "Этот номер телефона уже используется"
PHONE_FORMAT_MSG = "Номер телефона должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX"
PHONE_REQUIRED_MSG = "Телефон обязателен для заполнения"
