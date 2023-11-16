from django.urls import path

from api.audition.views import AuditionSectionsListAPIView, AuditionTopicAPIViewSet

app_name = "audition"
urlpatterns = [
    path("sections/", AuditionSectionsListAPIView.as_view(), name="sections_list"),
    path("topic/", AuditionTopicAPIViewSet.as_view({"get": "retrieve"}), name="topic"),
]
