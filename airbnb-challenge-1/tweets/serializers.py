from rest_framework import serializers

from .models import Tweet


class TweetSerializer(serializers.Serializer):
    """Tweet 모델을 직렬화하는 Serializer"""

    id = serializers.IntegerField(read_only=True)
    payload = serializers.CharField(max_length=180)
    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

