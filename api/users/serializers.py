from typing import Dict

from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.timezone import now
from rest_framework import serializers

from api.users.mixins.serializers import (
    BaseUserActivationSerializer,
    EmailValidationMixin,
    PasswordMatchValidationMixin,
)
from apps.users.models import User
from tasks.users import send_email_confirmation


class UserSerializer(PasswordMatchValidationMixin, serializers.ModelSerializer):
    password_repeat = serializers.CharField(write_only=True, required=True)

    def validate_password(self, value):
        validate_password(value)
        return value

    def update(self, instance, validated_data):
        if "email" in validated_data and validated_data["email"] != instance.email:
            if settings.IS_TESTING:
                send_email_confirmation(
                    user_pk=instance.pk, email=validated_data["email"]
                )
            else:
                send_email_confirmation.delay(
                    user_pk=instance.pk, email=validated_data["email"]
                )
            validated_data["email"] = instance.email
        return super().update(instance, validated_data)

    class Meta:
        model = User
        exclude = ["groups", "user_permissions"]
        extra_kwargs = {
            "password": {"write_only": True},
            "following": {"read_only": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }


class ExtendedUserSerializer(UserSerializer):
    likes_quantity = serializers.IntegerField(default=0, read_only=True)
    followers_quantity = serializers.IntegerField(default=0, read_only=True)
    following_quantity = serializers.IntegerField(default=0, read_only=True)


class FollowingUserSerializer(UserSerializer):
    following = UserSerializer(source="limited_following", many=True, read_only=True)


class FollowingAndFollowersUserSerializer(UserSerializer):
    following = UserSerializer(many=True, read_only=True)
    followers = UserSerializer(many=True, read_only=True)


class UserActivationSerializer(BaseUserActivationSerializer):
    token = serializers.CharField()

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        internal_value["user"] = self.validate_user_by_uid(
            internal_value["uid"], check_is_active=True
        )
        return internal_value

    def validate(self, attrs: Dict) -> Dict:
        user = attrs["user"]
        token = attrs["token"]

        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError({"token": "This token is invalid"})
        return attrs


class UserChangePasswordSerializer(
    PasswordMatchValidationMixin, serializers.Serializer
):
    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    def validate_password(self, value):
        validate_password(value)
        return value


class UserResetPassword(EmailValidationMixin, serializers.Serializer):
    email = serializers.EmailField()


class ConfirmEmailSerializer(BaseUserActivationSerializer):
    token = serializers.CharField()

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        internal_value["user"] = self.validate_user_by_uid(internal_value["uid"])
        return internal_value

    def validate(self, attrs: Dict) -> Dict:
        super().validate(attrs)
        user = attrs["user"]
        try:
            token = attrs["token"]
        except Exception:
            raise serializers.ValidationError({"token": "Token is invalid"})

        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError({"token": "This token is invalid"})
        activation_codes = user.activation_codes.filter(uid=attrs["uid"], code=token)
        if not activation_codes.exists():
            raise serializers.ValidationError(
                {"activation_code": "This activation code doesn't belong this user"}
            )
        activation_code = activation_codes.first()
        if now() > activation_code.expiration_date:
            raise serializers.ValidationError({"token": "This token is expired"})
        return attrs


class ConfirmPasswordSerializer(ConfirmEmailSerializer, UserChangePasswordSerializer):
    def validate(self, attrs: Dict) -> Dict:
        attrs = UserChangePasswordSerializer.validate(self, attrs)
        attrs = ConfirmEmailSerializer.validate(self, attrs)
        return attrs


class ResendUserActivationCodeSerializer(EmailValidationMixin, serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value: str) -> str:
        super().validate_email(value)
        user = User.objects.filter(email=value, is_active=True)
        if user.exists():
            raise serializers.ValidationError(
                "There is no inactive user with such email"
            )
        return value
