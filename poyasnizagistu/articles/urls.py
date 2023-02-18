from django.urls import path
from .views import *


urlpatterns = [
    path('', ArticlesList.as_view(), name='articles'),
    path('article/<slug:article_slug>/', ArticleDetail.as_view(), name='article'),
    path('thumbs_article/', thumbsarticle, name='thumbs_article'),
    path('thematic/<slug:thematic_slug>/', ShowThematic.as_view(), name='thematic'),


]