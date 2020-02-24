# 使用Django框架中集成的RSS包装工具
from django.contrib.syndication.views import Feed
from django.shortcuts import reverse
from .models import Article


class ArticleFeed(Feed):
    title = 'web全栈开发技术'
    description = '定期发布一系列wen全栈开发技术'
    link = '/'

    def items(self):
        return Article.objects.all().order_by('create_time')[:2]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.author

    def item_link(self, item):
        url = reverse('blogapp:detail', args=(item.id,))
        return url
