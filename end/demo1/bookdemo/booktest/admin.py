from django.contrib import admin

# Register your models here.


# 注册自己需要管理的模型 Book Hero
from .models import Book,Hero
admin.site.register(Book)
admin.site.register(Hero)