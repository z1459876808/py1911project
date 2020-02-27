from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *
from django.core import serializers
from .serializer import *

from rest_framework import viewsets


# Create your views here.

class CategoryViewsets(viewsets.ModelViewSet):
    """
    继承ModeLViewSet之后拥有GET POST PUT PATCH DELETE等HTTP动词操作
    queryset指明需要操作的模型列表
    serializer_ cLass 指明序列化类
    """

    queryset = Category.objects.all()

    serializer_class = CategorySerializer
    # def get_serializer_class(self):
        # return CategorySerializer


class GoodViewsets(viewsets.ModelViewSet):
    queryset = Good.objects.all()
    serializer_class = GoodSerializer

# *******************************************************************************************

# def index(request):
#     # return HttpResponse('首页')
#
#     categorys = Category.objects.all()
#     # 如果使用Json或者xml得形式返回数据，则可以实现前后端分离
#     result = serializers.serialize('json', categorys)
#     return JsonResponse(result,safe=False)
#
#     # 如果使用Django模板就是前后端不分离
#     # return render(request, '模板名字')
