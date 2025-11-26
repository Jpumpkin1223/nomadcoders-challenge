from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Tweet


class TweetSerializer(serializers.ModelSerializer):
    """Tweet 모델을 직렬화하는 Serializer"""

    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Tweet
        fields = ["id", "payload", "user", "username", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "username", "created_at", "updated_at"]

    def create(self, validated_data):
        """요청한 사용자로 Tweet을 생성한다."""
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if user is None or not user.is_authenticated:
            raise serializers.ValidationError("인증된 사용자만 트윗을 작성할 수 있습니다.")
        return Tweet.objects.create(user=user, **validated_data)


class UserSerializer(serializers.ModelSerializer):
    """Django 기본 User 모델 직렬화"""

    class Meta:
        model = User
        fields = ["id", "username", "email", "date_joined", "last_login"]
        read_only_fields = ["id", "date_joined", "last_login"]


class UserCreateSerializer(serializers.ModelSerializer):
    """회원가입용 Serializer"""

    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password_confirm"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "비밀번호가 일치하지 않습니다."}
            )
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("password_confirm")
        return User.objects.create_user(password=password, **validated_data)


class PasswordUpdateSerializer(serializers.Serializer):
    """비밀번호 변경 Serializer"""

    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True, min_length=8)

    def validate_current_password(self, value):
        user = self.context.get("user")
        if not user.check_password(value):
            raise serializers.ValidationError("현재 비밀번호가 일치하지 않습니다.")
        return value

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError(
                {"new_password_confirm": "새 비밀번호가 일치하지 않습니다."}
            )
        if attrs["new_password"] == attrs["current_password"]:
            raise serializers.ValidationError(
                {"new_password": "새 비밀번호는 기존 비밀번호와 달라야 합니다."}
            )
        return attrs

    def save(self, **kwargs):
        user = self.context.get("user")
        new_password = self.validated_data["new_password"]
        user.set_password(new_password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """세션 로그인을 위한 Serializer"""

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("아이디 또는 비밀번호가 올바르지 않습니다.")
        attrs["user"] = user
        return attrs
