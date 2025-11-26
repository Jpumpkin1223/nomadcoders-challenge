"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from tweets import views

urlpatterns = [
    path("", views.tweet_list, name="tweet_list"),
    path(
        "api/v1/tweets",
        views.TweetListCreateAPIView.as_view(),
        name="api_tweet_list",
    ),
    path(
        "api/v1/tweets/<int:pk>",
        views.TweetDetailAPIView.as_view(),
        name="api_tweet_detail",
    ),
    path("api/v1/users", views.UserListCreateAPIView.as_view(), name="api_user_list"),
    path(
        "api/v1/users/<int:pk>",
        views.UserDetailAPIView.as_view(),
        name="api_user_detail",
    ),
    path(
        "api/v1/users/password",
        views.UserPasswordUpdateAPIView.as_view(),
        name="api_user_password_update",
    ),
    path(
        "api/v1/users/<int:pk>/tweets",
        views.UserTweetsAPIView.as_view(),
        name="api_user_tweet_list",
    ),
    path("admin/", admin.site.urls),
]
