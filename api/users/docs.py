from drf_yasg.utils import no_body, swagger_auto_schema

from api.users.serializers import (
    UserChangePasswordSerializer,
    UserResetPassword,
    UserSerializer, ConfirmPasswordSerializer,
)

# :: UsersUnauthorizedViewSet docs

signup_docs = swagger_auto_schema(
    operation_id="Users signup",
    request_body=UserSerializer,
    responses={200: UserSerializer, 400: "{'error_code': 'Error details'}"},
)

activate_docs = swagger_auto_schema(
    operation_id="Activation of user",
    request_body=no_body,
    responses={200: "", 400: "{'error_code': 'Error details'}"}
)

resend_activation_code_docs = swagger_auto_schema(
    operation_id="Resend activation code",
    request_body=no_body,
    responses={200: "", 400: "{'error_code': 'Error details'}"}
)

reset_password_docs = swagger_auto_schema(
    operation_id="Reset password of user",
    operation_description="Resets user password by email",
    request_body=UserResetPassword,
    responses={204: "", 400: "{'error_code': 'Error details'}"},
)

confirm_password_docs = swagger_auto_schema(
    operation_id="Confirmation of user's password",
    request_body=ConfirmPasswordSerializer,
    responses={204: "", 400: "{'error_code': 'Error details'}"},
)

confirm_email_docs = swagger_auto_schema(
    operation_id="Confirmation of changing email",
    request_body=no_body,
    responses={204: "", 400: "{'error_code': 'Error details'}"},
)

# :: UsersAuthorizedViewSet docs


password_change_docs = swagger_auto_schema(
    operation_id="User change password",
    request_body=UserChangePasswordSerializer,
    responses={204: "", 400: "{'error_code': 'Error details'}"},
)

