from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse

from cart.models import ShoppingCart
from fresh_shop.settings import PAGE_NUMBER
from orders.models import OrderInfo, OrderGoods
from users.models import UserAddress
from utils.functions import get_order_sn


def order(request):
    if request.method == 'GET':
        # 获取当前登录系统的user_id
        user_id = request.session['user_id']
        # 获取当前勾选的商品用于下单
        cart_goods = ShoppingCart.objects.filter(user_id=user_id, is_select=True)
        # 在购物车对象上绑定一个total_price字段，用于存商品的总价
        for cart in cart_goods:
            cart.total_price = cart.nums * cart.goods.shop_price
        # 获取订单地址
        addresses = UserAddress.objects.filter(user_id=user_id)
        return render(request, 'place_order.html', {'cart_goods': cart_goods, 'addresses': addresses})

    if request.method == 'POST':
        """
        接收ajax请求，创建订单
        """
        # 1. 选择购物车中is_select为True的商品
        # 2. 创建订单
        # 3. 创建订单和商品之间的关联关系表，order_goods表
        # 4. 删除购物车中已下单的商品
        user_id = request.session['user_id']
        # 获取收货人的地址id
        address_id = request.POST.get('address_id')
        user_address = UserAddress.objects.filter(id=address_id).first()
        # 获取购物车中当前登录用户勾选的商品
        carts = ShoppingCart.objects.filter(user_id=user_id, is_select=True)
        # 订单货号
        order_sn = get_order_sn()
        # 订单金额
        order_mount = 0
        for cart in carts:
            order_mount += cart.nums * cart.goods.shop_price
        # 创建订单
        order = OrderInfo.objects.create(user_id=user_id,
                                         order_sn=order_sn,
                                         order_mount=order_mount,
                                         address=user_address.address,
                                         signer_name=user_address.signer_name,
                                         signer_mobile=user_address.signer_mobile)
        for cart in carts:
            # 创建订单和商品的详情表
            OrderGoods.objects.create(order_id=order.id,
                                      goods_id=cart.goods_id,
                                      goods_nums=cart.nums)
        carts.delete()
        # 删除session中的商品信息
        if request.session.get('goods'):
            request.session.pop('goods')
        return JsonResponse({'code': 200, 'msg': '请求成功'})


def user_order(request):

    if request.method == 'GET':
        user = request.user
        # 获取分页
        try:
            # 如果page参数不能转化为int类型，则异常，默认page为1
            page = int(request.GET.get('page', 1))
        except:
            page = 1
        # 获取当前用户所有的订单信息
        order_info = OrderInfo.objects.filter(user=user)
        paginator = Paginator(order_info, PAGE_NUMBER)
        order_info = paginator.page(page)
        order_status = OrderInfo.ORDER_STATUS
        return render(request, 'user_center_order.html', {'order_info': order_info, 'order_status': order_status})


def user_order_site(request):

    if request.method == 'GET':
        user = request.user
        user_addresses = UserAddress.objects.filter(user=user).order_by('-id')

        return render(request, 'user_center_site.html', {'user_addresses': user_addresses})


