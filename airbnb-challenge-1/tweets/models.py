from django.contrib.auth.models import User
from django.db import models

from common.models import TimeStampedModel


class Tweet(TimeStampedModel):
    """트윗 모델"""

    payload = models.TextField(max_length=180)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username}: {self.payload[:50]}"


class Like(TimeStampedModel):
    """좋아요 모델"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ["user", "tweet"]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} likes {self.tweet.id}"
