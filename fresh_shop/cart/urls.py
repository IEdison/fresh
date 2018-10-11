
from django.conf.urls import url

from cart import views

urlpatterns = [
    # 添加到购物车
    url(r'add_cart/', views.add_cart, name='add_cart'),
    # 购物车页面
    url(r'^cart/', views.cart, name='cart'),
    # 刷新价格
    url(r'^f_price/', views.f_price, name='f_price'),
    # 购物车数据
    url(r'^cart_count/', views.cart_count, name='cart_count'),
    # 修改购物车中商品的个数
    url(r'^change_goods_num/', views.change_goods_num, name='change_goods_num'),
]

