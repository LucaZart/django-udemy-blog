from django.urls import path
from blog.views import view_test

app_name = 'blog'
urlpatterns = [
    path('', view_test, name='view_test'),
]
