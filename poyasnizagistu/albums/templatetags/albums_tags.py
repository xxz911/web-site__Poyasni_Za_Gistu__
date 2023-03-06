from django import template
from django.db.models import Count
from django.core.cache import cache

from albums.models import *

register = template.Library()

# Пользовательский тег для выборки систем органов и подключению в шаблон
@register.inclusion_tag('albums/list_organ_system.html', name='showorgan')
def show_organ_system_and_album(organ_selected=0):
    # Если в кеше, берем из него, иначе делаем запрос к БД
    organ = cache.get('organ')
    if not organ:
        organ = Organ_System.objects.annotate(Count('album')).filter(album__is_published=True)
        cache.set('organ', organ, 60)
    return {'organ': organ, 'organ_selected': organ_selected}
