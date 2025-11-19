from django.shortcuts import render

from .models import Tweet


def tweet_list(request):
    """모든 Tweets를 보여주는 뷰"""
    tweets = Tweet.objects.all()
    return render(request, "tweets/list.html", {"tweets": tweets})
