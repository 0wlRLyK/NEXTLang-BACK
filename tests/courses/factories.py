import factory
from factory.django import DjangoModelFactory
from faker import Faker

from apps.courses.models import Course, Language

faker = Faker()


class LanguageFactory(DjangoModelFactory):
    """Factory for the Language model."""

    class Meta:
        model = Language
        django_get_or_create = ("code",)

    name = factory.LazyAttribute(lambda x: faker.language_name())
    code = factory.LazyAttribute(lambda x: faker.language_code())


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
