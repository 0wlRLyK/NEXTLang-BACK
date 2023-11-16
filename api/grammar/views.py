from django.db.models import Prefetch
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from api.grammar.serializers import GrammarSectionSerializer, UserGrammarTopicSerializer
from apps.grammar.models import GrammarSection, UserGrammarTopic
from common.views import CustomModelViewSet
from services.courses import UserCourseService


class GrammarSectionsListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GrammarSectionSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            user_course = UserCourseService(user=user).get_user_course()
            user_topics = UserGrammarTopic.objects.filter(user_course__user=user)
            return GrammarSection.objects.prefetch_related(
                Prefetch(
                    "topics__user_topics", queryset=user_topics, to_attr="users_topics"
                ),
                "topics",
            ).filter(level_id=user_course.level_id)
        return GrammarSection.objects.none()


class GrammarTopicAPIViewSet(CustomModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserGrammarTopicSerializer

    def get_object(self):
        user = self.request.user
        if user.is_authenticated:
            return UserGrammarTopic.objects.get(
                is_learning=True, user_course__user=user, user_course__is_default=True
            )
        return UserGrammarTopic.objects.none()
