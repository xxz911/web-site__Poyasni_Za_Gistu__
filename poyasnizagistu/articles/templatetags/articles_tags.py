from django import template
from django.db.models import Count
from articles.models import Thematic
from django.core.cache import cache

register = template.Library()


@register.inclusion_tag('articles/list_thematics.html', name='showthematics')
def show_organ_system_and_album(thematic_selected=0):
    thematic = cache.get('thematic')
    if not thematic:
        thematic = Thematic.objects.annotate(Count('article')).filter(article__is_published=True)
        cache.set('thematic', thematic, 60)
    return {'thematic': thematic, 'thematic_selected': thematic_selected}
