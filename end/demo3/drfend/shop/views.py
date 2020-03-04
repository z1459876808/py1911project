from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *
from django.core import serializers
from .serializer import *

from rest_framework import viewsets, permissions

from rest_framework.decorators import api_view, action

from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from django.views import View
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins

from . import permissions as mypermissions

from .throtting import MyUser, MyAnon
from .pagination import MyPagination


# Create your views here.


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDietailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryListView2(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, requset):
        return self.list(requset)

    def post(self, request):
        return self.create(request)


class CategoryDietailView2(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def patch(self, request, pk):
        return self.update(request, pk)

    def detele(self, request, pk):
        return self.detele(request, pk)


class CategoryListView1(APIView):
    """
    继承Django自带的View需要重写对应的http方法
    继承ORF自带的4PIView关即可完成请求响应的封装
    """

    def get(self, request):
        seria = CategorySerializer(instance=Category.objects.all(), many=True)
        return Response(seria.data, status=status.HTTP_200_OK)

    def post(self, request):
        seria = CategorySerializer(data=request.data)
        # 从请求中提取的数据序列化之前需要进行校验
        if seria.is_valid():
            seria.save()
            return Response(seria.data, status=status.HTTP_201_CREATED)
        else:
            return Response(seria.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDietailView1(APIView):
    def get(self, request, cid):
        seria = CategorySerializer(instance=get_object_or_404(Category, pk=cid))
        return Response(seria.data, status=status.HTTP_200_OK)

    def put(self, request, cid):
        seria = CategorySerializer(instance=get_object_or_404(Category, pk=cid), data=request.data)
        if seria.is_valid():
            seria.save()
            return Response(seria.data, status=status.HTTP_201_CREATED)
        else:
            return Response(seria.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, cid):
        seria = CategorySerializer(instance=get_object_or_404(Category, pk=cid), data=request.data)
        if seria.is_valid():
            seria.save()
            return Response(seria.data, status=status.HTTP_201_CREATED)
        else:
            return Response(seria.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, cid):
        get_object_or_404(Category, pk=cid).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def categorylist(request):
    if request.method == "GET":
        # instance 为需要序列化的对象来源于数据库
        seria = CategorySerializer(instance=Category.objects.all(), many=True)
        return Response(seria.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        # data为序列化对象来源于请求中掘取的数据
        seria = CategorySerializer(data=request.data)
        # 从请求中提取的数据序列化之前需要进行校验
        if seria.is_valid():
            seria.save()
            return Response(seria.data, status=status.HTTP_201_CREATED)
        else:
            return Response(seria.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def categorydetail(request, cid):
    model = get_object_or_404(Category, pk=cid)
    if request.method == 'GET':
        seria = CategorySerializer(instance=model)
        return Response(seria.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT' or request.method == 'PATCH':
        # 更新就是从请求中提取参数替换掉数据库中取出的数据
        seria = CategorySerializer(instance=model, data=request.data)
        # 验证是否合法
        if seria.is_valid():
            seria.save()
            return Response(seria.data)
        else:
            return Response(seria.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return HttpResponse('当前路由不允许' + request.method + '操作')


class CategoryViewsets1(viewsets.ModelViewSet):
    """
    继承ModeLViewSet之后拥有GET POST PUT PATCH DELETE等HTTP动词操作
    queryset指明需要操作的模型列表
    serializer_ cLass 指明序列化类
    """

    queryset = Category.objects.all()

    # serializer_class = CategorySerializer

    def get_serializer_class(self):
        return CategorySerializer

    @action(methods=['GET'], detail=False)
    def getlatestcategory(self, request):
        seria = CategorySerializer(instance=Category.objects.all()[:2], many=True)
        return Response(data=seria.data, status=status.HTTP_200_OK)


class CategoryViewsets(viewsets.ModelViewSet):
    """
    继承ModeLViewSet之后拥有GET POST PUT PATCH DELETE等HTTP动词操作
    queryset指明需要操作的模型列表
    serializer_ cLass 指明序列化类
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # 用户未登录不显示分类列表 优先级别高于全局配置
    # permission_classes = [permissions.IsAdminUser]

    # 超级管理员类可以创建分类  普通用户也可以查看分类
    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            return [permissions.IsAdminUser()]
        else:
            return []

    throttle_classes = [MyAnon, MyUser]

    # pagination_class = MyPagination



class GoodImgsViewsets(viewsets.ModelViewSet):
    queryset = Goodimg.objects.all()
    serializer_class = GoodImgSerializer


class GoodViewsets(viewsets.ModelViewSet):
    queryset = Good.objects.all()
    serializer_class = GoodSerializer


class UserViewsets1(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin):
    """
    声明用户资源类用户操作:获取个人信息更新个人信息 删除账户
    扩展出action路由  用户操作: 创建账月
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # 使用action扩展 资源的http万法
    @action(methods=['POST'], detail=False)
    def regist(self, request):
        seria = UserReigstSerializer(data=request.data)
        seria.is_valid(raise_exception=True)
        seria.save()
        return Response('创建成功')


class UserViewsets(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin):
    """
    声明用户资源类用户操作:获取个人信息更新个人信息 删除账户
    扩展出action路由  用户操作: 创建账月
    """
    queryset = User.objects.all()

    # serializer_class = UserSerializer

    def get_serializer_class(self):
        print('action代表http方法', self.action)
        if self.action == 'create':
            return UserReigstSerializer
        return UserSerializer


class OredrViewsets(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        """
        超级管理员只可以展示所有订单
        普通用户可以创建修改订单不可以操作其他用户的订单
        """
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        elif self.action == 'update' or self.action == 'partial_update' or self.action == 'retrieve' or self.action == 'destroy':
            return [mypermissions.OrederPermission()]
        else:
            return [permissions.IsAdminUser()]

# http方法                          混合类关键字                   action关键字
# GET列表                           List                          get
# POST创建对象                       Create                       create
# GET 单个对象                       Retrieve                     retrieve
# PUT 修改对象提供全属性              Update                       update
# PATCH 修改对象提供部分属性          Update                       partial_update
# DELETE 删除对象                    Destroy                      destroy


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
