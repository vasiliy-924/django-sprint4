from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .constants import POSTS_LIMIT
from .forms import CommentForm, PostForm, UserEditForm
from .models import Category, Comment, Post
from .services import get_paginated_page


def index(request):
    post_list = Post.objects.filter_posts_by_publication(
    ).annotate_comment_count().order_by('-pub_date')
    page_obj = get_paginated_page(request, post_list, POSTS_LIMIT)
    return render(request, "blog/index.html", {"page_obj": page_obj})


def post_detail(request, post_id):
    base_qs = Post.objects.select_related("author", "category", "location")
    post = get_object_or_404(base_qs, pk=post_id)
    is_public = (
        post.is_published
        and post.category is not None
        and post.category.is_published
        and post.pub_date <= timezone.now()
    )
    if not is_public and not (
        request.user == post.author or request.user.is_staff
    ):
        raise Http404

    form = CommentForm()
    comments = get_paginated_page(request, post.comments.all(), per_page=10)
    return render(
        request,
        "blog/detail.html",
        {"post": post, "form": form, "page_obj": comments},
    )


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category.objects.filter(is_published=True),
        slug=category_slug
    )
    posts_list = category.posts.filter_posts_by_publication(
    ).annotate_comment_count().order_by('-pub_date')
    page_obj = get_paginated_page(request, posts_list, POSTS_LIMIT)
    return render(
        request,
        "blog/category.html",
        {"category": category, "page_obj": page_obj},
    )


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts_list = author.posts.all().annotate_comment_count().order_by('-pub_date')

    if not (request.user == author or request.user.is_staff):
        posts_list = posts_list.filter_posts_by_publication()

    page_obj = get_paginated_page(request, posts_list, POSTS_LIMIT)
    return render(
        request, "blog/profile.html", {"profile": author, "page_obj": page_obj}
    )


@login_required
def edit_profile(request):
    form = UserEditForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect("blog:profile", username=request.user.username)
    return render(request, "blog/user.html", {"form": form})


@login_required
def create_post(request):
    form = PostForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("blog:profile", username=request.user.username)
    return render(request, "blog/create.html", {"form": form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect("blog:post_detail", post_id=post.id)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect("blog:post_detail", post_id=post.id)
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
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    return redirect("blog:post_detail", post_id=post.id)


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, author=request.user)
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect("blog:post_detail", post_id=post_id)
    return render(
        request, "blog/comment.html", {"form": form, "comment": comment}
    )


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, author=request.user)
    if request.method == "POST":
        comment.delete()
        return redirect("blog:post_detail", post_id=post_id)
    return render(request, "blog/comment.html", {"comment": comment})
