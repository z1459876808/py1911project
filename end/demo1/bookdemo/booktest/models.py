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
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
