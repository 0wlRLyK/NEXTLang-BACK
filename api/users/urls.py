from django.urls import path

from api.users.views import UsersAuthorizedViewSet, UsersUnauthorizedViewSet

app_name = "users"
urlpatterns = [
    path(
        "",
        UsersAuthorizedViewSet.as_view(
            {
                "get": "retrieve",
                "patch": "partial_update",
                "put": "update",
                "delete": "destroy",
            }
        ),
        name="user",
    ),
    path(
        "<int:pk>/",
        UsersAuthorizedViewSet.as_view(
            {
                "get": "retrieve",
            }
        ),
        name="user",
    ),
    path(
        "list/",
        UsersAuthorizedViewSet.as_view(
            {
                "get": "list",
            }
        ),
        name="list",
    ),
    path(
        "signup/", UsersUnauthorizedViewSet.as_view({"post": "signup"}), name="signup"
    ),
    path(
        "activate/<str:uid>/<str:token>/",
        UsersUnauthorizedViewSet.as_view({"post": "activate"}),
        name="activate",
    ),
    path(
        "confirm-email/<str:uid>/<str:token>/",
        UsersUnauthorizedViewSet.as_view({"post": "confirm_email"}),
        name="confirm-email",
    ),
    path(
        "reset-password/",
        UsersUnauthorizedViewSet.as_view({"post": "reset_password"}),
        name="reset-password",
    ),
    path(
        "confirm-password/",
        UsersUnauthorizedViewSet.as_view({"post": "confirm_password"}),
        name="confirm-password",
    ),
    path(
        "password-change/",
        UsersAuthorizedViewSet.as_view({"post": "password_change"}),
        name="password-change",
    ),
    path(
        "resend-activation-code/",
        UsersUnauthorizedViewSet.as_view({"post": "resend_activation_code"}),
        name="resend-activation-code",
    ),
]
