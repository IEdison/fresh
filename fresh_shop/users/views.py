from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from users.forms import UserRegisterForm, UserLoginForm, UserAddressForm
from users.models import User, UserAddress


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    if request.method == 'POST':
        # 表单验证， is_valid()
        # 验证通过后。使用自定义的Users.objects.create，在跳转到登录页面
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # 保存用户信息
            User.objects.create(username=form.cleaned_data['user_name'],
                                password=make_password(form.cleaned_data['pwd']),
                                email=form.cleaned_data['email'])
            # 注册成功，跳转到登录
            return HttpResponseRedirect(reverse('users:login'))
        else:
            return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            # 获取当前登录的用户对象
            user = User.objects.filter(username=form.cleaned_data['username']).first()
            # 校验密码是否正确
            if not check_password(form.cleaned_data['pwd'], user.password):
                return HttpResponseRedirect(reverse('users:login'))

            # 添加登录成功的验证
            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse('home:index'))
        else:
            return render(request, 'login.html', {'form': form})


def logout(request):
    if request.method == 'GET':
        # 清空session
        request.session.flush()
        # 跳转到首页
        return HttpResponseRedirect(reverse('home:index'))


def is_login(request):
    if request.method == 'GET':
        # 清空session
        user = request.user
        return JsonResponse({'code': 200, 'msg': '请求成功', 'username': user.username})


def user_center_order(request):
    if request.method == 'GET':
        return render(request, 'user_center_info.html')


def address(request):
    if request.method == 'GET':
        user = request.user
        # 获取用户的收货地址信息
        user_addresses = UserAddress.objects.filter(user=user).order_by('-id')
        return render(request, 'user_center_site.html', {'user_addresses': user_addresses})

    if request.method == 'POST':
        # 使用表单验证，验证收货地址的参数是否填写完整
        form = UserAddressForm(request.POST)
        if form.is_valid():
            user = request.user
            address_info = form.cleaned_data
            # 保存收货地址信息
            UserAddress.objects.create(**address_info, user=user)
            # 保存成功收货地址
            return HttpResponseRedirect(reverse('users:user_address'))
        else:
            user = request.user
            # 获取用户的收货地址信息
            user_addresses = UserAddress.objects.filter(user=user).order_by('-id')
            return render(request, 'user_center_site.html', {'form': form, 'user_addresses': user_addresses})
