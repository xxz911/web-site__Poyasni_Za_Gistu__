from django.urls import path
from .views import *

urlpatterns = [
    path('', blog, name='blog'),
    path('post/<int:post_id>/', show_post, name='post'),
    path('category/<int:cat_id>/', show_category, name='category')
]