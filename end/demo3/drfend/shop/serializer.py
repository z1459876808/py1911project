from rest_framework import serializers
from .models import *


class CustomSerializer(serializers.RelatedField):
    """
    自定义序列化类
    """

    def to_representation(self, value):
        """
        重写字段的输出格式
        :param value:
        :return:
        """

        return str(value.id) + '--' + value.name + '--' + value.desc


class CategorySerializer(serializers.Serializer):
    """
    序列化决定了模型序列化细节
    """
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=10, min_length=3,
                                 error_messages={'max_length': '最多十个字', 'min_length': '最少三个字'})

    def create(self, validated_data):
        """
        通过重写create方法来定义模型创建方式
        :param validated_data:
        :return:
        """
        instance = Category.objects.create(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        """
        通过重写update方法来定义模型的更新方法
        :param instance:  更改之前的实例
        :param validated_data:   更改参数
        :return:    返回新的实例
        """

        instance.name = validated_data.get('name')
        instance.save()
        return instance


class CategorySerializer1(serializers.ModelSerializer):
    """
    编写针对Category的序列化类
    本类指明了Category的序列化细节
    需要继承ModelSerializer才可以针对模型进行序列化
    在Meta类中model 指明序列化的模型  fields指明序列化的字段

    """
    # goods - -定要和related.name的值- 致
    # StringRelatedField()可以显 示关联模型中的__str__ 返回值 many=True 代表多个对象read_ only=True 代表只读
    goods = serializers.StringRelatedField(many=True)

    # PrimaryKeyRelatedField显示主健值
    # goods = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    # SlugRelatedField显示自定义字段值
    # goods = serializers.SlugRelatedField(s1ug_field='name', many=True, read_only=True)

    # 显示资源RestFuLAPI
    # goods = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='good-detail')

    # 自定义序列化类
    # goods = CustomSerializer(many=True, read_only=True)
    # goods = GoodSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'goods')


class GoodSerializer(serializers.ModelSerializer):
    # 在序列化时指定宇段在多方 使用source = 模型名.宇段名  read_only = True 表示不能更a
    category = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Good
        fields = ('name', 'desc', 'category')
