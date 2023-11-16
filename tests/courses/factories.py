import factory
from factory.django import DjangoModelFactory
from faker import Faker

from apps.courses.models import Course, Language, UserCourse
from tests.users.factories import UserFactory, fake

faker = Faker()


class LanguageFactory(DjangoModelFactory):
    """Factory for the Language model."""

    class Meta:
        model = Language
        django_get_or_create = ("code",)

    name = factory.LazyAttribute(lambda x: faker.language_name())
    code = factory.LazyAttribute(lambda x: faker.language_code())


class LevelFactory(DjangoModelFactory):
    class Meta:
        model = "courses.Level"

    name = factory.Iterator(["Початківець", "Просунутий", "Експерт"])


class CourseFactory(DjangoModelFactory):
    """Factory for the Course model."""

    class Meta:
        model = Course

    name = factory.LazyAttribute(lambda x: faker.catch_phrase())
    from_language = factory.SubFactory(LanguageFactory)
    to_language = factory.SubFactory(LanguageFactory)

    @factory.post_generation
    def ensure_different_languages(self, create, extracted, **kwargs):
        if create and self.from_language == self.to_language:
            self.to_language = LanguageFactory()
            self.save()


class UserCourseFactory(DjangoModelFactory):
    class Meta:
        model = UserCourse

    user = factory.SubFactory(UserFactory)
    course = factory.SubFactory(CourseFactory)
    level = factory.SubFactory(LevelFactory)
    is_default = True


class SectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True

    course = factory.SubFactory(CourseFactory)
    name = factory.LazyFunction(fake.word)
    level = factory.SubFactory(LevelFactory)


class GrammarSectionFactory(SectionFactory):
    class Meta:
        model = "grammar.GrammarSection"


class AuditionSectionFactory(SectionFactory):
    class Meta:
        model = "audition.AuditionSection"


class TopicFactory(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True

    section = factory.SubFactory(SectionFactory)
    name = factory.LazyFunction(fake.word)
    slug = factory.LazyFunction(fake.slug)
    order = factory.Sequence(lambda n: n)


class GrammarTopicFactory(TopicFactory):
    class Meta:
        model = "grammar.GrammarTopic"


class AuditionTopicFactory(TopicFactory):
    class Meta:
        model = "audition.AuditionTopic"


class UserTopicFactory(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True

    user_course = factory.SubFactory(UserCourseFactory)
    topic = factory.SubFactory(TopicFactory)
    is_learning = False


class UserGrammarTopicFactory(UserTopicFactory):
    class Meta:
        model = "grammar.UserGrammarTopic"


class UserAuditionTopicFactory(UserTopicFactory):
    class Meta:
        model = "audition.UserAuditionTopic"
