from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "anonymous_username", "author", "reported", "created_at")
    list_filter = ("category", "reported", "created_at")
    search_fields = ("content", "anonymous_username", "author__username")
    ordering = ("-created_at",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "anonymous_username", "author", "reported", "created_at")
    list_filter = ("reported", "created_at")
    search_fields = ("content", "anonymous_username", "author__username", "post__content")
    ordering = ("-created_at",)