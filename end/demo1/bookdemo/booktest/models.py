from django.db import models


# Create your models here.

# MVT   M数据模型

# ORM   M数据模型

# 在此处编写应用的数据模型类


# 每一张表就是一个模型类
# 有了 ORM之后我们就可以定义出表对应的模型类
# 通过操作模型类去操作数据库  不需要写sq语句


# 有了模型类之后模型类如何与数据库交互
# 1注册模型在setting.py 中的INSTALLED_ APPS 添加应用名
# 2生成迁移文件用于与数据库交互python manage.py makemigrations 会在对应的应用下方生成迁移文件
# 3执行迁移会在对应的数据库中生成对应的表python manage.py migrate
# 模型类更改之后需要再次生成迁移文件 执行迁移


class Book(models.Model):
    """
    Book继承了Model类 因为Model类拥有操作数据库的功能
    """
    #       models.CharField是一个字符串(max_length最大长度是20)
    title = models.CharField(max_length=20)
    #          models.DateField更新时间(default数据库默认时间是""1998-04-10)
    pub_date = models.DateField(default="1998-04-10")
    price = models.FloatField(default=0)

    def __str__(self):
        return self.title


class Hero(models.Model):
    """
    Hero继承了Model 也可以操作数据库
    """
    name = models.CharField(max_length=20)
    #       models.CharField是一个字符串(max_length最大长度是5,choices选项以元组的形式存放
    #       有多少个选项就写多少个元组  default数据库默认的选项male男)
    gender = models.CharField(max_length=6, choices=(("male", "男"), ("female", "女")), default="male")

    content = models.CharField(max_length=100)

    #      models.ForeignKey定义一个外键( )
    # book 是一对多中的外键 on_delete代表删除主表数据如何做
    # models.CASCADE 级联删除
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='heros')

    def __str__(self):
        return self.name


class UserManger(models.Manager):
    """
    自定义模型管理类  该模型不具有 objects对象
    """

    def deleteByTelephone(self, tele):
        # django默认的 objects是Manager类型  *.objects.get()
        user = self.get(telephone=tele)
        user.delete()

    def createUser(self, tele):
        # self.model()可以获取模型类构造函数
        user = self.model()
        user.telephone = tele
        user.save()


class User(models.Model):
    telephone = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号码')
    # 自定义过管理字段后b不再有objects  自定义一个
    objects = UserManger()

    def __str__(self):
        return self.telephone

    class Meta:
        # 表明
        db_table = "用户类"
        ordering = ['id']
        # admin页面进入模型类显示名字
        verbose_name = '用户模型类'
        # admin页面在应用下方显示得模型名
        verbose_name_plural = '用户模型类'

# 一对多 一方Book 实例 b 多方 Hero 实例 h
# 一找多  b.hero_set.all()  如果定义过 related_name = 'heros'   b.heros.all()


class Account(models.Model):
    username = models.CharField(max_length=20,verbose_name='用户名')
    password = models.CharField(max_length=16,verbose_name='密码')
    regist_name = models.DateField(auto_now_add=True,verbose_name='注册日期')


class Concat(models.Model):
    telephone = models.CharField(max_length=11,verbose_name='手机号')
    email = models.EmailField(default='1459876808@qq.com')
    account = models.OneToOneField(Account,on_delete=models.CASCADE,related_name='con')

# 一对一  一方 Account 实例：a  一方 Concat 实例：c  关系字段定义在任意一方
# a找c  a.concat
# c找a  c.account


class Article(models.Model):
    title = models.CharField(max_length=20,verbose_name='标题')
    sumary = models.TextField(verbose_name='正文')

class Tag(models.Model):
    name = models.CharField(max_length=10,verbose_name='标签名')
    article = models.ManyToManyField(Article,related_name='tags')

# 多对多  多方Article
# 实例 a
# 多方Tag    实例t
# 关系字段可以定义在任意一方
# 添加关系t. articles . add(a)
# 移除关系t. orticles. remove(a)