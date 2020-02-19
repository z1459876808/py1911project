from django.db import models


# Create your models here.


class Ads(models.Model):
    img = models.ImageField(upload_to='ads', verbose_name='图片')
    desc = models.CharField(max_length=20, null=True, blank=True, verbose_name='轮播图')


class Category(models.Model):
    name = models.CharField(max_length=20, verbose_name='分类名')


class Tag(models.Model):
    name = models.CharField(max_length=20, verbose_name='标签名')


class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name='文章标题')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    author = models.CharField(max_length=20, verbose_name='作者')
    views = models.CharField(default=0, verbose_name='浏览量')
    body = models.TextField(verbose_name='正文')
    tags = models.ManyToManyField(Tag, verbose_name='标签')


class Comment(models.Model):
    name = models.CharField(max_length=20, verbose_name='评论人')
    url = models.URLField(default='http://www.zcx.com', verbose_name='个人主页')
    email = models.EmailField(default='1459876808@qq.com', verbose_name='个人邮箱')
    body = models.CharField(max_length=500, verbose_name='评论内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='所属文章')
