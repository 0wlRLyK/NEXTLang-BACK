from django.test import TestCase

from apps.users.models import ActivationCode, User
from services.users import UnauthorizedUserService, UsersService
from tests.users.factories import ActivationCodeFactory  # type: ignore
from tests.users.factories import UserFactory


class TestUsersService(TestCase):
    def setUp(self):
        self.user = UserFactory(is_active=False, email="original_email@example.com")
        self.service = UsersService(self.user)

    def test_activate_user(self):
        self.service.activate()
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_set_password(self):
        new_password = "newPassword123"
        self.service.set_password(new_password)
        self.assertTrue(self.user.check_password(new_password))

    def test_set_email(self):
        new_email = "new_email@example.com"
        self.service.set_email(new_email)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, new_email)

    def test_confirm_password(self):
        password = "newPassword123"
        activation_code = ActivationCodeFactory(user=self.user)
        uid = activation_code.uid
        token = activation_code.code

        self.service.confirm_password(password, uid, token)
        self.assertTrue(self.user.check_password(password))
        with self.assertRaises(ActivationCode.DoesNotExist):
            ActivationCode.objects.get(user=self.user, uid=uid, code=token)

    def test_confirm_email(self):
        new_email = "new_email@example.com"
        activation_code = ActivationCodeFactory(user=self.user, email=new_email)
        uid = activation_code.uid
        token = activation_code.code

        self.service.confirm_email(uid, token)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, new_email)
        with self.assertRaises(ActivationCode.DoesNotExist):
            ActivationCode.objects.get(user=self.user, uid=uid, code=token)


class TestUnauthorizedUserService(TestCase):
    def test_create_user(self):
        data = {
            "email": "test@example.com",
            "username": "testuser",
        }
        password = "testpassword"

        user = UnauthorizedUserService.create_user(data, password)

        self.assertTrue(User.objects.filter(email="test@example.com").exists())
        self.assertTrue(user.check_password(password))
