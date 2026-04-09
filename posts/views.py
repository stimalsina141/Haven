from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Post
from .forms import PostForm

# Create your views here.
# from django.http import HttpResponse

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
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("home")
    else:
        form = PostForm()
    
    return render(request, "posts/create_post.html", {"form": form})
    
