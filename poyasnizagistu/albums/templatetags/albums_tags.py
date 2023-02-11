from django import template
from django.db.models import Count

from albums.models import *

register = template.Library()


@register.inclusion_tag('albums/list_organ_system.html', name='showorgan')
def show_organ_system_and_album(organ_selected=0):
    organ = Organ_System.objects.annotate(Count('album')).filter(album__is_published=True)
    return {'organ': organ, 'organ_selected': organ_selected}
