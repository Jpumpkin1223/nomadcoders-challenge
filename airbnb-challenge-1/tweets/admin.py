from django.contrib import admin

from .models import Like, Tweet


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "payload",
        "user",
        "like_count",
        "created_at",
        "updated_at",
    ]
    list_filter = ["created_at", "updated_at", "user"]
    search_fields = ["payload", "user__username"]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "created_at"

    def like_count(self, obj):
        return obj.likes.count()

    like_count.short_description = "Likes"


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "tweet", "created_at", "updated_at"]
    list_filter = ["created_at", "updated_at", "user"]
    search_fields = ["user__username"]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "created_at"
