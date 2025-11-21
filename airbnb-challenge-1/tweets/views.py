from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Tweet
from .serializers import TweetSerializer


def tweet_list(request):
    """모든 Tweets를 보여주는 뷰"""
    tweets = Tweet.objects.all()
    return render(request, "tweets/list.html", {"tweets": tweets})


class TweetListAPIView(APIView):
    """모든 Tweets를 반환하는 API 뷰"""

    def get(self, request):
        tweets = Tweet.objects.all()
        serializer = TweetSerializer(tweets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserTweetListAPIView(APIView):
    """특정 User의 모든 Tweets를 반환하는 API 뷰"""

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        tweets = Tweet.objects.filter(user=user)
        serializer = TweetSerializer(tweets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
