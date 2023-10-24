# type: ignore
from datetime import date, timedelta

import factory
from django.utils.timezone import now
from factory import SubFactory
from factory.django import DjangoModelFactory
from faker import Faker

from apps.users.models import ActivationCode, User
from common.utils.uid import encode_uid

fake = Faker()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.LazyAttribute(lambda x: fake.unique.email())
    username = factory.LazyAttribute(lambda x: fake.unique.user_name())
    password = factory.PostGenerationMethodCall("set_password", "testpassword")
    avatar = factory.django.ImageField(color="blue")
    birthdate = factory.LazyAttribute(
        lambda o: date.today() - timedelta(days=(18) * 365.25)
    )
    is_active = True


class ActivationCodeFactory(DjangoModelFactory):
    class Meta:
        model = ActivationCode

    user = SubFactory(UserFactory)
    uid = factory.LazyAttribute(lambda o: encode_uid(o.user.pk))
    email = factory.Maybe(
        "include_email", factory.LazyAttribute(lambda x: x.user.email), ""
    )
    code = factory.Sequence(lambda n: f"code{n}")
    expiration_date = factory.LazyAttribute(lambda _: now() + timedelta(days=1))
