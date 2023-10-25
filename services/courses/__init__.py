from django.contrib.auth import get_user_model

from apps.courses.models import Course, UserCourse
from services.courses.day import UserDayService
from services.courses.exceptions import CourseAlreadyStudying, UserWithoutDefaultCourse

User = get_user_model()


class UserCourseService:
    def __init__(self, user: User):
        self.user = user
        self.user_course = self._get_user_course()
        self.user_day = self.get_or_create_user_day()

    def _get_user_course(self):
        try:
            course = UserCourse.objects.get(user=self.user, is_default=True)
        except UserCourse.DoesNotExist:
            raise UserWithoutDefaultCourse
        return course

    def get_or_create_user_day(self):
        return UserDayService(self.user_course).get_or_create_user_day()

    def _course_validation(self, course):
        if UserCourse.objects.filter(user=self.user, course=course).exists():
            raise CourseAlreadyStudying

    def add_course(self, course: Course):
        self._course_validation(course)
        # Set all courses for this user to is_default=False
        UserCourse.objects.filter(user=self.user).update(is_default=False)

        # Create new default course
        user_course = UserCourse.objects.create(
            user=self.user, course=course, is_default=True
        )
        UserDayService(self.user_course).get_or_create_user_day()
        return user_course
