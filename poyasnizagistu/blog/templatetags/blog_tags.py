from django import template
from django.db.models import Count

from blog.models import *

register = template.Library()


@register.inclusion_tag('blog/list_categories.html', name='showcats')
def show_categories_and_post(cat_selected=0):
    cats = CategoryPost.objects.annotate(Count('post')).filter(post__is_published=True)
    return {'cats': cats, 'cat_selected': cat_selected}

