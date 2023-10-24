from typing import Dict

from rest_framework import serializers

from apps.users.models import User
from common.utils.uid import decode_uid


class PasswordMatchValidationMixin:
    def validate(self, attrs: Dict) -> Dict:
        super().validate(attrs)  # type: ignore
        if attrs.get("password") != attrs.get("password_repeat"):
            raise serializers.ValidationError(
                {
                    "password_repeat": "The password and password repeat fields must match"
                }
            )
        return attrs


class BaseUserActivationSerializer(serializers.Serializer):
    uid = serializers.CharField()

    @staticmethod
    def validate_user_by_uid(uid: str, check_is_active: bool = False) -> User:
        try:
            uid_decoded = decode_uid(uid)
            if "_" in uid_decoded:
                pk = int(uid_decoded.split("_")[0])
            else:
                pk = int(uid_decoded)
            user = User.objects.get(pk=pk)
            if user.is_active and check_is_active:
                raise serializers.ValidationError(
                    {"user": "User with this ID is already activated"}
                )
            return user

        except (ValueError, User.DoesNotExist) as e:
            if isinstance(e, ValueError):
                raise serializers.ValidationError({"uid": "The uid is incorrect"})
            else:
                raise serializers.ValidationError(
                    {"user": "There is no user with this ID"}
                )


class EmailValidationMixin:
    def validate_email(self, email: str) -> str:
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("There is no user with such email")
        return email
