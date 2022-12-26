from django.urls import path
from users.views import RegisterUser

urlpatterns = [
    # path('login/', login, name='login'),
    path('reg/', RegisterUser.as_view(), name='reg'),

]