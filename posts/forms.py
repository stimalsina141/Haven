from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    def clean_content(self):
        content = self.cleaned_data.get("content", "").strip()
        if len(content) < 5:
            raise forms.ValidationError("Post is too short (min 5 characters).")
        return content
    
    class Meta:
        model = Post
        fields = ["content", "category"]
        widgets = {
            "content": forms.Textarea(
                attrs={"placeholder": "Share your thoughts anonymously...", "rows":4}
            ),
        }


class CommentForm(forms.ModelForm):
    def clean_content(self):
        content = self.cleaned_data.get("content", "").strip()
        if len(content) < 2:
            raise forms.ValidationError("Reply is too short (min 2 characters).")
        return content
    
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"placeholder": "Write a supportive reply...", "rows": 3}
            ),
        }
        labels = {"content": ""}