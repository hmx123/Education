from django.contrib.auth.hashers import make_password
from django.shortcuts import render

# Create your views here.
from django.views import View

from users.forms import RegisterForm
from users.models import UserProfile
from utils.email_send import send_register_email
from django_redis import get_redis_connection



class RegisterView(View):
    '''用户注册'''
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html',{'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', None)
            # 如果用户存在，提示错误信息
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已注册'})

            pass_word = request.POST.get('password', None)
            # 实例化user_profile对象
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            # 对保存到数据库密码加密
            user_profile.password = make_password(pass_word)
            user_profile.save()

            send_register_email(user_name, 'register')
            return render(request, 'login.html')
        else:
            return render(request,'register.html', {'register_form': register_form})


class ActiveUserView(View):
    def get(self, request, actice_code):
        # 在redis查询email是否存在
        conn = get_redis_connection('default')
        email_value = conn.get(actice_code)
        if email_value:
            # 查找到邮箱对应的user
            user = UserProfile.objects.get(email=email_value)
            user.is_active = True
            user.save()
        else:
            # 验证失败
            return render(request, 'active_fail.html')

        # 激活成功
        return render(request, 'login.html')





