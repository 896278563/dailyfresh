from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.core.urlresolvers import reverse
import re
from users.models import User
from django.db import IntegrityError
from celery_tasks.tasks import send_active_email
from django.conf import settings
from django.core.mail import send_mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# Create your views here.

class ActiveView(View):
    """邮件激活"""

    def get(self, request):
        """处理邮件激活逻辑"""
        pass




class RegisterView(View):
    """类视图：处理注册"""

    def get(self, requset):
        """处理GET 请求，返回注册页面"""
        return render(requset, 'register.html')

    def post(self, requset):
        """处理POST请求， 实现注册逻辑"""

        # 接受用户注册参数
        user_name = requset.POST.get('user_name')
        password = requset.POST.get('pwd')
        email = requset.POST.get('email')
        allow = requset.POST.get('allow')

        # 校验用户注册参数: 只要有一个数据为空，就返回FALSE， 只有全部为真才返回TRUE
        if not all([user_name, password, email]):
            # 公司中根据开发文档实现需求
            return redirect(reverse('users:register'))

        # 判断邮箱格式
        if not re.match(r"^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$", email):
            return render(requset, 'register.html', {"errmsg":"邮箱格式错误"})

        # 判断是否勾选了协议
        if allow != 'on':
            return render(requset, 'register.html', {"errmsg":"请勾选用户协议"})

        # 保存用户注册参数
        try:
            user = User.objects.create_user(user_name, email, password)
        except IntegrityError:   # 重名异常判断
            return render(requset, 'register.html', {"errmsg":"用户已存在"})

        # 重置激活状态： 需要邮件激活
        user.is_active = False
        # 注意： 更改了数据  需要重新保存
        user.save()

        # 生成token
        token = user.generate_active_tocken()

        # 发送激活邮件： 不能阻塞HttpResponse
        # http://127.0.0.1:8000/users/active/user_id
        # http://127.0.0.1:8000/users/active/user.id
        # http://127.0.0.1:8000/users/active/!@#$&%^YTQRWEGE*&#@^#$!
        #
        # subject = "天天生鲜用户激活"  # 标题
        # body = ""   # 文本邮件体
        # sender = settings.EMAIL_FROM # 发件人
        # receiver = [email]      # 接收人
        # html_body = '<h1>尊敬的用户%s，感谢您注册天天生鲜！</h1>' \
        #             '<br><p>请点击此链接激活您的账号<a href="http://127.0.0.1:8000/users/active/%s">' \
        #             'http://127.0.0.1:8000/users/active/%s</a></p>' %(user_name, token, token)
        # send_mail(subject, body, sender, receiver, html_message=html_body)

        return HttpResponse('这是处理注册逻辑')

# def register(requset):
#     """处理注册页面"""
#
#     # 获取请求方法， 判断是GET/POST请求
#     if requset.method == 'GET':
#         # 处理GET 请求，返回注册页面
#         return render(requset, 'register.html')
#     else:
#         # 处理POST请求， 实现注册逻辑
#         return HttpResponse('这里是实现注册逻辑')