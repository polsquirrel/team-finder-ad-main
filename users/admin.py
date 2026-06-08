from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "id",
        "email",
        "name",
        "surname",
        "owned_projects_count",
        "participated_projects_count",
        "is_active",
        "is_staff",
    )
    list_display_links = ("id", "email")
    list_filter = ("is_active", "is_staff", "skills")
    search_fields = ("email", "name", "surname", "phone")
    filter_horizontal = ("skills",)
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {"fields": ("name", "surname", "avatar", "about", "phone", "github_url")},
        ),
        ("Skills", {"fields": ("skills",)}),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "surname", "password1", "password2"),
            },
        ),
    )

    @admin.display(description="Проектов (автор)", ordering="owned_projects")
    def owned_projects_count(self, obj):
        return obj.owned_projects.count()

    @admin.display(description="Проектов (участник)", ordering="participated_projects")
    def participated_projects_count(self, obj):
        return obj.participated_projects.count()
