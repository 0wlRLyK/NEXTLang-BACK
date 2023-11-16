from abc import ABC
from typing import Optional

from apps.audition.models import AuditionTopic, UserAuditionTopic
from apps.courses.constants import SphereLiteral
from apps.grammar.models import GrammarTopic, UserGrammarTopic
from services.courses import UserCourseService
from services.courses.dto import LearningSphereDTO
from services.courses.exceptions import NoAvailableTopics


class TopicFactory(ABC):
    model = None  # Визначається у підкласах

    def get_query_set(self, **filters):
        return self.model.objects.filter(**filters)

    def first(self, course, level):
        return self.get_query_set(section__course=course, section__level=level).first()

    def next(self, topic_id: int):
        # Спочатку отримуємо поточну тему за її id
        current_topic = self.get_query_set(id=topic_id).first()
        if not current_topic:
            return None

        # Потім шукаємо наступну тему
        next_topic = self.get_query_set(
            section=current_topic.section, order__gt=current_topic.order
        ).first()

        # Якщо наступної теми немає у поточному розділі, шукаємо першу тему в наступному розділі
        if not next_topic:
            next_topic = self.get_query_set(
                section__order=current_topic.section.order + 1
            ).first()

        return next_topic

    def last(self, course, level):
        return self.get_query_set(section__course=course, section__level=level).last()


class GrammarTopicFactory(TopicFactory):
    model = GrammarTopic


class AuditionTopicFactory(TopicFactory):
    model = AuditionTopic


class UserTopicFactory:
    model = None

    def reset_learning_status(self, user_course):
        self.model.objects.filter(user_course=user_course).update(is_learning=False)

    def set_learning_topic(self, user_course, topic_id):
        if topic_id:
            user_learning_topic, created = self.model.objects.get_or_create(
                user_course=user_course,
                topic_id=topic_id,
                defaults={"is_learning": True},
            )
            if not created:
                user_learning_topic.is_learning = True
                user_learning_topic.save()
        else:
            raise NoAvailableTopics


class UserGrammarTopicFactory(UserTopicFactory):
    model = UserGrammarTopic


class UserAuditionTopicFactory(UserTopicFactory):
    model = UserAuditionTopic


class TopicFactoryProvider:
    def __init__(self):
        self.factory_mapping = LearningSphereDTO(
            grammar=GrammarTopicFactory(), audition=AuditionTopicFactory()
        )

    def get_factory(self, sphere: SphereLiteral):
        return self.factory_mapping.get(sphere)


class UserTopicFactoryProvider:
    def __init__(self):
        self.factory_mapping = LearningSphereDTO(
            grammar=UserGrammarTopicFactory(), audition=UserAuditionTopicFactory()
        )

    def get_factory(self, sphere: SphereLiteral):
        return self.factory_mapping.get(sphere)


class TopicService:
    def __init__(self, user, sphere: SphereLiteral):
        self.user = user
        self.user_course = UserCourseService(user).get_user_course()
        self.sphere: SphereLiteral = sphere

    def _get_topic(self, topic_id: Optional[int]):
        topic_factory = TopicFactoryProvider().get_factory(self.sphere)
        if topic_id:
            return topic_factory.next(topic_id)
        else:
            return topic_factory.first(
                course=self.user_course.course, level=self.user_course.level
            )

    def set_topic(self, topic_id: Optional[int]):
        user_topic_factory = UserTopicFactoryProvider().get_factory(self.sphere)
        user_topic_factory.reset_learning_status(self.user_course)
        topic = self._get_topic(topic_id)
        if topic:
            user_topic_factory.set_learning_topic(self.user_course, topic.pk)
        else:
            raise NoAvailableTopics
