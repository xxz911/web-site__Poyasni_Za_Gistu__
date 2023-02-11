from django.urls import path
from .views import *


urlpatterns = [
    path('', AlbumList.as_view(), name='albums'),
    path('album/<slug:album_slug>/', AlbumDetail.as_view(), name='album'),
    path('thumbs_album/', thumbsalbum, name='thumbs_album'),
    path('organ_system/<slug:organ_slug>/', ShowOrganSystem.as_view(), name='organ'),


]