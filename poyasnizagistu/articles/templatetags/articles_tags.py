from django import template
from django.db.models import Count


from articles.models import Thematic

register = template.Library()


@register.inclusion_tag('articles/list_thematics.html', name='showthematics')
def show_organ_system_and_album(thematic_selected=0):
    thematic = Thematic.objects.annotate(Count('article')).filter(article__is_published=True)
    return {'thematic': thematic, 'thematic_selected': thematic_selected}
