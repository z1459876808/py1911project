from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Ads)
admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Tag)
