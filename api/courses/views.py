from typing import Any, Dict, Tuple

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.courses.exceptions import CourseAlreadyStudyingAPIException
from api.courses.serializers import (
    AddCourseSerializer,
    CourseSerializer,
    ExerciseTypeSerializer,
    UserCourseSerializer,
)
from apps.courses.models import Course, ExerciseType, UserCourse
from common.views import CustomModelViewSet, action_with_serializer
from services.courses import CourseAlreadyStudyingException, UserCourseService


class CoursesListAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    http_method_names = ["get"]


class ExerciseTypeListAPIView(ListAPIView):
    queryset = ExerciseType.objects.all()
    serializer_class = ExerciseTypeSerializer
    http_method_names = ["get"]


class UserCoursesViewSet(CustomModelViewSet):
    serializer_class = UserCourseSerializer
    permission_classes = [IsAuthenticated]
    service_class = UserCourseService
    http_method_names = ["get", "post"]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user.courses.all()
        return UserCourse.objects.none()

    @action_with_serializer(
        methods=["POST"], detail=False, serializer_class=AddCourseSerializer
    )
    def add_course(
        self, request: Request, *args: Tuple[Any], **kwargs: Dict
    ) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.service_class(self.request.user).add_course(
                serializer.validated_data.get("course")
            )
        except CourseAlreadyStudyingException:
            raise CourseAlreadyStudyingAPIException()
        return Response(status=status.HTTP_204_NO_CONTENT)
