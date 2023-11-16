from django.urls import path

from api.grammar.views import GrammarSectionsListAPIView, GrammarTopicAPIViewSet

app_name = "grammar"
urlpatterns = [
    path("sections/", GrammarSectionsListAPIView.as_view(), name="sections_list"),
    path("topic/", GrammarTopicAPIViewSet.as_view({"get": "retrieve"}), name="topic"),
]
