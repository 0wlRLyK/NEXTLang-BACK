import os
import re
from datetime import timedelta

from django.contrib.auth.hashers import check_password
from django.core import mail
from django.core.files import File
from django.urls import reverse
from django.utils.timezone import now
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import ActivationCode, User
from common.tests import get_token_for_user
from tests.users.factories import UserFactory, fake  # type: ignore


class UserSignUpTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super(UserSignUpTests, cls).setUpClass()
        cls.user = UserFactory.create()

    def test_successful_signup(self):
        image_path = os.path.join(os.path.dirname(__file__), "../_data/1.jpg")
        with open(image_path, "rb") as image:
            password = fake.password()
            data = {
                "email": "0wlrlyk@gmail.com",
                "username": fake.user_name(),
                "password": password,
                "password_repeat": password,
                "avatar": File(image),
                "birthdate": fake.date_of_birth(minimum_age=14).strftime("%Y-%m-%d"),
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
            }
            url = reverse("users:signup")
            response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertTrue(User.objects.filter(email=data["email"]).exists())

    def test_successful_activation(self):
        image_path = os.path.join(os.path.dirname(__file__), "../_data/1.jpg")
        with open(image_path, "rb") as image:
            password = fake.password()
            data = {
                "email": fake.email(),
                "username": fake.user_name(),
                "password": password,
                "password_repeat": password,
                "avatar": File(image),
                "birthdate": fake.date_of_birth(minimum_age=14).strftime("%Y-%m-%d"),
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
            }
            url = reverse("users:signup")
            response = self.client.post(url, data, format="multipart")
            message = mail.outbox[0].message().__str__()
            match = re.search(r'href="([^"]*activate[^"]*)"', message)
            url = match.group(1)
            # Search of uid and token in link
            uid_match = re.search(r"uid=([^&]*)", url)
            token_match = re.search(r"token=([^&]*)", url)
            if uid_match and token_match:
                uid = uid_match.group(1)
                token = token_match.group(1)
                url = reverse("users:activate", kwargs={"uid": uid, "token": token})
                activate_response = self.client.post(url, format="json")
                user = User.objects.get(pk=response.data.get("id"))
                user.refresh_from_db()
                self.assertIsNotNone(user.password)
                self.assertEqual(activate_response.status_code, status.HTTP_200_OK)
                self.assertEqual(user.email, data["email"])
                self.assertEqual(user.username, data["username"])
                self.assertIn("access", activate_response.data)
                self.assertIn("refresh", activate_response.data)
                self.assertTrue(".jpg" in user.avatar.name)
                self.assertTrue(user.is_active)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertTrue(User.objects.filter(email=data["email"]).exists())

    def test_wrong_signup_different_passwords(self):
        image_path = os.path.join(os.path.dirname(__file__), "../_data/1.jpg")
        with open(image_path, "rb") as image:
            data = {
                "email": fake.email(),
                "username": fake.user_name(),
                "password": fake.password(),
                "password_repeat": fake.password(),
                "avatar": File(image),
                "birthdate": fake.date_of_birth(minimum_age=14).strftime("%Y-%m-%d"),
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
            }
            url = reverse("users:signup")
            response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data.keys()), 1)
        self.assertEqual(list(response.data.keys())[0], "password_repeat")

    def test_wrong_signup_missing_fields(self):
        data = {
            "email": fake.email(),
        }

        url = reverse("users:signup")
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_successful_change_password_signup(self):
        token = get_token_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        url = reverse("users:password-change")
        password = fake.password()
        data = {"password": password, "password_repeat": password}
        response = self.client.post(url, data=data, format="json")
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(check_password(password, self.user.password))

    def test_change_password_signup_password_check(self):
        token = get_token_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        url = reverse("users:password-change")
        password = "password"  # noqa
        data = {"password": password, "password_repeat": password}
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_successful_reset_password(self):
        data = {"email": self.user.email}
        url_reset_password = reverse("users:reset-password")
        response = self.client.post(url_reset_password, data=data, format="json")
        message = mail.outbox[0].message().__str__()
        match = re.search(r'href="([^"]*reset-password[^"]*)"', message)
        is_activation_code_exists = self.user.activation_codes.all().exists()
        url = match.group(1)
        # Search for uid and token in a link
        uid_match = re.search(r"uid=([^&]*)", url)
        token_match = re.search(r"token=([^&]*)", url)
        if uid_match and token_match:
            uid = uid_match.group(1)
            token = token_match.group(1)
            data = {
                "uid": uid,
                "token": token,
                "password": "New_p@ssword1",
                "password_repeat": "New_p@ssword1",
            }
            url = reverse("users:confirm-password")
            confirm_response = self.client.post(url, data=data, format="json")
            is_activation_code_exists_after = self.user.activation_codes.all().exists()
            self.user.refresh_from_db()
            self.assertTrue(check_password(data["password"], self.user.password))
            self.assertEqual(confirm_response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertTrue(is_activation_code_exists)
            self.assertFalse(is_activation_code_exists_after)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_reset_password_check_password(self):
        data = {"email": self.user.email}
        url_reset_password = reverse("users:reset-password")
        response = self.client.post(url_reset_password, data=data, format="json")
        message = mail.outbox[0].message().__str__()
        match = re.search(r'href="([^"]*reset-password[^"]*)"', message)
        self.user.activation_codes.all().exists()
        url = match.group(1)
        # Search for uid and token in a link
        uid_match = re.search(r"uid=([^&]*)", url)
        token_match = re.search(r"token=([^&]*)", url)
        if uid_match and token_match:
            uid = uid_match.group(1)
            token = token_match.group(1)
            data = {
                "uid": uid,
                "token": token,
                "password": "password",
                "password_repeat": "password",
            }
            url = reverse("users:confirm-password")
            confirm_response = self.client.post(url, data=data, format="json")
            self.assertEqual(confirm_response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn("password", confirm_response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_wrong_uid(self):
        data = {"email": self.user.email}
        url_reset_password = reverse("users:reset-password")
        response = self.client.post(url_reset_password, data=data, format="json")
        message = mail.outbox[0].message().__str__()
        match = re.search(r'href="([^"]*reset-password[^"]*)"', message)
        url = match.group(1)
        # Search for uid and token in a link
        uid_match = re.search(r"uid=([^&]*)", url)
        token_match = re.search(r"token=([^&]*)", url)
        if uid_match and token_match:
            token = token_match.group(1)

            data = {
                "uid": "AV8xsq",
                "token": token,
                "password": "New_password",
                "password_repeat": "New_password",
            }
            url = reverse("users:confirm-password")
            confirm_response = self.client.post(url, data=data, format="json")
            self.user.refresh_from_db()
            self.assertTrue("uid" in confirm_response.data)
            self.assertEqual(confirm_response.data["uid"], "The uid is incorrect")
            self.assertEqual(confirm_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_wrong_token(self):
        self.user.is_active = True
        self.user.save()
        data = {"email": self.user.email}
        url_reset_password = reverse("users:reset-password")
        response = self.client.post(url_reset_password, data=data, format="json")
        message = mail.outbox[0].message().__str__()
        match = re.search(r'href="([^"]*reset-password[^"]*)"', message)
        url = match.group(1)
        # Search for uid and token in a link
        uid_match = re.search(r"uid=([^&]*)", url)
        token_match = re.search(r"token=([^&]*)", url)
        if uid_match and token_match:
            uid = uid_match.group(1)
            data = {
                "uid": uid,
                "token": "random_text",
                "password": "New_password",
                "password_repeat": "New_password",
            }
            url = reverse("users:confirm-password")
            confirm_response = self.client.post(url, data=data, format="json")
            self.user.refresh_from_db()
            self.assertTrue("token" in confirm_response.data)
            self.assertEqual(
                str(confirm_response.data["token"][0]), "This token is invalid"
            )
            self.assertEqual(confirm_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_wrong_token_expired(self):
        data = {"email": self.user.email}
        url_reset_password = reverse("users:reset-password")
        response = self.client.post(url_reset_password, data=data, format="json")
        message = mail.outbox[0].message().__str__()
        match = re.search(r'href="([^"]*reset-password[^"]*)"', message)
        url = match.group(1)
        # Search for uid and token in a link
        uid_match = re.search(r"uid=([^&]*)", url)
        token_match = re.search(r"token=([^&]*)", url)
        if uid_match and token_match:
            uid = uid_match.group(1)
            token = token_match.group(1)
            activation_code = ActivationCode.objects.get(
                uid=uid, code=token, user=self.user
            )
            activation_code.expiration_date = now() - timedelta(days=1)
            activation_code.save()
            data = {
                "uid": uid,
                "token": token,
                "password": "New_password",
                "password_repeat": "New_password",
            }
            url = reverse("users:confirm-password")
            confirm_response = self.client.post(url, data=data, format="json")
            self.user.refresh_from_db()
            self.assertTrue("token" in confirm_response.data)
            self.assertEqual(
                str(confirm_response.data["token"][0]), "This token is expired"
            )
            self.assertEqual(confirm_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_successful_change_email(self):
        token = get_token_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        data = {"email": "new_test_email@test.mail.com"}
        url_change_email = reverse("users:user")
        response = self.client.patch(url_change_email, data=data, format="json")
        message = mail.outbox[0].message().__str__()
        match = re.search(r'href="([^"]*confirm-email[^"]*)"', message)
        is_activation_code_exists = self.user.activation_codes.all().exists()
        url = match.group(1)
        # Search for uid and token in a link
        uid_match = re.search(r"uid=([^&]*)", url)
        token_match = re.search(r"token=([^&]*)", url)
        if uid_match and token_match:
            uid = uid_match.group(1)
            token = token_match.group(1)
            url = reverse("users:confirm-email", kwargs={"uid": uid, "token": token})
            confirm_response = self.client.post(url, data=data, format="json")
            is_activation_code_exists_after = self.user.activation_codes.all().exists()
            self.user.refresh_from_db()
            self.assertEqual(self.user.email, data["email"])
            self.assertEqual(confirm_response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertTrue(is_activation_code_exists)
            self.assertFalse(is_activation_code_exists_after)
        self.assertNotEqual(response.data.get("email"), data["email"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_successful_delete_user(self):
        token = get_token_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        url = reverse("users:user")
        url_second = reverse("users:user", kwargs={"pk": self.user.pk})
        response_delete = self.client.delete(url, format="json")
        response_get = self.client.get(url_second, format="json")
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_get.status_code, status.HTTP_401_UNAUTHORIZED)

    def tests_successful_user_flow(self):
        password = fake.password()
        data = {
            "birthdate": fake.date_of_birth(minimum_age=14).strftime("%Y-%m-%d"),
            "password": password,
            "email": fake.email(),
            "password_repeat": password,
            "username": fake.user_name(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
        }
        # Part 1 :: Create user and send activation letter at email
        url = reverse("users:signup")
        response_create = self.client.post(url, data, format="multipart")
        user = User.objects.get(pk=response_create.data.get("id"))
        # Part 2 :: Resend activation letter at email
        url_resend = reverse("users:resend-activation-code")
        response_resend_activation_code = self.client.post(
            url_resend, {"email": data["email"]}, format="multipart"
        )
        message = mail.outbox[1].message().__str__()
        match = re.search(r'href="([^"]*activate[^"]*)"', message)
        url = match.group(1)
        # Search of uid and token in link
        uid_match = re.search(r"uid=([^&]*)", url)
        token_match = re.search(r"token=([^&]*)", url)
        if uid_match and token_match:
            uid = uid_match.group(1)
            token = token_match.group(1)
            # Part 3 :: Activate user
            url = reverse("users:activate", kwargs={"uid": uid, "token": token})
            activate_response = self.client.post(url, format="json")

            self.client.credentials(
                HTTP_AUTHORIZATION=f"Bearer {activate_response.data.get('access')}"
            )
            # Part 4 :: Update user
            url_user = reverse("users:user")
            update_data = {
                "username": "test_username",
            }
            response_update = self.client.patch(
                url_user, data=update_data, format="multipart"
            )
            self.assertEqual(response_update.status_code, 200)
            user.refresh_from_db()

            self.assertEqual(user.is_active, True)
            self.assertEqual(user.username, update_data.get("username"))
        self.assertEqual(response_create.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response_resend_activation_code.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertTrue(len(mail.outbox) >= 2)

    def tests_successful_user_flow_json(self):
        password = fake.password()
        data = {
            "birthdate": fake.date_of_birth(minimum_age=14).strftime("%Y-%m-%d"),
            "password": password,
            "email": fake.email(),
            "password_repeat": password,
            "username": fake.user_name(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
        }
        # Part 1 :: Create user and send activation letter at email
        url = reverse("users:signup")
        response_create = self.client.post(url, data, format="multipart")
        user = User.objects.get(pk=response_create.data.get("id"))
        # Part 2 :: Resend activation letter at email
        url_resend = reverse("users:resend-activation-code")
        response_resend_activation_code = self.client.post(
            url_resend, {"email": data["email"]}, format="multipart"
        )
        message = mail.outbox[1].message().__str__()
        match = re.search(r'href="([^"]*activate[^"]*)"', message)
        url = match.group(1)
        # Search of uid and token in link
        uid_match = re.search(r"uid=([^&]*)", url)
        token_match = re.search(r"token=([^&]*)", url)
        if uid_match and token_match:
            uid = uid_match.group(1)
            token = token_match.group(1)
            # Part 3 :: Activate user
            url = reverse("users:activate", kwargs={"uid": uid, "token": token})
            activate_response = self.client.post(url, format="json")

            self.client.credentials(
                HTTP_AUTHORIZATION=f"Bearer {activate_response.data.get('access')}"
            )
            # Part 4 :: Update user
            url_user = reverse("users:user")
            update_data = {
                "username": "test_username",
                "birthdate": fake.date_of_birth(minimum_age=14).strftime("%Y-%m-%d"),
                "password": password,
                "password_repeat": password,
                "email": fake.email(),
            }
            response_update = self.client.patch(
                url_user, data=update_data, format="multipart"
            )
            self.assertEqual(response_update.status_code, 200)
            user.refresh_from_db()

            self.assertEqual(user.is_active, True)
            self.assertEqual(user.username, update_data.get("username"))
        self.assertEqual(response_create.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response_resend_activation_code.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertTrue(len(mail.outbox) >= 2)

    def tests_check_password(self):
        password = "password"  # noqa
        data = {
            "birthdate": fake.date_of_birth(minimum_age=18).strftime("%Y-%m-%d"),
            "password": password,
            "email": fake.email(),
            "password_repeat": password,
        }
        url = reverse("users:signup")
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_list_of_users(self):
        quantity = 5
        UserFactory.create_batch(quantity)
        response = self.client.get(reverse("users:list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], quantity + 1)
