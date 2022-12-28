from django.urls import path, include
from users.views import RegisterUser

urlpatterns = [
    # path('login/', login, name='login'),
    path('captcha/', include('captcha.urls')),
    path('reg/', RegisterUser.as_view(), name='reg'),

]