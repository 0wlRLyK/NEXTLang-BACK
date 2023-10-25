from django.urls import path

from api.courses.views import CoursesListAPIView

app_name = "courses"
urlpatterns = [path("", CoursesListAPIView.as_view(), name="courses")]
