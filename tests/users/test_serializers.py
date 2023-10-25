import os

from django.core.files import File
from django.test import TestCase

from api.users.serializers import UserSerializer
from tests.courses.factories import CourseFactory
from tests.users.factories import UserFactory, fake  # type: ignore


class TestUserSerializer(TestCase):
    def test_valid_serializer(self):
        user = UserFactory.create()
        serializer = UserSerializer(user)
        self.assertIn("username", serializer.data)
        self.assertEqual(serializer.data["username"], user.username)

    def test_invalid_password_repeat(self):
        image_path = os.path.join(os.path.dirname(__file__), "../_data/1.jpg")
        course = CourseFactory.create()
        with open(image_path, "rb") as image:
            data = {
                "username": fake.user_name(),
                "email": fake.email(),
                "password": "Testpassword",
                "password_repeat": "Wrongpassword",
                "avatar": File(image),
                "birthdate": fake.date_of_birth(minimum_age=14).strftime("%Y-%m-%d"),
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "default_course": course.pk,
            }

            serializer = UserSerializer(data=data)
            self.assertFalse(serializer.is_valid())
            self.assertIn("password_repeat", serializer.errors)

    def test_expected_fields(self):
        serializer = UserSerializer(data={})
        serializer.is_valid()
        required_fields = [
            field_name
            for field_name, field in serializer.fields.items()
            if field.required
        ]
        required_fields_list = [
            "password_repeat",
            "default_course",
            "password",
            "username",
            "first_name",
            "last_name",
            "birthdate",
        ]
        self.assertFalse(serializer.is_valid())
        self.assertListEqual(list(serializer.errors.keys()), required_fields)
        self.assertListEqual(list(serializer.errors.keys()), required_fields_list)
