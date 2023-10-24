from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Primary user model that inherits from django AbstractUser
    Main fields are email (used as login), username, password
    """

    is_active = models.BooleanField(default=False)
    birthdate = models.DateField(null=True, default=None)
    avatar = models.ImageField(upload_to="users/avatars/", blank=True)
    requests_quantity = models.PositiveSmallIntegerField(
        default=1, help_text="Needs for salt generation for uid"
    )


class ActivationCode(models.Model):
    """
    Activation Code Model,
    utilized to retain an activation code associated with a user in the event of password or email change/reset.
    """

    class CodeTypes(models.TextChoices):
        PASSWORD = "password"  # noqa
        EMAIL = "email"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="activation_codes"
    )
    uid = models.CharField(max_length=50, verbose_name="User ID in base64")
    email = models.EmailField(
        blank=True, help_text="Used only in case of email changing confirmation"
    )
    code = models.CharField(max_length=255, verbose_name="Activation/confirmation code")
    expiration_date = models.DateTimeField(
        verbose_name="Expiration date of activation code"
    )
