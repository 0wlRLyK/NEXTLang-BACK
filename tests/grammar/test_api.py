from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.courses.constants import LearningSpheres
from common.tests import get_token_for_user
from services.courses.topic import (
    TopicFactoryProvider,
    TopicService,
    UserTopicFactoryProvider,
)
from tests.courses.factories import (
    CourseFactory,
    GrammarSectionFactory,
    GrammarTopicFactory,
    LanguageFactory,
    UserCourseFactory,
)
from tests.users.factories import UserFactory


class GrammarAPITestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()  # Припускаємо, що у вас є UserFactory
        self.from_language = LanguageFactory()
        self.to_language = LanguageFactory()
        self.course = CourseFactory(
            from_language=self.from_language, to_language=self.to_language
        )
        self.user_course = UserCourseFactory(user=self.user, course=self.course)
        self.topics_count = 5

        # Створення секцій та тем для граматики і аудіювання
        self.grammar_sections = [
            GrammarSectionFactory(course=self.course, level=self.user_course.level)
            for _ in range(self.topics_count)
        ]

        self.grammar_topics = [
            GrammarTopicFactory(section=section) for section in self.grammar_sections
        ]

        self.topic_provider = TopicFactoryProvider()
        self.user_topic_provider = UserTopicFactoryProvider()
        TopicService(user=self.user, sphere=LearningSpheres.GRAMMAR).set_topic(
            topic_id=None
        )

    def test_sections_list(self):
        token = get_token_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(reverse("grammar:sections_list"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], self.topics_count)
        self.assertTrue(response.data["results"][0]["topics"][0]["is_learning"])

    def test_retrieve_current_topic(self):
        token = get_token_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(reverse("grammar:topic"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["topic"], self.grammar_topics[0].id)
