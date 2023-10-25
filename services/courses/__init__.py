from django.contrib.auth import get_user_model

from apps.courses.models import UserCourse
from services.courses.day import UserDayService
from services.courses.exceptions import UserWithoutDefaultCourse

User = get_user_model()


class UserCourseService:
    def __init__(self, user: User):
        self.user = user
        self.user_course = self._get_user_course()
        self.user_day = self.get_or_create_user_day()

    def _get_user_course(self):
        try:
            UserCourse.objects.get(user=self.user, is_default=True).first()
        except UserCourse.DoesNotExist:
            raise UserWithoutDefaultCourse

    def get_or_create_user_day(self):
        return UserDayService(self.user_course).get_or_create_user_day()
