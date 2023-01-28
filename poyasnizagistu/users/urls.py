from django.urls import path, include
from users.views import RegisterUser, AccauntUser, profile


urlpatterns = [

    path('captcha/', include('captcha.urls')),
    path('registration/', RegisterUser.as_view(), name='register'),
    path('profile/<slug:user_slug>/', profile, name='profile'),
    path('profile_change/', AccauntUser.as_view(), name='profile_change'),


]

urlpatterns += [
    path('', include('django.contrib.auth.urls')),
]