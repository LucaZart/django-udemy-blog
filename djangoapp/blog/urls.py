from django.urls import path
from blog.views import category, created_by, page, post, search, tag
from blog.views import PostListView

app_name = "blog"
urlpatterns = [
    # path("", index, name="index"),
    path("", PostListView.as_view(), name="index"),
    path("page/<slug:slug>/", page, name="page"),
    path("post/<slug:slug>/", post, name="post"),
    path("post/<slug:slug>/", post, name="post"),
    path("created_by/<int:author_id>/", created_by, name="created_by"),
    path("category/<slug:slug>/", category, name="category"),
    path("tag/<slug:slug>/", tag, name="tag"),
    path("search/", search, name="search"),
]
