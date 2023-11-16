from django.test import TestCase

from apps.audition.models import UserAuditionTopic
from apps.grammar.models import GrammarTopic, UserGrammarTopic
from services.courses.exceptions import NoAvailableTopics
from services.courses.topic import AuditionTopicFactory as AuditionTopicServiceFactory
from services.courses.topic import GrammarTopicFactory as GrammarTopicServiceFactory
from services.courses.topic import TopicFactoryProvider, TopicService
from services.courses.topic import (
    UserAuditionTopicFactory as UserAuditionTopicServiceFactory,
)
from services.courses.topic import (
    UserGrammarTopicFactory as UserGrammarTopicServiceFactory,
)
from services.courses.topic import UserTopicFactoryProvider
from tests.courses.factories import (
    AuditionSectionFactory,
    AuditionTopicFactory,
    CourseFactory,
    GrammarSectionFactory,
    GrammarTopicFactory,
    LanguageFactory,
    UserCourseFactory,
)
from tests.users.factories import UserFactory


class TestTopicService(TestCase):
    def setUp(self):
        self.user = UserFactory()  # Припускаємо, що у вас є UserFactory
        self.from_language = LanguageFactory()
        self.to_language = LanguageFactory()
        self.course = CourseFactory(
            from_language=self.from_language, to_language=self.to_language
        )
        self.user_course = UserCourseFactory(user=self.user, course=self.course)

        # Створення секцій та тем для граматики і аудіювання
        self.grammar_sections = [
            GrammarSectionFactory(course=self.course, level=self.user_course.level)
            for _ in range(5)
        ]
        self.audition_sections = [
            AuditionSectionFactory(course=self.course, level=self.user_course.level)
            for _ in range(5)
        ]

        self.grammar_topics = [
            GrammarTopicFactory(section=section) for section in self.grammar_sections
        ]
        self.audition_topics = [
            AuditionTopicFactory(section=section) for section in self.audition_sections
        ]

        self.topic_provider = TopicFactoryProvider()
        self.user_topic_provider = UserTopicFactoryProvider()

    def test_grammar_first_method(self):
        grammar_factory = self.topic_provider.get_factory("grammar")
        first_topic = grammar_factory.first(
            course=self.course, level=self.user_course.level
        )
        self.assertEqual(first_topic, self.grammar_topics[0])

    def test_grammar_last_method(self):
        grammar_factory = self.topic_provider.get_factory("grammar")
        last_topic = grammar_factory.last(
            course=self.course, level=self.user_course.level
        )
        self.assertEqual(last_topic, self.grammar_topics[-1])

    def test_audition_first_method(self):
        audition_factory = self.topic_provider.get_factory("audition")
        first_topic = audition_factory.first(
            course=self.course, level=self.user_course.level
        )
        self.assertEqual(first_topic, self.audition_topics[0])

    def test_audition_last_method(self):
        audition_factory = self.topic_provider.get_factory("audition")
        last_topic = audition_factory.last(
            course=self.course, level=self.user_course.level
        )
        self.assertEqual(last_topic, self.audition_topics[-1])

    def test_grammar_next_method(self):
        grammar_factory = self.topic_provider.get_factory("grammar")
        first_topic = self.grammar_topics[0]
        next_topic = grammar_factory.next(topic_id=first_topic.id)
        self.assertEqual(next_topic, self.grammar_topics[1])

    def test_audition_next_method(self):
        audition_factory = self.topic_provider.get_factory("audition")
        first_topic = self.audition_topics[0]
        next_topic = audition_factory.next(topic_id=first_topic.id)
        self.assertEqual(next_topic, self.audition_topics[1])

    def test_topic_factory_provider_resolves_factories_correctly(self):
        self.assertIsInstance(
            self.topic_provider.get_factory("grammar"), GrammarTopicServiceFactory
        )
        self.assertIsInstance(
            self.topic_provider.get_factory("audition"), AuditionTopicServiceFactory
        )

    def test_reset_and_set_learning_status_grammar(self):
        factory = self.user_topic_provider.get_factory("grammar")
        topic = self.grammar_topics[0]

        # Встановлення теми для вивчення
        factory.set_learning_topic(self.user_course, topic.id)
        self.assertTrue(
            UserGrammarTopic.objects.filter(topic=topic, is_learning=True).exists()
        )

        # Ресет статусу вивчення
        factory.reset_learning_status(self.user_course)
        self.assertFalse(UserGrammarTopic.objects.filter(is_learning=True).exists())

    def test_reset_and_set_learning_status_audition(self):
        factory = self.user_topic_provider.get_factory("audition")
        topic = self.audition_topics[0]

        # Встановлення теми для вивчення
        factory.set_learning_topic(self.user_course, topic.id)
        self.assertTrue(
            UserAuditionTopic.objects.filter(topic=topic, is_learning=True).exists()
        )

        # Ресет статусу вивчення
        factory.reset_learning_status(self.user_course)
        self.assertFalse(UserAuditionTopic.objects.filter(is_learning=True).exists())

    def test_user_topic_provider_resolves_factories_correctly(self):
        grammar_factory = self.user_topic_provider.get_factory("grammar")
        audition_factory = self.user_topic_provider.get_factory("audition")

        self.assertIsInstance(grammar_factory, UserGrammarTopicServiceFactory)
        self.assertIsInstance(audition_factory, UserAuditionTopicServiceFactory)

    def test_set_topic_for_new_user(self):
        # Тест для користувача без дефолтної теми
        service = TopicService(self.user, "grammar")
        service.set_topic(None)

        self.assertTrue(
            UserGrammarTopic.objects.filter(
                user_course=self.user_course,
                topic=self.grammar_topics[0],
                is_learning=True,
            ).exists()
        )

    def test_update_topic_for_existing_user(self):
        # Створіть спочатку дефолтну тему
        service = TopicService(self.user, "grammar")
        service.set_topic(None)
        current_topic = UserGrammarTopic.objects.get(
            user_course=self.user_course, is_learning=True
        )
        next_topic_id = self.grammar_topics[1].id
        service.set_topic(current_topic.topic.pk)

        self.assertFalse(
            UserGrammarTopic.objects.filter(
                topic=self.grammar_topics[0], is_learning=True
            ).exists()
        )
        self.assertTrue(
            UserGrammarTopic.objects.filter(
                topic_id=next_topic_id, is_learning=True
            ).exists()
        )

    def test_no_available_topics_raises_exception(self):
        # Видалення всіх тем
        GrammarTopic.objects.all().delete()

        service = TopicService(self.user, "grammar")
        with self.assertRaises(NoAvailableTopics):
            service.set_topic(None)
