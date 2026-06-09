from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render

from projects.constants import (
    PROJECTS_PER_PAGE,
    PROJECT_STATUS_CLOSED,
    PROJECT_STATUS_OPEN,
)
from projects.forms import ProjectForm
from projects.models import Project
from projects.services import paginate_queryset


def _project_detail_queryset():
    return Project.objects.select_related("owner").prefetch_related("participants")


def _is_project_owner(user, project):
    return project.owner == user


def project_list(request):
    all_projects = _project_detail_queryset()
    projects_page = paginate_queryset(request, all_projects, PROJECTS_PER_PAGE)
    return render(request, "projects/project_list.html", {"projects": projects_page})


def project_detail(request, project_id):
    project = _project_detail_queryset().filter(id=project_id).first()
    if project is None:
        return JsonResponse({"error": "Project not found"}, status=404)
    return render(request, "projects/project-details.html", {"project": project})

@login_required
def create_project(request):
    project_form = ProjectForm(request.POST or None)
    if project_form.is_valid():
        new_project = project_form.save(commit=False)
        new_project.owner = request.user
        new_project.save()
        new_project.participants.add(request.user)
        return redirect("projects:project_detail", project_id=new_project.id)

    return render(
        request,
        "projects/create-project.html",
        {"form": project_form, "is_edit": False},
    )


@login_required
def edit_project(request, project_id):
    project = Project.objects.filter(id=project_id).first()
    if project is None:
        return JsonResponse({"error": "Project not found"}, status=404)

    if not _is_project_owner(request.user, project):
        return redirect("projects:project_detail", project_id=project.id)

    project_form = ProjectForm(request.POST or None, instance=project)
    if project_form.is_valid():
        project_form.save()
        return redirect("projects:project_detail", project_id=project.id)

    return render(
        request,
        "projects/create-project.html",
        {"form": project_form, "is_edit": True, "project": project},
    )


@login_required
def complete_project(request, project_id):
    project = Project.objects.filter(id=project_id).first()
    if project is None:
        return JsonResponse({'error': 'Project not found'}, status=404)

    can_complete = (
        request.method == "POST"
        and _is_project_owner(request.user, project)
        and project.status == PROJECT_STATUS_OPEN
    )
    if can_complete:
        project.status = PROJECT_STATUS_CLOSED
        project.save()
        return JsonResponse({"status": "ok", "project_status": PROJECT_STATUS_CLOSED})

    return JsonResponse({"status": "error"}, status=HTTPStatus.BAD_REQUEST)


@login_required
def toggle_participate(request, project_id):
    project = Project.objects.filter(id=project_id).first()
    if project is None:
        return JsonResponse({"error": "Project not found"}, status=404)

    if request.method == "POST":
        membership = project.participants.filter(id=request.user.id)
        if membership.exists():
            project.participants.remove(request.user)
        else:
            project.participants.add(request.user)

    return redirect("projects:project_detail", project_id=project.id)
