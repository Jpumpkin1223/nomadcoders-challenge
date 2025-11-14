from django.contrib import admin
from .models import Tweet, Like


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ['id', 'payload', 'user', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at', 'user']
    search_fields = ['payload', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'tweet', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at', 'user']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
