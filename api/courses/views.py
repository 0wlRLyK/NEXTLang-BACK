from rest_framework.generics import ListAPIView

from api.courses.serializers import CourseSerializer
from apps.courses.models import Course


class CoursesListAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    http_method_names = ["get"]
