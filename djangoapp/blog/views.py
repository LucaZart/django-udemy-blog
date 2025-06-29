from django.core.paginator import Paginator
from django.shortcuts import render
from blog.models import Post

PER_PAGE = 9


def index(request):
    posts = Post.object.get_published()

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "blog/pages/index.html",
        {
            "page_obj": page_obj,
        },
    )


def created_by(request, author_id):
    posts = Post.object.get_published().filter(created_by__pk=author_id)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "blog/pages/index.html",
        {
            "page_obj": page_obj,
        },
    )


def category(request, slug):
    posts = Post.object.get_published().filter(category__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "blog/pages/index.html",
        {
            "page_obj": page_obj,
        },
    )


def tag(request, slug):
    posts = Post.object.get_published().filter(tag__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "blog/pages/index.html",
        {
            "page_obj": page_obj,
        },
    )


def page(request, slug):
    # paginator = Paginator(posts, 9)
    # page_number = request.GET.get("page")
    # page_obj = paginator.get_page(page_number)

    return render(
        request,
        "blog/pages/page.html",
        {
            # 'page_obj': page_obj,
        },
    )


def post(request, slug):
    post = Post.object.get_published().filter(slug=slug).first()

    return render(
        request,
        "blog/pages/post.html",
        {
            "post": post,
        },
    )
