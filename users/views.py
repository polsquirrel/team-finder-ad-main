import json
from http import HTTPStatus

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from projects.models import Skill
from users.constants import SKILL_AUTOCOMPLETE_LIMIT
from users.forms import ProfileEditForm, RegistrationForm
from users.models import User
from users.pagination import paginate_queryset


def _filter_users_by_skill(queryset, skill_name):
    if not skill_name:
        return queryset
    return queryset.filter(skills__name=skill_name).distinct()


def user_list(request):
    participants_qs = User.objects.all().order_by("id")
    skill_catalog = Skill.objects.all().order_by("name")
    selected_skill = request.GET.get("skill")

    filtered_users = _filter_users_by_skill(participants_qs, selected_skill)
    page = paginate_queryset(request, filtered_users)

    return render(
        request,
        "users/participants.html",
        {
            "participants": page,
            "all_skills": skill_catalog,
            "active_skill": selected_skill,
        },
    )


def register(request):
    registration_form = RegistrationForm(request.POST or None)
    if registration_form.is_valid():
        new_user = registration_form.save(commit=False)
        new_user.set_password(registration_form.cleaned_data["password"])
        new_user.save()
        login(request, new_user)
        return redirect("projects:project_list")

    return render(request, "users/register.html", {"form": registration_form})


def user_detail(request, user_id):
    profile = get_object_or_404(User, id=user_id)
    return render(request, "users/user-details.html", {"user": profile})


def logout_view(request):
    logout(request)
    return redirect("projects:project_list")


@login_required
def edit_profile(request, user_id):
    profile = get_object_or_404(User, id=user_id)

    if request.user.id != profile.id:
        return redirect("users:user_detail", user_id=profile.id)

    edit_form = ProfileEditForm(
        request.POST or None,
        request.FILES or None,
        instance=profile,
    )
    if edit_form.is_valid():
        edit_form.save()
        return redirect("users:user_detail", user_id=profile.id)

    return render(
        request,
        "users/edit_profile.html",
        {"form": edit_form, "user_obj": profile},
    )


def skill_autocomplete(request):
    search_term = request.GET.get("q", "")
    if len(search_term) < 2:
        return JsonResponse([], safe=False)

    matching_skills = (
        Skill.objects.filter(name__istartswith=search_term)
        .order_by("name")[:SKILL_AUTOCOMPLETE_LIMIT]
    )
    results = [{"id": item.id, "name": item.name} for item in matching_skills]
    return JsonResponse(results, safe=False)


def _parse_skill_request_body(request):
    if request.content_type == "application/json":
        try:
            return json.loads(request.body)
        except json.JSONDecodeError:
            return {}
    return request.POST


@login_required
@require_POST
def add_user_skill(request, user_id):
    profile = get_object_or_404(User, id=user_id)

    if request.user.id != profile.id:
        return JsonResponse({"error": "Forbidden"}, status=HTTPStatus.FORBIDDEN)

    payload = _parse_skill_request_body(request)
    skill_id = payload.get("skill_id")
    skill_name = payload.get("name", "").strip() if payload.get("name") else ""

    if skill_id:
        skill = get_object_or_404(Skill, id=skill_id)
        created = False
    elif skill_name:
        skill, created = Skill.objects.get_or_create(name=skill_name)
    else:
        return JsonResponse(
            {"error": "Укажите skill_id или name"},
            status=HTTPStatus.BAD_REQUEST,
        )

    added = False
    if not profile.skills.filter(id=skill.id).exists():
        profile.skills.add(skill)
        added = True

    return JsonResponse({
        "skill_id": skill.id,
        "id": skill.id,
        "name": skill.name,
        "created": created,
        "added": added,
    })


@login_required
@require_POST
def remove_user_skill(request, user_id, skill_id):
    profile = get_object_or_404(User, id=user_id)
    skill = get_object_or_404(Skill, id=skill_id)

    if request.user.id != profile.id:
        return JsonResponse({"status": "error"}, status=HTTPStatus.FORBIDDEN)

    if not profile.skills.filter(id=skill.id).exists():
        return JsonResponse({"status": "error"}, status=HTTPStatus.BAD_REQUEST)

    profile.skills.remove(skill)
    return JsonResponse({"status": "ok"})


def custom_login(request):
    if request.method == "POST":
        email_input = request.POST.get("username")
        password_input = request.POST.get("password")
        authenticated_user = authenticate(
            request,
            username=email_input,
            password=password_input,
        )
        if authenticated_user is not None:
            login(request, authenticated_user)
            return redirect("projects:project_list")

    auth_form = AuthenticationForm()
    return render(request, "users/login.html", {"form": auth_form})
