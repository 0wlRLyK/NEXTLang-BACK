from django.urls import path

from api.courses.views import (
    CoursesListAPIView,
    ExerciseTypeListAPIView,
    UserCoursesViewSet,
)

app_name = "courses"
urlpatterns = [
    path("", CoursesListAPIView.as_view(), name="courses_list"),
    path("add/", UserCoursesViewSet.as_view({"post": "add_course"}), name="add_course"),
    path("my/", UserCoursesViewSet.as_view({"get": "list"}), name="my_courses_list"),
    path("exercise-types/", ExerciseTypeListAPIView.as_view(), name="exercise-types"),
]
