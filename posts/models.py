from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Post(models.Model):
    CATEGORY_CHOICES = [
        ("celebration", "Celebration"),
        ("struggle", "Struggle"),
        ("decision", "Decision Help"),
        ("grief", "Grief"),
    ]

    content = models.TextField()
    category = models.CharField(max_length=20, choices = CATEGORY_CHOICES)
    anonymous_username = models.CharField(max_length=50,blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    reported = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.anonymous_username:
            self.anonymous_username = f"User_{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)

    
    def __str__(self):
        return f"{self.category} - {self.anonymous_username}: {self.content[:30]}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    anonymous_username = models.CharField(max_length=50, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    reported = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.anonymous_username:
            self.anonymous_username = f"User_{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Comment by {self.anonymous_username} on Post {self.post_id}"