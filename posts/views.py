from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.contrib.admin.views.decorators import staff_member_required

from .models import Post, Comment
from .forms import PostForm, CommentForm


def home(request):
    category = request.GET.get("category")

    if category:
        posts = Post.objects.filter(category=category).order_by("?")
    else:
        posts = Post.objects.all().order_by("?")

    return render(
        request,
        "posts/home.html",
        {"posts": posts, "selected_category": category},
    )


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            now = timezone.now()
            posts_last_10 = Post.objects.filter(
                author=request.user,
                created_at__gte=now - timedelta(minutes=10)).count()

            if posts_last_10 >= 5:
                messages.error(request, "You're posting too fast. Please wait 1 hour before creating another post.")
                return redirect("home")
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            messages.success(request, "Post created.")
            return redirect("home")
    else:
        form = PostForm()

    return render(request, "posts/create_post.html", {"form": form})


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.order_by("created_at")

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            now = timezone.now()
            replies_last_5 = Comment.objects.filter(
                author=request.user,
                created_at__gte=now - timedelta(minutes=5)).count()

            if replies_last_5 >= 15:
                messages.error(request, "You're replying too fast. Please wait 15 minutes before replying again.")
                return redirect("post_detail", post_id=post.id)

            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            messages.success(request, "Reply posted.")
            return redirect("post_detail", post_id=post.id)
    else:
        form = CommentForm()

    return render(request, "posts/post_detail.html", {
        "post": post,
        "comments": comments,
        "form": form,
    })


@login_required
def report_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.reported = True
    post.save(update_fields=["reported"])
    messages.success(request, "Post reported. Thank you.")
    return redirect("post_detail", post_id=post.id)


@login_required
def report_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.reported = True
    comment.save(update_fields=["reported"])
    messages.success(request, "Reply reported. Thank you.")
    return redirect("post_detail", post_id=comment.post.id)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        messages.error(request, "You can only delete your own posts.")
        return redirect("post_detail", post_id=post.id)

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted.")
        return redirect("home")

    return render(request, "posts/confirm_delete_post.html", {"post": post})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author != request.user:
        messages.error(request, "You can only delete your own replies.")
        return redirect("post_detail", post_id=comment.post.id)

    if request.method == "POST":
        post_id = comment.post.id
        comment.delete()
        messages.success(request, "Reply deleted.")
        return redirect("post_detail", post_id=post_id)

    return render(request, "posts/confirm_delete_comment.html", {"comment": comment})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        messages.error(request, "You can only edit your own posts.")
        return redirect("post_detail", post_id=post.id)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated.")
            return redirect("post_detail", post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, "posts/edit_post.html", {"form": form, "post": post})

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author != request.user:
        messages.error(request, "You can only edit your own replies.")
        return redirect("post_detail", post_id=comment.post.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Reply updated.")
            return redirect("post_detail", post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, "posts/edit_comment.html", {"form": form, "comment": comment})


@staff_member_required
def moderation_dashboard(request):
    reported_posts = Post.objects.filter(reported=True).order_by("-created_at")
    reported_comments = Comment.objects.filter(reported=True).order_by("-created_at")
    return render(request, "posts/moderation_dashboard.html", {
        "reported_posts": reported_posts,
        "reported_comments": reported_comments,
    })


@staff_member_required
def unreport_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.reported = False
    post.save(update_fields=["reported"])
    messages.success(request, "Post unreported.")
    return redirect("moderation_dashboard")


@staff_member_required
def unreport_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.reported = False
    comment.save(update_fields=["reported"])
    messages.success(request, "Reply unreported.")
    return redirect("moderation_dashboard")