from django.urls import path

from .views import (
    UserDetailAPIView,
    UserListCreateAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    UserPasswordUpdateAPIView,
    UserTweetsAPIView,
)

urlpatterns = [
    path("api/v1/users", UserListCreateAPIView.as_view(), name="api_user_list"),
    path("api/v1/users/<int:pk>", UserDetailAPIView.as_view(), name="api_user_detail"),
    path(
        "api/v1/users/<int:pk>/tweets",
        UserTweetsAPIView.as_view(),
        name="api_user_tweet_list",
    ),
    path("api/v1/users/password", UserPasswordUpdateAPIView.as_view(), name="api_user_password_update"),
    path("api/v1/users/login", UserLoginAPIView.as_view(), name="api_user_login"),
    path("api/v1/users/logout", UserLogoutAPIView.as_view(), name="api_user_logout"),
]
