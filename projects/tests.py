from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from projects.models import Project, Skill

UserModel = get_user_model()


class SkillModelTest(TestCase):
    def test_create_skill(self):
        skill_record = Skill.objects.create(name='Python')
        self.assertEqual(skill_record.name, 'Python')


class ProjectModelTest(TestCase):
    def setUp(self):
        self.project_owner = UserModel.objects.create_user(
            email='owner@test.com',
            password='pass123',
            name='Project',
            surname='Owner',
            phone='+79004444444',
        )

    def test_create_project(self):
        project_record = Project.objects.create(
            name='Test Project',
            owner=self.project_owner,
            status='open',
        )
        self.assertEqual(project_record.name, 'Test Project')


class ProjectListViewTest(TestCase):
    LIST_URL = reverse('projects:project_list')

    def setUp(self):
        self.list_owner = UserModel.objects.create_user(
            email='test@test.com',
            password='pass123',
            name='Test',
            surname='User',
            phone='+79005555555',
        )
        Project.objects.create(name='Project 1', owner=self.list_owner)

    def test_projects_list_page_exists(self):
        page_response = self.client.get(self.LIST_URL)
        self.assertEqual(page_response.status_code, HTTPStatus.OK)


class ProjectCreateTest(TestCase):
    CREATE_URL = reverse('projects:create_project')

    @classmethod
    def setUpTestData(cls):
        cls.creator = UserModel.objects.create_user(
            email='creator@test.com',
            password='pass123',
            name='Creator',
            surname='User',
            phone='+79006666666',
        )

    def setUp(self):
        self.authenticated_client = Client()
        self.authenticated_client.login(
            username='creator@test.com',
            password='pass123',
        )

    def test_create_project_page_exists(self):
        page_response = self.authenticated_client.get(self.CREATE_URL)
        self.assertEqual(page_response.status_code, HTTPStatus.OK)


class ProjectDetailTest(TestCase):
    def setUp(self):
        self.detail_owner = UserModel.objects.create_user(
            email='viewer@test.com',
            password='pass123',
            name='Viewer',
            surname='User',
            phone='+79007777777',
        )
        self.detail_project = Project.objects.create(
            name='Detail Project',
            owner=self.detail_owner,
        )

    def test_project_detail_page_exists(self):
        detail_url = reverse('projects:project_detail', args=[self.detail_project.id])
        page_response = self.client.get(detail_url)
        self.assertEqual(page_response.status_code, HTTPStatus.OK)


class SkillAutocompleteTest(TestCase):
    AUTOCOMPLETE_URL = reverse('users:skill_autocomplete')

    @classmethod
    def setUpTestData(cls):
        Skill.objects.create(name='Python')

    def test_skill_autocomplete(self):
        page_response = self.client.get(f'{self.AUTOCOMPLETE_URL}?q=py')
        self.assertEqual(page_response.status_code, HTTPStatus.OK)
