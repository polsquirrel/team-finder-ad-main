from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


def redirect_to_project_catalog(request):
    return redirect("projects:project_list")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", redirect_to_project_catalog),
    path("users/", include(("users.urls", "users"), namespace="users")),
    path("projects/", include(("projects.urls", "projects"), namespace="projects")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
