from django.db import models
# 导入富文本字段
from DjangoUeditor.models import UEditorField

# Create your models here.


class Ads(models.Model):
    """
    使用图片字段 需要安装 pip install pillowwwwwwww
    轮播图
    """
    img = models.ImageField(upload_to="ads", verbose_name="图片")
    desc = models.CharField(max_length=20, null=True, blank=True, verbose_name="图片描述")

    def __str__(self):
        return self.desc


class Category(models.Model):
    """
    分类页
    """
    name = models.CharField(max_length=20, verbose_name="分类名")

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    标签类
    """
    name = models.CharField(max_length=20, verbose_name="标签名")


class Article(models.Model):
    """
    文章类
    """
    title = models.CharField(max_length=50, verbose_name="文章标题")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="分类")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    author = models.CharField(max_length=20, verbose_name="作者")
    views = models.PositiveIntegerField(default=0, verbose_name="浏览量")
    # body = models.TextField(verbose_name="正文")
    # 使用百度Ueditor 富文本字段类型
    body = UEditorField(imagePath='imgs/',width="100%")
    tags = models.ManyToManyField(Tag)


class Comment(models.Model):
    """
    评论表
    """
    name = models.CharField(max_length=20, verbose_name="评论人")
    url = models.URLField(default="http://www.hsh.com", verbose_name="个人主页")
    email = models.EmailField(default="1287807280@qq.com", verbose_name="个人邮箱")
    body = models.CharField(max_length=500, verbose_name="评论内容")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="所属文章")
