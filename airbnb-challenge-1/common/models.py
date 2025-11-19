from django.db import models


class TimeStampedModel(models.Model):
    """추상 기본 클래스: created_at과 updated_at 필드를 제공"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
