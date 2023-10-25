from datetime import date

from apps.courses.models import UserCourse, UserDay


class UserDayService:
    def __init__(self, user_course: UserCourse):
        self.user_course = user_course
        self.user_day = self.get_or_create_user_day()

    def get_or_create_user_day(self):
        user_day, created = UserDay.objects.get_or_create(
            date=date.today(),
            user_course=self.user_course,
        )
        return user_day
