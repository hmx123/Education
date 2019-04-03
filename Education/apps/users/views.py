from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.views import View

from users.forms import RegisterForm, LoginForm, ForgetPwdForm
from users.models import UserProfile, EmailVerifyRecord
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


# 用户激活
class ActiveUserView(View):
    def get(self, request, active_code):
        # 在redis查询email是否存在
        # conn = get_redis_connection('default')
        # email_value = conn.get(actice_code)
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)

        if all_record:
            for record in all_record:
                # 获取到对应的邮箱
                email = record.email
                # 查找到邮箱对应的user
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                # 验证码不对的时候跳转到激活失败页面
        else:
            return render(request, 'active_fail.html')
        # 激活成功跳转到登录页面
        return render(request, "login.html", )

# 设置邮箱和用户都可以登录
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None,**kwargs):
        try:
            # Q为使用并集查询
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            # django的后台中密码加密 UserProfile继承AbstractUser中有check_password验证
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    '''用户登录'''

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        # 实例化
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 获取用户用户名和密码
            user_name = request.POST.get('username', None)
            pass_word = request.POST.get('password', None)
            # 成功返回user对象，失败None
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    # 只有用户激活才能登录
                    login(request, user)
                    return render(request, 'login.html')
                else:
                    return render(request, 'login.html', {'msg': '用户未激活，请前往邮箱激活。', 'login_form': login_form})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误','login_form':login_form})
        else:
            return render(request, 'login.html', {'login_form': login_form})

class ForgetPwdView(View):
    '''找回密码'''
    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html',{'forget_form':forget_form})

    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', None)
            send_register_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    pass

