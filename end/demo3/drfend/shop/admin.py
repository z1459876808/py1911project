from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Good)
admin.site.register(Goodimg)
admin.site.register(User)
admin.site.register(Order)

