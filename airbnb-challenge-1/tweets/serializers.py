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
