from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException


class CourseAlreadyStudyingAPIException(APIException):
    """Already studying course"""

    status_code = 400
    default_detail = _("You are already studying this course")
    default_code = "course_already_studying"
