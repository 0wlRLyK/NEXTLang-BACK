from rest_framework import serializers

from apps.audition.models import AuditionSection, AuditionTopic, UserAuditionTopic


class AuditionTopicSerializer(serializers.ModelSerializer):
    is_learning = serializers.SerializerMethodField()
    is_passed = serializers.SerializerMethodField()

    class Meta:
        model = AuditionTopic
        fields = "__all__"

    def get_is_learning(self, obj):
        # Перевірка, чи існує UserTopic для даного користувача і даної теми
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            return UserAuditionTopic.objects.filter(
                user_course__user=request.user, topic=obj, is_learning=True
            ).exists()
        return False

    def get_is_passed(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            return UserAuditionTopic.objects.filter(
                user_course__user=request.user, topic=obj, is_passed=True
            ).exists()
        return False


class AuditionSectionSerializer(serializers.ModelSerializer):
    topics = AuditionTopicSerializer(many=True, read_only=True)

    class Meta:
        model = AuditionSection
        fields = "__all__"


class UserAuditionTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAuditionTopic
        fields = "__all__"
