from django.template import Library
from ..models import Article, Category, Tag

register = Library()


@register.filter
def dateFormat(data):
    return '%d-%d-%d' % (data.year, data.month, data.day)


@register.filter
def authorFormat(author, info):
    return info + ':' + author.upper()


@register.simple_tag
def get_latestarticles(num=3):
    return Article.objects.all().order_by('-create_time')[:num]


@register.simple_tag
def get_latesdates(num=3):
    dates = Article.objects.dates('create_time', 'month', 'DESC')[:num]
    return dates


@register.simple_tag
def get_category():
    return Category.objects.all().order_by('-id')

@register.simple_tag
def get_tags():
    return Tag.objects.all().order_by('-id')
