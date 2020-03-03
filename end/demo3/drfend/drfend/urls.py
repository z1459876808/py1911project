"""drfend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from shop.views import *

from django.views.static import serve
from django.conf.urls import url
from .settings import MEDIA_ROOT

# 引入API文档路由
from rest_framework.documentation import include_docs_urls

# 引入DRF自带的路由类
from rest_framework import routers

# 通过router 默认路由注册资源
router = routers.DefaultRouter()
router.register('categorys', CategoryViewsets)
router.register('goods', GoodViewsets)
router.register('goodsimg', GoodImgsViewsets)
router.register('user', UserViewsets)
router.register('orders', OredrViewsets)

urlpatterns = [
    path('admin/', admin.site.urls),
    # 配置RestFulAPI
    path('api/v1/', include(router.urls)),
    # API文档地址
    path('api/v1/docs/', include_docs_urls(title='RestFuAPI', description='RestFuAPI v1')),

    # 为了在DRF路由调试界面能够使用用户相关功能需要引入以下路由
    path('', include('rest_framework.urls')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    # url(r'^categorylist/$', categorylist, name='categorylist'),
    # url(r'^categorydetail/(\d+)/$', categorydetail, name='categorydetail')

    # url(r'^categorylist/$', CategoryListView.as_view(), name='categorylist'),
    # url(r'^categorydetail/(?P<pk>\d+)/$', CategoryDietailView.as_view(), name='categorydetail')

]
