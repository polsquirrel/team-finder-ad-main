from django.contrib import admin

from projects.models import Project, Skill


def _format_related_names(items, label_fn):
    names = [label_fn(item) for item in items]
    return ", ".join(names) if names else "-"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "owner",
        "status",
        "participants_display",
        "skills_display",
    )
    list_display_links = ("id", "name")
    list_filter = ("status", "created_at")
    search_fields = ("name", "description", "owner__email", "owner__name")
    readonly_fields = ("created_at",)
    filter_horizontal = ("participants", "skills")

    @admin.display(description="Участники")
    def participants_display(self, obj):
        return _format_related_names(
            obj.participants.all(),
            lambda participant: f"{participant.name} {participant.surname}",
        )

    @admin.display(description="Навыки")
    def skills_display(self, obj):
        return _format_related_names(obj.skills.all(), lambda skill: skill.name)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
