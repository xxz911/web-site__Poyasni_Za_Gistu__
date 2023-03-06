from django import template
from django.db.models import Count
from django.core.cache import cache

from articles.models import Thematic

register = template.Library()

# Пользовательский тег для выборки тематик и подключению в шаблон
@register.inclusion_tag('articles/list_thematics.html', name='showthematics')
def show_organ_system_and_album(thematic_selected=0):
    # Если в кеше, берем из него, иначе делаем запрос к БД
    thematic = cache.get('thematic')
    if not thematic:
        thematic = Thematic.objects.annotate(Count('article')).filter(article__is_published=True)
        cache.set('thematic', thematic, 60)
    return {'thematic': thematic, 'thematic_selected': thematic_selected}
