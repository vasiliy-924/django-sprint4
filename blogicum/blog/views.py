from blog.forms import UserEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now

from .constants import POSTS_LIMIT
from .forms import CommentForm, PostForm
from .models import Category, Comment, Post
from .querysets import filter_posts_by_publication


def index(request):
    post_list = filter_posts_by_publication(Post.objects.all())
    post_list = post_list.annotate(comment_count=Count("comments")).order_by(
        "-pub_date"
    )
    paginator = Paginator(post_list, POSTS_LIMIT)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "blog/index.html", {"page_obj": page_obj})


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.select_related("author", "category", "location").annotate(
            comment_count=Count("comments")
        ),
        pk=post_id,
    )
    is_public = (
        post.is_published
        and post.category.is_published
        and post.pub_date <= now()
    )
    if not is_public and not (
        request.user == post.author or request.user.is_staff
    ):
        raise Http404
    form = CommentForm()
    comments = post.comments.select_related("author").order_by("created_at")
    return render(
        request,
        "blog/detail.html",
        {"post": post, "form": form, "comments": comments},
    )


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category.objects.filter(is_published=True), slug=category_slug
    )
    posts_list = filter_posts_by_publication(category.posts.all())
    posts_list = posts_list.annotate(comment_count=Count("comments")).order_by(
        "-pub_date"
    )
    paginator = Paginator(posts_list, POSTS_LIMIT)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "blog/category.html",
        {"category": category, "page_obj": page_obj},
    )


def profile(request, username):
    user = get_object_or_404(User, username=username)
    post_list = (
        user.posts.all()
        .annotate(comment_count=Count("comments"))
        .order_by("-pub_date")
    )
    paginator = Paginator(post_list, POSTS_LIMIT)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request, "blog/profile.html", {"profile": user, "page_obj": page_obj}
    )


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("blog:profile", username=request.user.username)
    else:
        form = UserEditForm(instance=request.user)
    return render(request, "blog/user.html", {"form": form})


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("blog:profile", username=request.user.username)
    else:
        form = PostForm()
    return render(request, "blog/create.html", {"form": form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect("blog:post_detail", post_id=post.id)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("blog:post_detail", post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, "blog/create.html", {"form": form})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect("blog:post_detail", post_id=post.id)
    if request.method == "POST":
        post.delete()
        return redirect("blog:profile", username=request.user.username)
    form = PostForm(instance=post)
    return render(request, "blog/create.html", {"form": form})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect("blog:post_detail", post_id=post.id)


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, author=request.user)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("blog:post_detail", post_id=post_id)
    else:
        form = CommentForm(instance=comment)
    return render(
        request, "blog/comment.html", {"form": form, "comment": comment}
    )


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, author=request.user)
    if request.method == "POST":
        comment.delete()
        return redirect("blog:post_detail", post_id=post_id)
    # GET: рендерим тот же шаблон comment.html, он по URL покажет подтверждение
    return render(request, "blog/comment.html", {"comment": comment})
