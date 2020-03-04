"""

"""

from django.contrib.auth import backends
from .models import User
from django.db.models import Q


class MyLoginBackend(backends.BaseBackend):
    def authenticate(self, request, **kwargs):
        """

        :param request:
        :param kwargs: 认证参数
        :return: 如果认证成功返回认证用户否则返回None
        """
        username = kwargs['username']
        password = kwargs['password']

        user = User.objects.filter(Q(username=username) | Q(email=username) | Q(telephone=username)).first()
        if user:
            b = user.check_password(password)
            if b:
                return user
            else:
                return None
        else:
            return None
