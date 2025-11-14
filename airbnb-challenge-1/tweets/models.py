from django.db import models
from django.contrib.auth.models import User


class TimeStampedModel(models.Model):
    """추상 기본 클래스: created_at과 updated_at 필드를 제공"""
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class Tweet(TimeStampedModel):
    """트윗 모델"""
    payload = models.TextField(max_length=180)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.payload[:50]}"


class Like(TimeStampedModel):
    """좋아요 모델"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ['user', 'tweet']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} likes {self.tweet.id}"
