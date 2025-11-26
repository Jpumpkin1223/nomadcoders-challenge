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
