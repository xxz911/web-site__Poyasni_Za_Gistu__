from django.urls import path, include
from users.views import RegisterUser, AccauntUser, profile
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('captcha/', include('captcha.urls')),
    path('registration/', RegisterUser.as_view(), name='register'),
    path('profile/<slug:user_slug>/', profile, name='profile'),
    path('profile_change/', AccauntUser.as_view(), name='profile_change'),


    path('password_reset/', auth_views.PasswordResetView.as_view(
        html_email_template_name='registration/password_reset_emaill.html',

)),
    path('', include('django.contrib.auth.urls'))


]

