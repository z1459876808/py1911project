# 引入路由绑定函数
from django.conf.urls import url
from . import views

# 每一个路由文件中必须编写一个路由数组
urlpatterns = [
    url(r'^index/$', views.index),
    url(r'^about/$', views.about),
    url(r'^detail/(\d+)', views.detail)
]
