# Ограничения длины полей
SKILL_NAME_MAX_LENGTH = 124
PROJECT_NAME_MAX_LENGTH = 200

# Коды статусов проекта
PROJECT_STATUS_OPEN = "open"
PROJECT_STATUS_CLOSED = "closed"

PROJECT_STATUS_CHOICES = (
    (PROJECT_STATUS_OPEN, "Open"),
    (PROJECT_STATUS_CLOSED, "Closed"),
)

# Пагинация каталога проектов
PROJECTS_PER_PAGE = 12
