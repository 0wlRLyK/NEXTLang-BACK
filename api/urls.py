from django.urls import include, path

from api.users.views import CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    path("users/", include("api.users.urls")),
    path("courses/", include("api.courses.urls")),
    path("audition/", include("api.audition.urls")),
    path("grammar/", include("api.grammar.urls")),
    path("token/", CustomTokenObtainPairView.as_view(), name="token"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
]
