from django.conf.urls import url
from . import views

app_name = 'shop'

urlpatterns = [
    url('^$', views.index, name='index'),
]
