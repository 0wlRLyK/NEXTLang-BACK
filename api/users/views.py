from dataclasses import asdict
from typing import Any, Dict, Optional, Tuple

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AnonymousUser
from django.http import Http404
from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response

from api.users.docs import (
    activate_docs,
    confirm_email_docs,
    confirm_password_docs,
    password_change_docs,
    resend_activation_code_docs,
    reset_password_docs,
    signup_docs,
)
from api.users.serializers import (
    ConfirmEmailSerializer,
    ConfirmPasswordSerializer,
    ResendUserActivationCodeSerializer,
    UserActivationSerializer,
    UserChangePasswordSerializer,
    UserResetPassword,
    UserSerializer,
)
from apps.users.models import User
from common.views import CustomViewSet  # type: ignore
from common.views import CustomModelViewSet, action_with_serializer
from services.users import UnauthorizedUserService, UsersService
from tasks.users import send_password_activation


class UsersUnauthorizedViewSet(CustomViewSet):
    """
    ViewSet with actions for unauthorized users
    """

    permission_classes = [permissions.AllowAny]
    http_method_names = ["post"]
    tags = ["Users [unauthorized]"]
    service = UsersService

    @signup_docs
    @action_with_serializer(
        detail=False,
        methods=["post"],
        serializer_class=UserSerializer,
        permission_classes=[permissions.AllowAny],
    )
    def signup(self, request: Request, *args: Tuple[Any], **kwargs: Dict) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        password = data.pop("password")
        # Delete password_repeat field because it was needed only for validation
        data.pop("password_repeat")
        instance = UnauthorizedUserService.create_user(data=data, password=password)
        serializer = self.get_serializer(instance)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @activate_docs
    @action_with_serializer(
        methods=["POST"], detail=True, serializer_class=UserActivationSerializer
    )
    def activate(self, request, *args: Tuple[Any], **kwargs: Dict):
        data = {"uid": kwargs["uid"], "token": kwargs["token"]}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        response_data = self.service(serializer.validated_data.get("user")).activate()
        return Response(data=asdict(response_data), status=status.HTTP_200_OK)

    @reset_password_docs
    @action_with_serializer(
        methods=["POST"], detail=True, serializer_class=UserResetPassword
    )
    def reset_password(self, request, *args: Tuple[Any], **kwargs: Dict):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if settings.IS_TESTING:
            send_password_activation(user_email=serializer.validated_data["email"])
        else:
            send_password_activation.delay(
                user_email=serializer.validated_data["email"]
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    @confirm_password_docs
    @action_with_serializer(
        methods=["POST"], detail=True, serializer_class=ConfirmPasswordSerializer
    )
    def confirm_password(self, request, *args: Tuple[Any], **kwargs: Dict):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        self.service(data["user"]).confirm_password(
            password=data["password"], uid=data["uid"], token=data["token"]
        )

        return Response(status=status.HTTP_204_NO_CONTENT)

    @confirm_email_docs
    @action_with_serializer(
        methods=["POST"], detail=True, serializer_class=ConfirmEmailSerializer
    )
    def confirm_email(self, request, *args: Tuple[Any], **kwargs: Dict):
        data: Dict = {"uid": kwargs["uid"], "token": kwargs["token"]}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.service(serializer.validated_data["user"]).confirm_email(
            uid=data["uid"], token=data["token"]
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @resend_activation_code_docs
    @action_with_serializer(
        methods=["POST"],
        detail=True,
        serializer_class=ResendUserActivationCodeSerializer,
    )
    def resend_activation_code(self, request, *args: Tuple[Any], **kwargs: Dict):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=serializer.validated_data.get("email"))
        self.service(user).send_activation_email(is_created=False)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UsersAuthorizedViewSet(CustomModelViewSet):
    tags = ["Users [authorized]"]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ["post", "get", "put", "patch", "delete"]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    service = UsersService

    def get_object(self) -> Optional[AbstractBaseUser | AnonymousUser]:
        if self.kwargs.get("pk"):
            pk = self.kwargs["pk"]
        else:
            pk = self.request.user.pk
        try:
            user = self.get_queryset().get(pk=pk, is_active=True)
        except User.DoesNotExist:
            raise Http404("User not found")
        return user

    @password_change_docs
    @action_with_serializer(
        detail=False,
        methods=["post"],
        serializer_class=UserChangePasswordSerializer,
        permission_classes=[permissions.IsAuthenticated],
    )
    def password_change(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not isinstance(request.user, AnonymousUser):
            user = request.user
            self.service(user).set_password(serializer.validated_data.get("password"))
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super(UsersAuthorizedViewSet, self).list(request, args, kwargs)
