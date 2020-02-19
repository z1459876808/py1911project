

from django.conf.urls import url
from . import views

app_name = 'polls'

urlpatterns = [
    url(r'^$',views.index,name='index'),
    # 如果在正则表达式中有正则分组  那么在视图中必须得有响应的形参
    # 如果正则分组有别名 那么形参名一定要和正则分组别名一致
    url(r'^detail/(?P<qid>\d+)/$',views.detail,name='detail'),
    url(r'^result/(\d+)/$',views.result,name='result'),
    url(r'^login/$',views.login,name='login'),
    url(r'^regist/$',views.regist,name='regist'),
    url(r'^logout/$',views.logout,name='logout')

    # url(r'^$',views.IndexView.as_view(),name='index'),
    # url(r'^detail/(?P<qid>\d+)/$',views.DetailView.as_view(),name='detail'),
    # url(r'^result/(\d+)/$',views.ResultView.as_view(),name='result')
]