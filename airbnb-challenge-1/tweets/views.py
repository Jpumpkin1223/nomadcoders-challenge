from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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


class TweetListCreateAPIView(APIView):
    """GET: 전체 트윗 목록 / POST: 새 트윗 생성"""

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tweets = Tweet.objects.all()
        serializer = TweetSerializer(tweets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TweetSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            tweet = serializer.save()
            return Response(TweetSerializer(tweet).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TweetDetailAPIView(APIView):
    """단일 트윗 조회/수정/삭제"""

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Tweet, pk=pk)

    def get(self, request, pk):
        tweet = self.get_object(pk)
        serializer = TweetSerializer(tweet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        tweet = self.get_object(pk)
        if tweet.user != request.user:
            return Response(
                {"detail": "본인 트윗만 수정할 수 있습니다."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = TweetSerializer(tweet, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        tweet = self.get_object(pk)
        if tweet.user != request.user:
            return Response(
                {"detail": "본인 트윗만 삭제할 수 있습니다."},
                status=status.HTTP_403_FORBIDDEN,
            )
        tweet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
