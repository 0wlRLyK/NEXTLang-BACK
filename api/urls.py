from django.urls import include, path

# fmt: off
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# fmt: on

urlpatterns = [
    path("users/", include("api.users.urls")),
    path("courses/", include("api.courses.urls")),
    path("audition/", include("api.audition.urls")),
    path("grammar/", include("api.grammar.urls")),
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
