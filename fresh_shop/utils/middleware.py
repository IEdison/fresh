
import re

from django.utils.deprecation import  MiddlewareMixin
from django.http import HttpResponseRedirect
from django.urls import reverse

from users.models import User
from cart.models import ShoppingCart


class UserAuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 登录验证中间件
        # 不需要登录验证的URL地址
        not_need_check = ['/home/index/', '/users/login/', '/users/register/',
                          '/cart/cart/', '/cart/f_price/', '/cart/add_cart/',
                          '/media/(.*)', '/static/(.*)', '/goods/goods_detail/(\d+)/',
                          '/cart/cart_count/', '/cart/change_goods_num/']
        path = request.path
        for not_path in not_need_check:
            # 匹配当前URL地址是不是不需要登录验证
            if re.match(not_path, path):
                return None

        # 登录验证开始
        user_id = request.session.get('user_id')
        # 没有登录，获取不到user_id参数，则跳转到登录页面
        if not user_id:
            return HttpResponseRedirect(reverse('users:login'))

        # 给request.user赋值，赋值为当前登录系统的用户
        user = User.objects.get(pk=user_id)
        request.user = user

        return None


class UserSessionMiddleware(MiddlewareMixin):
    # 同步session数据到shopping_cart表

    def process_request(self, request):
        # 判断用户是否登录
        user_id = request.session.get('user_id')
        if user_id:
            # 获取到session中的商品数据
            session_goods = request.session.get('goods')
            if session_goods:
                # 1. 如果购物车中没有session中的商品数据，则创建
                # 2. 如果购物车中有session中的商品数据，则更新
                # session中商品信息的结构:[[id, num, is_select],[id, num, is_select]]
                for goods in session_goods:
                    # 查询购物车中是否存在商品信息
                    cart = ShoppingCart.objects.filter(goods_id=goods[0],
                                                       user_id=user_id).first()
                    if cart:
                        # 如果购物车中存在session中保存的商品信息，则修改数量和选择状态
                        if cart.nums != goods[1]:
                            # 如果商品数量不相同，则同步商品的数量
                            cart.nums = int(goods[1])
                        # 同步商品选择状态
                        cart.is_select = int(goods[2])
                        cart.save()
                    else:
                        # session中的商品数据不存在于购物车中，则保存
                        ShoppingCart.objects.create(user_id=user_id,
                                                    goods_id=goods[0],
                                                    nums=int(goods[1]),
                                                    is_select=int(goods[2]))
                return None


