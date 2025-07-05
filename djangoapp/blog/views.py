from typing import Any
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from blog.models import Page, Post
from django.contrib.auth.models import User
from django.views.generic import ListView

PER_PAGE = 9


class PostListView(ListView):
    model = Post
    template_name = "blog/pages/index.html"
    context_object_name = "posts"
    ordering = ("-pk",)
    paginate_by = PER_PAGE
    queryset = Post.object.get_published()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context.update(
            {
                "page_title": "Home - ",
            }
        )

        return context


# def index(request):
#     posts = Post.object.get_published()

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         "blog/pages/index.html",
#         {
#             "page_obj": page_obj,
#             "page_title": "Home - ",
#         },
#     )


def created_by(request, author_id):
    posts = Post.object.get_published().filter(created_by__pk=author_id)
    user = User.objects.filter(pk=author_id).first()

    if user is None:
        raise Http404

    user_full_name = user.username
    if user.first_name:
        user_full_name = f"{user.first_name} {user.last_name}"

    page_title = f"Posts de {user_full_name}"

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "blog/pages/index.html",
        {
            "page_obj": page_obj,
            "page_title": page_title,
        },
    )


def category(request, slug):
    posts = Post.object.get_published().filter(category__slug=slug)

    if len(posts) == 0:
        raise Http404

    page_title = f"{posts[0].category.name} - "

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "blog/pages/index.html",
        {
            "page_obj": page_obj,
            "page_title": page_title,
        },
    )


def tag(request, slug):
    posts = Post.object.get_published().filter(tag__slug=slug)

    if len(posts) == 0:
        raise Http404

    page_title = f"{posts[0].tag.first().name} - "

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "blog/pages/index.html",
        {
            "page_obj": page_obj,
            "page_title": page_title,
        },
    )


def search(request):
    search_value = request.GET.get("search", "").strip()
    posts = Post.object.get_published().filter(
        Q(title__icontains=search_value)
        | Q(excerpt__icontains=search_value)
        | Q(content__icontains=search_value)
    )[:PER_PAGE]

    page_title = f"{search_value[:30]} - "

    return render(
        request,
        "blog/pages/index.html",
        {
            "page_obj": posts,
            "search_value": search_value,
            "page_title": page_title,
        },
    )


def page(request, slug):
    page_obj = Page.objects.filter(is_published=True).filter(slug=slug).first()

    if page_obj is None:
        raise Http404

    page_title = f"{page_obj.title} - "

    return render(
        request,
        "blog/pages/page.html",
        {
            "page": page_obj,
            "page_title": page_title,
        },
    )


def post(request, slug):
    post_obj = Post.object.get_published().filter(slug=slug).first()

    if post_obj is None:
        raise Http404

    page_title = f"{post_obj.title} - "

    return render(
        request,
        "blog/pages/post.html",
        {
            "post": post_obj,
            "page_title": page_title,
        },
    )
