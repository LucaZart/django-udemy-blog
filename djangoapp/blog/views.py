from typing import Any
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect
from blog.models import Page, Post
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView

PER_PAGE = 9


class PostListView(ListView):
    template_name = "blog/pages/index.html"
    context_object_name = "posts"
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


class CreatedByListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context: dict[str, Any] = {}

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        author_id = self.kwargs.get("author_id")
        user = User.objects.filter(pk=author_id).first()

        if user is None:
            raise Http404()

        self._temp_context = {
            "author_id": author_id,
            "user": user,
        }

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self._temp_context["user"]

        user_full_name = user.username
        if user.first_name:
            user_full_name = f"{user.first_name}"

        page_title = f"Posts de {user_full_name}"

        context.update(
            {
                "page_title": page_title,
            }
        )

        return context

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(created_by__pk=self._temp_context["user"].pk)
        return qs


class CategoryListView(PostListView):
    allow_empty = False

    def get_queryset(self):
        return super().get_queryset().filter(category__slug=self.kwargs.get("slug"))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page_title = f"{self.object_list[0].category.name} - "  # type: ignore

        context.update(
            {
                "page_title": page_title,
            }
        )
        return context


class TagListView(PostListView):
    allow_empty = False

    def get_queryset(self):
        return super().get_queryset().filter(tag__slug=self.kwargs.get("slug"))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page_title = f"{self.object_list[0].tag.first().name} - "  # type: ignore

        context.update(
            {
                "page_title": page_title,
            }
        )
        return context


class SearchListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._search_value: str = ""

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self._search_value = request.GET.get("search", "").strip()
        return super().setup(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        search_value = self._search_value

        qs = (
            super()
            .get_queryset()
            .filter(
                Q(title__icontains=search_value)
                | Q(excerpt__icontains=search_value)
                | Q(content__icontains=search_value)
            )[:PER_PAGE]
        )
        return qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        search_value = self._search_value

        context.update(
            {
                "page_title": f"{search_value[:30]} - ",
                "search_value": search_value,
            }
        )

        return context

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if self._search_value == "":
            return redirect("blog:index")
        return super().get(request, *args, **kwargs)


class PageDetailView(DetailView):
    model = Page
    template_name = "blog/pages/page.html"
    slug_field = "slug"
    context_object_name = "page"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page = self.get_object()
        page_title = f"{page.title} - "  # type:ignore
        context.update(
            {
                "page_title": page_title,
            }
        )
        return context

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_published=True)


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/pages/post.html"
    slug_field = "slug"
    context_object_name = "post"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page = self.get_object()
        page_title = f"{page.title} - "  # type:ignore
        context.update(
            {
                "page_title": page_title,
            }
        )
        return context

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_published=True)
