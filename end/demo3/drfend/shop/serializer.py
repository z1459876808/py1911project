from rest_framework import serializers
from .models import *


# 自定义序列化类
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
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=10, min_length=1,
                                 error_messages={'max_length': '最多十个字', 'min_length': '最少一个字'})

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
    # StringRelatedField()可以显 示关联模型中的__str__ 返回值 many=True 代表多个对象read_only=True 代表只读
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


class GoodImgSerializer(serializers.Serializer):
    img = serializers.ImageField()
    good = serializers.CharField(source='good.name')

    def validate(self, attrs):
        print('初始值', attrs["good"]["name"])
        try:
            g = Good.objects.get(name=attrs["good"]["name"])
            attrs["good"] = g
        except:
            raise serializers.ValidationError('该商品不存在')
        return attrs

    def create(self, validated_data):
        instance = Goodimg.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        instance.img = validated_data.get('img')
        instance.good = validated_data.get('good', instance.good)
        instance.save()
        return instance


class GoodSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20, min_length=2, error_messages={
        "max_length": "最多20个字",
        "min_ength": "最少2个字"
    })
    category = CategorySerializer(label="分类")
    imgs = GoodImgSerializer(label='图片', many=True)

    def validate_category(self, category):
        """
        处理 category
        :param category: 处理的原始值
        :return: 返回的新值
        """
        print("category原始值为", category)
        try:
            Category.objects.get(name=category["name"])
        except:
            raise serializers.ValidationError("输入的分类名不存在")

        return category

    # def validate(self, attrs):
    #     print("收到的数据为", attrs)
    #
    #     try:
    #         c = Category.objects.get(name=attrs["category"]["name"])
    #     except:
    #         c = Category.objects.create(name=attrs["category"]["name"])
    #
    #     attrs["category"] = c
    #     print("更改之后的数据", attrs)
    #
    #     return attrs

    def create(self, validated_data):
        print("创建参数", validated_data)
        instance = Good.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance


class GoodSerializer1(serializers.ModelSerializer):
    # 在序列化时指定宇段在多方 使用source = 模型名.宇段名  read_only = True 表示不能更a
    category = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Good
        fields = ('name', 'desc', 'category')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ['user_permissions', 'groups']

    def validate(self, attrs):
        from django.contrib.auth import hashers
        attrs['password'] = hashers.make_password(attrs['password'])

        return attrs


class UserReigstSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=10, min_length=3, error_messages={'required': '必填项'})
    password = serializers.CharField(max_length=10, min_length=3, write_only=True)
    password2 = serializers.CharField(max_length=10, min_length=3, write_only=True)

    def validate_password2(self, data):
        if data != self.initial_data['password']:
            raise serializers.ValidationError('密码不一致')
        else:
            return data

    def validate(self, attrs):

        del attrs['password2']
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(username=validated_data.get('username'), email=validated_data.get('email'),
                                        password=validated_data.get('password'))


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
