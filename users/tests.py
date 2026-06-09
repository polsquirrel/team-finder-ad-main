import json
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from projects.models import Skill

UserModel = get_user_model()


def _build_test_user(email, password, first_name, last_name, phone="+79001111111"):
    return UserModel.objects.create_user(
        email=email,
        password=password,
        name=first_name,
        surname=last_name,
        phone=phone,
    )


class UserModelTest(TestCase):
    def test_create_user(self):
        account = _build_test_user(
            email="test@test.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.assertEqual(account.email, "test@test.com")
        self.assertTrue(account.check_password("testpass123"))
        self.assertTrue(account.is_active)
        self.assertFalse(account.is_staff)
        self.assertTrue(account.avatar.name)

    def test_create_superuser(self):
        super_account = UserModel.objects.create_superuser(
            email="admin@test.com",
            password="adminpass123",
            name="Admin",
            surname="User",
            phone="+79008888888",
        )
        self.assertTrue(super_account.is_staff)
        self.assertTrue(super_account.is_superuser)


class UserRegistrationTest(TestCase):
    REGISTER_URL = reverse("users:register")

    def test_register_page_exists(self):
        page_response = self.client.get(self.REGISTER_URL)
        self.assertEqual(page_response.status_code, HTTPStatus.OK)

    def test_user_registration_success(self):
        registration_data = {
            "name": "Test",
            "surname": "User",
            "email": "newuser@test.com",
            "phone": "89001234567",
            "password": "testpass123",
        }
        page_response = self.client.post(self.REGISTER_URL, registration_data)
        self.assertEqual(page_response.status_code, HTTPStatus.FOUND)
        self.assertEqual(UserModel.objects.count(), 1)


class UserListViewTest(TestCase):
    PARTICIPANTS_URL = reverse("users:user_list")

    @classmethod
    def setUpTestData(cls):
        cls.first_participant = _build_test_user(
            email="user1@test.com",
            password="pass",
            first_name="User1",
            last_name="One",
            phone="+79001111111",
        )
        cls.second_participant = _build_test_user(
            email="user2@test.com",
            password="pass",
            first_name="User2",
            last_name="Two",
            phone="+79002222222",
        )

    def test_users_list_page_exists(self):
        page_response = self.client.get(self.PARTICIPANTS_URL)
        self.assertEqual(page_response.status_code, HTTPStatus.OK)

    def test_users_list_contains_users(self):
        page_response = self.client.get(self.PARTICIPANTS_URL)
        self.assertContains(page_response, "User1 One")
        self.assertContains(page_response, "User2 Two")

    def test_users_list_filter_by_skill_name(self):
        python_skill = Skill.objects.create(name="Python")
        self.first_participant.skills.add(python_skill)

        filtered_url = f"{self.PARTICIPANTS_URL}?skill=Python"
        page_response = self.client.get(filtered_url)

        self.assertEqual(page_response.status_code, HTTPStatus.OK)
        self.assertContains(page_response, "User1 One")
        self.assertNotContains(page_response, "User2 Two")


class UserSkillsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.profile_owner = _build_test_user(
            email="skills@test.com",
            password="pass123",
            first_name="Skill",
            last_name="Owner",
            phone="+79003333333",
        )
        cls.existing_skill = Skill.objects.create(name="Python")

    def setUp(self):
        self.auth_client = Client()
        self.auth_client.login(username="skills@test.com", password="pass123")

    def test_add_skill_by_name(self):
        add_url = reverse("users:add_user_skill", args=[self.profile_owner.id])
        response = self.auth_client.post(
            add_url,
            data=json.dumps({"name": "Django"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        payload = response.json()
        self.assertTrue(payload["created"])
        self.assertTrue(payload["added"])
        self.assertTrue(self.profile_owner.skills.filter(name="Django").exists())

    def test_add_existing_skill_by_id(self):
        add_url = reverse("users:add_user_skill", args=[self.profile_owner.id])
        response = self.auth_client.post(
            add_url,
            data=json.dumps({"skill_id": self.existing_skill.id}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        payload = response.json()
        self.assertFalse(payload["created"])
        self.assertTrue(payload["added"])

    def test_remove_skill(self):
        self.profile_owner.skills.add(self.existing_skill)
        remove_url = reverse(
            "users:remove_user_skill",
            args=[self.profile_owner.id, self.existing_skill.id],
        )
        response = self.auth_client.post(remove_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json()["status"], "ok")
        self.assertFalse(
            self.profile_owner.skills.filter(id=self.existing_skill.id).exists()
        )
