from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from django.utils.safestring import mark_safe
from blog.models import Category, Page, Post, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
    )
    list_display_links = ("name",)
    search_fields = (
        "id",
        "name",
        "slug",
    )
    list_per_page = 10
    ordering = ("-id",)
    prepopulated_fields = {
        "slug": ("name",),
    }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
    )
    list_display_links = ("name",)
    search_fields = (
        "id",
        "name",
        "slug",
    )
    list_per_page = 10
    ordering = ("-id",)
    prepopulated_fields = {
        "slug": ("name",),
    }


@admin.register(Page)
class PageAdmin(SummernoteModelAdmin):
    summernote_fields = ("content",)
    list_display = (
        "id",
        "title",
        "is_published",
    )
    list_display_links = ("title",)
    search_fields = (
        "id",
        "slug",
        "title",
        "content",
    )
    list_per_page = 10
    ordering = ("-id",)
    prepopulated_fields = {
        "slug": ("title",),
    }


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ("content",)
    list_display = (
        "id",
        "title",
        "is_published",
        "created_by",
    )
    list_display_links = ("title",)
    search_fields = (
        "id",
        "slug",
        "title",
        "excerpt",
        "content",
    )
    list_per_page = 50
    list_filter = (
        "category",
        "is_published",
    )
    list_editable = ("is_published",)
    ordering = ("-id",)
    readonly_fields = (
        "created_at",
        "updated_at",
        "updated_by",
        "created_by",
        "link",
    )
    prepopulated_fields = {
        "slug": ("title",),
    }
    autocomplete_fields = "tag", "category"

    def link(self, obj):
        if not obj.pk:
            return "-"

        url_post = obj.get_absolute_url()
        link_post = mark_safe(f'<a target="_blank" href="{url_post}">Ver Post</a>')
        return link_post

    def save_model(self, request, obj, form, change):
        print(f"{request.user=} - {change=}")

        if change:
            obj.updated_by = request.user
        else:
            obj.updated_by = request.user
            obj.created_by = request.user

        obj.save()
