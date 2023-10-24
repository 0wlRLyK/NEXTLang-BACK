from typing import Dict

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.models import User
from services.users import UsersService


@receiver(post_save, sender=User)
def create_user(sender, instance: User, created: bool, **kwargs: Dict):
    """
    Post signal after creation user
    :param sender: User model
    :param instance:  User model
    :param created: check is object created
    :param kwargs: other params
    :return: None
    """
    if created:
        UsersService(instance).send_activation_email(is_created=created)
