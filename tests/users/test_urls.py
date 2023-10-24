from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from tests.users.factories import UserFactory  # type: ignore


class UserURLsTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory.create()

    def test_user_urls_get(self):
        # Testing UsersAuthorizedViewSet related URLs
        user_url = reverse("users:user")
        url_string = "/api/users/"
        response = self.client.get(user_url)
        self.assertNotIn(response.status_code, [status.HTTP_405_METHOD_NOT_ALLOWED])
        self.assertEqual(user_url, url_string)

    def test_user_urls_patch(self):
        # Testing UsersAuthorizedViewSet related URLs
        user_url = reverse("users:user")
        url_string = "/api/users/"
        response = self.client.patch(user_url)
        self.assertNotIn(
            response.status_code,
            [status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED],
        )
        self.assertEqual(user_url, url_string)

    def test_user_urls_put(self):
        # Testing UsersAuthorizedViewSet related URLs
        user_url = reverse("users:user")
        url_string = "/api/users/"
        response = self.client.put(user_url)
        self.assertNotIn(
            response.status_code,
            [status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED],
        )
        self.assertEqual(user_url, url_string)

    def test_user_urls_delete(self):
        # Testing UsersAuthorizedViewSet related URLs
        user_url = reverse("users:user")
        url_string = "/api/users/"
        response = self.client.delete(user_url)
        self.assertNotIn(
            response.status_code,
            [status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED],
        )
        self.assertEqual(user_url, url_string)

    def test_user_urls_retrieve(self):
        # Testing UsersAuthorizedViewSet retrieve
        user_detail_url = reverse("users:user", args=[self.user.pk])
        url_string = f"/api/users/{self.user.pk}/"
        response = self.client.get(user_detail_url)
        self.assertNotIn(
            response.status_code,
            [status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED],
        )
        self.assertEqual(user_detail_url, url_string)

    def test_user_unuauthorized_urls_list(self):
        # Testing UsersUnauthorizedViewSet related URLs
        url_string = "/api/users/signup/"
        signup_url = reverse("users:signup")
        response = self.client.post(signup_url)
        self.assertNotIn(
            response.status_code,
            [status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED],
        )
        self.assertEqual(signup_url, url_string)

    def test_user_unuauthorized_urls_resend_activation_code(self):
        # Testing UsersUnauthorizedViewSet related URLs
        url_string = "/api/users/resend-activation-code/"
        resend_url = reverse("users:resend-activation-code")
        response = self.client.post(resend_url)
        self.assertNotIn(
            response.status_code,
            [status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED],
        )
        self.assertEqual(resend_url, url_string)

    def test_user_password_change(self):
        # Testing UsersUnauthorizedViewSet related URLs
        url_string = "/api/users/password-change/"
        resend_url = reverse("users:password-change")
        response = self.client.post(resend_url)
        self.assertNotIn(
            response.status_code,
            [status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED],
        )
        self.assertEqual(resend_url, url_string)
