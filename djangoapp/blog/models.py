from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from utils.rands import slugfy_new
from utils.images import resize_image
from django_summernote.models import AbstractAttachment


class PostAttachment(AbstractAttachment):
    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.file.name

        current_file_name = str(self.file.name)
        super_save = super().save(*args, **kwargs)

        file_changed = False
        if self.file:
            file_changed = current_file_name != self.file.name

        if file_changed:
            resize_image(self.file, 900)

        return super_save


class Tag(models.Model):
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True, default=None, null=True, blank=True, max_length=255
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugfy_new(self.name)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True, default=None, null=True, blank=True, max_length=255
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugfy_new(self.name)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Page(models.Model):
    class Meta:
        verbose_name = "Page"
        verbose_name_plural = "Pages"

    title = models.CharField(max_length=65)
    slug = models.SlugField(
        unique=True, default="", null=False, blank=True, max_length=255
    )
    is_published = models.BooleanField(
        default=False,
        help_text=(
            "Este campo deverá estar marcado se "
            "quer que a publicação apareça na tela principal."
        ),
    )
    content = models.TextField()

    def get_absolute_url(self):
        if not self.is_published:
            return reverse("blog:index")
        return reverse("blog:page", args=(self.slug,))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugfy_new(self.title)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class PostManager(models.Manager):
    def get_published(self):
        return self.filter(is_published=True).order_by("-pk")


class Post(models.Model):
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    object = PostManager()

    title = models.CharField(max_length=65)
    slug = models.SlugField(
        unique=True, default="", null=False, blank=True, max_length=255
    )
    excerpt = models.CharField(max_length=255)
    is_published = models.BooleanField(
        default=False,
        help_text=(
            "Este campo deverá estar marcado se "
            "quer que a publicação apareça na tela principal."
        ),
    )
    content = models.TextField()
    cover = models.ImageField(upload_to="posts/%Y/%m/", blank=True, default="")
    cover_in_post_content = models.BooleanField(
        default=True, help_text="Exibir está imagem de capa dentro da página do post?"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="page_created_by",
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="page_updated_by",
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    tag = models.ManyToManyField(Tag, blank=True, default="")

    def get_absolute_url(self):
        if not self.is_published:
            return reverse("blog:index")
        return reverse("blog:post", args=(self.slug,))

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugfy_new(self.title)

        current_cover_name = str(self.cover.name)
        super_save = super().save()

        cover_changed = False
        if self.cover:
            cover_changed = current_cover_name != self.cover.name

        if cover_changed:
            resize_image(self.cover, 900)

        return super_save
