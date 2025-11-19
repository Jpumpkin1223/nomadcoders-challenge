from django.contrib import admin

from .models import Like, Tweet


class ElonMuskFilter(admin.SimpleListFilter):
    title = "Elon Musk"
    parameter_name = "elon_musk"

    def lookups(self, request, model_admin):
        return [
            ("contains", "Contains Elon Musk"),
            ("not_contains", "Doesn't contain Elon Musk"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "contains":
            return queryset.filter(payload__icontains="Elon Musk")
        if self.value() == "not_contains":
            return queryset.exclude(payload__icontains="Elon Musk")
        return queryset


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
    list_filter = ["created_at", "updated_at", "user", ElonMuskFilter]
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
