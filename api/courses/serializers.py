from rest_framework import serializers

from apps.courses.models import Course, ExerciseType, UserCourse


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class ExerciseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseType
        exclude = ["answer_schema"]


class UserCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCourse
        fields = "__all__"


class AddCourseSerializer(serializers.Serializer):
    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), write_only=True
    )
