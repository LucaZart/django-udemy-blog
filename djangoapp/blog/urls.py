from django.urls import path
from blog.views import page, post, search
from blog.views import PostListView, CreatedByListView, CategoryListView, TagListView

app_name = "blog"
urlpatterns = [
    # path("", index, name="index"),
    path("", PostListView.as_view(), name="index"),
    path("page/<slug:slug>/", page, name="page"),
    path("post/<slug:slug>/", post, name="post"),
    path("created_by/<int:author_id>/", CreatedByListView.as_view(), name="created_by"),
    path("category/<slug:slug>/", CategoryListView.as_view(), name="category"),
    path("tag/<slug:slug>/", TagListView.as_view(), name="tag"),
    path("search/", search, name="search"),
]
