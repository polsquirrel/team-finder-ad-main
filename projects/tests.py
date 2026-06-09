from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from projects.models import Project, Skill
from projects.constants import (
    OWNER_EMAIL,
    OWNER_PASSWORD,
    OWNER_NAME,
    OWNER_SURNAME,
    OWNER_PHONE,
    PROJECT_NAME,
    PROJECT_STATUS_OPEN,
    LIST_OWNER_EMAIL,
    LIST_OWNER_PASSWORD,
    LIST_OWNER_NAME,
    LIST_OWNER_SURNAME,
    LIST_OWNER_PHONE,
    LIST_PROJECT_NAME,
    CREATOR_EMAIL,
    CREATOR_PASSWORD,
    CREATOR_NAME,
    CREATOR_SURNAME,
    CREATOR_PHONE,
    VIEWER_EMAIL,
    VIEWER_PASSWORD,
    VIEWER_NAME,
    VIEWER_SURNAME,
    VIEWER_PHONE,
    DETAIL_PROJECT_NAME,
    SKILL_NAME,
)

UserModel = get_user_model()


class SkillModelTest(TestCase):
    def test_create_skill(self):
        skill_record = Skill.objects.create(name="Python")
        self.assertEqual(skill_record.name, "Python")


class ProjectModelTest(TestCase):
    def setUp(self):
        self.project_owner = UserModel.objects.create_user(
            email=OWNER_EMAIL,
            password=OWNER_PASSWORD,
            name=OWNER_NAME,
            surname=OWNER_SURNAME,
            phone=OWNER_PHONE,
        )

    def test_create_project(self):
        project_record = Project.objects.create(
            name=PROJECT_NAME,
            owner=self.project_owner,
            status=PROJECT_STATUS_OPEN,
        )
        self.assertEqual(project_record.name, PROJECT_NAME)


class ProjectListViewTest(TestCase):
    LIST_URL = reverse("projects:project_list")

    def setUp(self):
        self.list_owner = UserModel.objects.create_user(
            email=LIST_OWNER_EMAIL,
            password=LIST_OWNER_PASSWORD,
            name=LIST_OWNER_NAME,
            surname=LIST_OWNER_SURNAME,
            phone=LIST_OWNER_PHONE,
        )
        Project.objects.create(name=LIST_PROJECT_NAME, owner=self.list_owner)

    def test_projects_list_page_exists(self):
        page_response = self.client.get(self.LIST_URL)
        self.assertEqual(page_response.status_code, HTTPStatus.OK)


class ProjectCreateTest(TestCase):
    CREATE_URL = reverse("projects:create_project")

    @classmethod
    def setUpTestData(cls):
        cls.creator = UserModel.objects.create_user(
            email=CREATOR_EMAIL,
            password=CREATOR_PASSWORD,
            name=CREATOR_NAME,
            surname=CREATOR_SURNAME,
            phone=CREATOR_PHONE,
        )

    def setUp(self):
        self.authenticated_client = Client()
        self.authenticated_client.login(
            username=CREATOR_EMAIL,
            password=CREATOR_PASSWORD,
        )

    def test_create_project_page_exists(self):
        page_response = self.authenticated_client.get(self.CREATE_URL)
        self.assertEqual(page_response.status_code, HTTPStatus.OK)


class ProjectDetailTest(TestCase):
    def setUp(self):
        self.detail_owner = UserModel.objects.create_user(
            email=VIEWER_EMAIL,
            password=VIEWER_PASSWORD,
            name=VIEWER_NAME,
            surname=VIEWER_SURNAME,
            phone=VIEWER_PHONE,
        )
        self.detail_project = Project.objects.create(
            name=DETAIL_PROJECT_NAME,
            owner=self.detail_owner,
        )

    def test_project_detail_page_exists(self):
        detail_url = reverse("projects:project_detail", args=[self.detail_project.id])
        page_response = self.client.get(detail_url)
        self.assertEqual(page_response.status_code, HTTPStatus.OK)


class SkillAutocompleteTest(TestCase):
    AUTOCOMPLETE_URL = reverse("users:skill_autocomplete")

    @classmethod
    def setUpTestData(cls):
        Skill.objects.create(name=SKILL_NAME)

    def test_skill_autocomplete(self):
        page_response = self.client.get(f"{self.AUTOCOMPLETE_URL}?q=py")
        self.assertEqual(page_response.status_code, HTTPStatus.OK)
