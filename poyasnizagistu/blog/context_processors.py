menu = [{'title': "Блог", 'url_name': 'blog'},
{'title': "Статьи", 'url_name': 'articles'},
{'title': "Альбомы", 'url_name': 'albums'},
{'title': "Платное", 'url_name': 'home'},
{'title': "О сайте", 'url_name': 'home'},
]

def menu_context_processor(request):

    return {'menu': menu}