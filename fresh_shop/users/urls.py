
from django.conf.urls import url

from users import views

urlpatterns = [
    # 注册
    url(r'^register/', views.register, name='register'),
    # 登录
    url(r'^login/', views.login, name='login'),
    # 退出
    url('logout/', views.logout, name='logout'),
    # 登录验证，获取登录系统的用户
    url('is_login/', views.is_login, name='is_login'),
    # 个人信息中心
    url('user_center_order/', views.user_center_order, name='user_center_order'),
    # 收货地址
    url('user_address/', views.address, name='user_address'),
]

