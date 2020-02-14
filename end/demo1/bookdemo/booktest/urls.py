# 引入路由绑定函数
from django.conf.urls import url
from . import views

app_name = 'booktest'
# 每一个路由文件中必须编写一个路由数组
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^detail/(\d+)', views.detail, name='detail'),

    url(r'^deletebook/(\d+)/$', views.deletebook, name='deletebook'),
    url(r'^deletehero/(\d+)/$', views.deletehero, name='deletehero'),
    url(r'^addbook/$', views.addbook, name='addbook'),
    url(r'^editbook/(\d+)/$',views.editbook,name='editbook'),
    url(r'^addhero/(\d+)/$', views.addhero, name='addhero'),
    url(r'^edithero/(\d+)/$', views.edithero, name='edithero')
]
