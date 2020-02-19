from django.contrib import admin

# Register your models here.
from .models import *

class ChoiceInline(admin.StackedInline):
    # 关联的模型类
    model = Choices
    # 关联个数
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    # list_display = [""]
    inlines = [ChoiceInline]

class ChoiceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Question,QuestionAdmin)
admin.site.register(Choices,ChoiceAdmin)

admin.site.register(User)

"""
admin 给后台管理使用
admin.site.register(Question)   # 管理员可以看到模型类
class ChoiceAdmin(admin.ModelAdmin):  #可以自定义Choice的管理页面
"""