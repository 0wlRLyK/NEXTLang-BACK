from rest_framework import serializers

from apps.grammar.models import GrammarSection, GrammarTopic, UserGrammarTopic


class GrammarTopicSerializer(serializers.ModelSerializer):
    is_learning = serializers.SerializerMethodField()
    is_passed = serializers.SerializerMethodField()

    class Meta:
        model = GrammarTopic
        fields = "__all__"

    def get_is_learning(self, obj):
        # Перевірка, чи існує UserTopic для даного користувача і даної теми
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            return UserGrammarTopic.objects.filter(
                user_course__user=request.user, topic=obj, is_learning=True
            ).exists()
        return False

    def get_is_passed(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            return UserGrammarTopic.objects.filter(
                user_course__user=request.user, topic=obj, is_passed=True
            ).exists()
        return False


class GrammarSectionSerializer(serializers.ModelSerializer):
    topics = GrammarTopicSerializer(many=True, read_only=True)

    class Meta:
        model = GrammarSection
        fields = "__all__"


class UserGrammarTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGrammarTopic
        fields = "__all__"
