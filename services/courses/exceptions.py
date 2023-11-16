class UserWithoutDefaultCourseException(BaseException):
    """Exception when user doesn't have default course"""


class CourseAlreadyStudyingException(BaseException):
    """Exception when the user is already studying this course"""


class NoExerciseOptionsAvailableException(BaseException):
    """Exception when there are no available options for this exercise"""


class InvalidAnswerSchemaException(BaseException):
    """Raises when schema is invalid"""


class WrongAnswerException(BaseException):
    """Raises when user pass wrong answer"""


class NoAvailableTopics(BaseException):
    """There is no available topics found by this filter"""
