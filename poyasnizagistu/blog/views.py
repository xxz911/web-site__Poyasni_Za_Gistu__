from django.http import HttpResponse
from django.shortcuts import render


menu = ['Блог', 'Статьи', 'Альбомы', 'Платное', 'О сайте']


def home(request):
    return render(request, 'blog/home.html', {'menu': menu})