from django.urls import include, path

# fmt: off
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# fmt: on

urlpatterns = [
    path("users/", include("api.users.urls")),
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
