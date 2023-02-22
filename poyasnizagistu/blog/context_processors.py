menu = [
{'title': "Блог", 'url_name': 'blog'},
{'title': "Статьи", 'url_name': 'articles'},
{'title': "Альбомы", 'url_name': 'albums'},
{'title': "О сайте", 'url_name': 'about'},
]
home = {'title': "Главная", 'url_name': 'home'}
def menu_context_processor(request):

    return {'menu': menu, 'home': home}