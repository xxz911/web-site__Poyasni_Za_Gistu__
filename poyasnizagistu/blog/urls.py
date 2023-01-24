from django.urls import path
from .views import *

urlpatterns = [
    path('', BlogPosts.as_view(), name='blog'),
    path('post/<slug:post_slug>/', ShowBlogPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', ShowBlogCategory.as_view(), name='category')
]