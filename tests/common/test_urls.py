from django.test import TestCase

from apps.users.models import User


class AdminPanelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.admin_user = User.objects.create_superuser(
            "admin", "admin@example.com", "password123"
        )

    def test_admin_panel_is_accessible(self):
        response = self.client.get("/admin/")
        url = "/admin/login/?next=/admin/"
        self.assertEqual(response.url, url)
        self.assertEqual(response.status_code, 302)

    def test_admin_panel_is_accessible2(self):
        response = self.client.get("/admin/login/?next=/admin/")
        self.assertEqual(response.status_code, 200)

    def test_admin_panel_accessible_for_logged_in_admin(self):
        self.client.login(username="admin", password="password123")
        self.client.force_login(self.admin_user)
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 302)


class DocsTestCase(TestCase):
    def test_swagger_ui_is_accessible(self):
        response = self.client.get("/api/swagger/")
        self.assertEqual(response.status_code, 200)

    def test_redoc_ui_is_accessible(self):
        response = self.client.get("/api/redoc/")
        self.assertEqual(response.status_code, 200)
