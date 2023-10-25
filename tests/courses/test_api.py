from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.courses.models import UserCourse
from tests.courses.factories import CourseFactory, UserCourseFactory
from tests.users.factories import UserFactory


class TestUserCoursesViewSet(APITestCase):
    def setUp(self):
        self.course1 = CourseFactory()
        self.course2 = CourseFactory()
        self.user = UserFactory()
        self.user_couse = UserCourseFactory(
            user=self.user, course=self.course1, is_default=True
        )

        self.url_add_course = reverse("courses:add_course")
        self.client.force_authenticate(self.user)

    def test_add_new_default_course(self):
        response = self.client.post(self.url_add_course, {"course": self.course2.id})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        user_course = UserCourse.objects.filter(
            user=self.user, course=self.course2
        ).first()
        self.assertIsNotNone(user_course)
        self.assertTrue(user_course.is_default)

    def test_try_adding_already_studying_course(self):
        response = self.client.post(self.url_add_course, {"course": self.course1.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_default_on_adding_new_course(self):
        self.client.post(self.url_add_course, {"course": self.course2.id})
        old_course = UserCourse.objects.filter(
            user=self.user, course=self.course1
        ).first()
        new_course = UserCourse.objects.filter(
            user=self.user, course=self.course2
        ).first()
        self.assertFalse(old_course.is_default)
        self.assertTrue(new_course.is_default)

    def test_unauthenticated_user(self):
        self.client.force_authenticate(None)  # Logout user
        response = self.client.post(self.url_add_course, {"course": self.course1.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
