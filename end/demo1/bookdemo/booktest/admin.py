from django.contrib import admin

from django.contrib.admin import ModelAdmin

# Register your models here.


# 注册自己需要管理的模型 Book Hero
from .models import Book, Hero, User


class HeroInline(admin.StackedInline):
    model = Hero
    extra = 1


class HeroAdmin(ModelAdmin):
    list_display = ('name', 'gender', 'content', 'book')

    search_fields = ('name', 'gender')


admin.site.register(Hero, HeroAdmin)


class BookAdmin(ModelAdmin):
    list_display = ('title', 'price', 'pub_date')

    search_fields = ('title', 'price')

    inlines = [HeroInline]


admin.site.register(Book, BookAdmin)

admin.site.register(User)
