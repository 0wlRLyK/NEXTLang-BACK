from django.db.models import Prefetch
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from api.audition.serializers import (
    AuditionSectionSerializer,
    UserAuditionTopicSerializer,
)
from apps.audition.models import AuditionSection, UserAuditionTopic
from common.views import CustomModelViewSet
from services.courses import UserCourseService


class AuditionSectionsListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AuditionSectionSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            user_course = UserCourseService(user=user).get_user_course()
            user_topics = UserAuditionTopic.objects.filter(user_course__user=user)
            return AuditionSection.objects.prefetch_related(
                Prefetch(
                    "topics__user_topics", queryset=user_topics, to_attr="users_topics"
                ),
                "topics",
            ).filter(level_id=user_course.level_id)
        return AuditionSection.objects.none()


class AuditionTopicAPIViewSet(CustomModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserAuditionTopicSerializer

    def get_object(self):
        user = self.request.user
        if user.is_authenticated:
            return UserAuditionTopic.objects.get(
                is_learning=True, user_course__user=user, user_course__is_default=True
            )
        return UserAuditionTopic.objects.none()
