from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import path

from users.forms import CustomLoginForm
from users.views import (
    add_user_skill,
    edit_profile,
    logout_view,
    register,
    remove_user_skill,
    skill_autocomplete,
    user_detail,
    user_list,
)

urlpatterns = [
    path("list/", user_list, name="user_list"),
    path("register/", register, name="register"),
    path(
        "login/",
        LoginView.as_view(
            template_name="users/login.html", authentication_form=CustomLoginForm
        ),
        name="login",
    ),
    path("logout/", logout_view, name="logout"),
    path(
        "change-password/",
        PasswordChangeView.as_view(template_name="users/change_password.html"),
        name="change_password",
    ),
    path("skills/", skill_autocomplete, name="skill_autocomplete"),
    path("<int:user_id>/skills/add/", add_user_skill, name="add_user_skill"),
    path(
        "<int:user_id>/skills/<int:skill_id>/remove/",
        remove_user_skill,
        name="remove_user_skill",
    ),
    path("<int:user_id>/", user_detail, name="user_detail"),
    path("<int:user_id>/edit/", edit_profile, name="edit_profile"),
]
