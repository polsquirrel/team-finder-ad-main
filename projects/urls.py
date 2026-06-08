from django.urls import path

from projects.views import (
    complete_project,
    create_project,
    edit_project,
    project_detail,
    project_list,
    toggle_participate,
)

urlpatterns = [
    path("list/", project_list, name="project_list"),
    path("create-project/", create_project, name="create_project"),
    path("<int:project_id>/", project_detail, name="project_detail"),
    path("<int:project_id>/edit/", edit_project, name="edit_project"),
    path("<int:project_id>/complete/", complete_project, name="complete_project"),
    path(
        "<int:project_id>/toggle-participate/",
        toggle_participate,
        name="toggle_participate",
    ),
]
