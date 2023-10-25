from typing import Dict

from django.conf import settings
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken

from apps.courses.models import UserCourse
from apps.users.models import ActivationCode, User
from services.courses import UserDayService, UserWithoutDefaultCourse
from services.users.dto import AccessRefreshTokensDTO
from tasks.users import send_activation_email


class UsersService:
    """
    Service for performing operations on User model.
    Designed to encapsulate business logic related to User model.
    """

    def __init__(self, user: User):
        """
        Initialize the UsersService.

        :param user: The user instance to perform operations on.
        """
        self._user = user

    def _activate(self) -> None:
        """
        Activate the user by setting the `is_active` flag to True.
        """
        self._user.is_active = True
        self._user.save()

    def _get_token(self) -> AccessRefreshTokensDTO:
        """
        Activate the user by setting the `is_active` flag to True.
        """
        token = RefreshToken.for_user(self._user)
        return AccessRefreshTokensDTO(
            access=str(token.access_token), refresh=str(token)
        )

    def activate(self) -> AccessRefreshTokensDTO:
        self._activate()
        return self._get_token()

    def send_activation_email(self, is_created: bool) -> None:
        if settings.IS_TESTING:
            send_activation_email(user_pk=self._user.pk, is_created=is_created)
        else:
            transaction.on_commit(
                lambda: send_activation_email.delay(
                    user_pk=self._user.pk, is_created=is_created
                )
            )

    def set_password(self, password: str) -> None:
        """
        Set a new password for the user.

        :param password: The new password.
        """
        self._user.set_password(password)
        self._user.save()

    def set_email(self, email: str) -> None:
        """
        Set a new email for the user.

        :param email: The new email address.
        """
        self._user.email = email
        self._user.save()

    @transaction.atomic
    def confirm_password(self, password: str, uid: str, token: str) -> None:
        """
        Confirm and set a new password using an activation code.

        :param password: The new password.
        :param uid: The UID associated with the activation code.
        :param token: The actual activation code or token.
        """
        self.set_password(password)
        ActivationCode.objects.filter(user=self._user, uid=uid, code=token).delete()

    @transaction.atomic
    def confirm_email(self, uid: str, token: str) -> None:
        """
        Confirm and set a new email using an activation code.

        :param uid: The UID associated with the activation code.
        :param token: The actual activation code or token.
        """
        activation_code = ActivationCode.objects.get(
            user=self._user, uid=uid, code=token
        )
        self.set_email(activation_code.email)
        activation_code.delete()


class UnauthorizedUserService:
    @staticmethod
    @transaction.atomic
    def create_user(data: Dict, password: str) -> User:
        """
        Creates user
        :param data: data of user
        :param profile: data of user profile
        :param password: raw password
        :return: User object
        """
        default_course = data.pop("default_course", None)
        if not default_course:
            raise UserWithoutDefaultCourse

        user = User(**data)
        user.set_password(password)
        user.save()

        course = UnauthorizedUserService.create_user_course(user, default_course)
        UserDayService(course).get_or_create_user_day()
        return user

    @staticmethod
    def create_user_course(user: User, course: UserCourse) -> UserCourse:
        return UserCourse.objects.create(user=user, course=course)
