from django.urls import path
from .views import *


urlpatterns = [
    path('', PostList.as_view(), name='blog'),
    path('post/<slug:post_slug>/', PostDetail.as_view(), name='post'),
    path('thumbs/', thumbs, name='thumbs_post'),
    path('category/<slug:cat_slug>/', ShowCategory.as_view(), name='category'),
    path('search_posts/', SearchPosts.as_view(), name='search_posts'),


]