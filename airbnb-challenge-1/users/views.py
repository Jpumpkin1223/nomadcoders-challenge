from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from tweets.models import Tweet
from tweets.serializers import TweetSerializer

from .serializers import (
    LoginSerializer,
    PasswordUpdateSerializer,
    UserCreateSerializer,
    UserSerializer,
)


class UserListCreateAPIView(APIView):
    """GET: 사용자 목록 / POST: 회원가입"""

    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(APIView):
    """단일 사용자 정보"""

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserTweetsAPIView(APIView):
    """특정 사용자의 트윗 목록"""

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        tweets = Tweet.objects.filter(user=user)
        serializer = TweetSerializer(tweets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserPasswordUpdateAPIView(APIView):
    """로그인 사용자의 비밀번호를 변경한다."""

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = PasswordUpdateSerializer(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "비밀번호가 변경되었습니다."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    """세션 기반 로그인"""

    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(APIView):
    """세션 기반 로그아웃"""

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"detail": "로그아웃되었습니다."}, status=status.HTTP_200_OK)
