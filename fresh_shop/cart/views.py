from django.shortcuts import render
from django.http import JsonResponse

from goods.models import Goods
from cart.models import ShoppingCart


def add_cart(request):
    if request.method == 'POST':
        # 添加到session中的数据格式为:
        # key==>goods,
        # value==>[[id1, num, 1], [id2, num, 0], [id3, num, 1]....]

        # 1.1 添加到购物车的数据，其实就是添加到session中
        # 1.2 如果商品已经加入到session中，则修改session中商品的个数
        # 1.3 如果商品没有添加到session中，则添加

        # 获取从ajax中传递的商品的id和商品的个数
        goods_id = request.POST.get('goods_id')
        goods_num = request.POST.get('goods_num')
        # 组装存储的数据结构
        goods_list = [goods_id, goods_num, 1]
        # 判断在session中是否存储了商品信息
        if request.session.get('goods'):
            # 标识符: 用于判断当前加入到购物车的商品
            # 如果购物车中已经存在了该商品，则修改flag为1，否则flag还是为0
            flag = 0
            # 说明购物车中已经存储了商品信息
            session_goods = request.session['goods']
            for goods in session_goods:
                # 循环判断，判断加入到session中的商品是否已经存在于session中
                if goods_id == goods[0]:
                    goods[1] = int(goods[1]) + int(goods_num)
                    # 标识符，修改session中的商品后，标识符修改为1
                    flag = 1
            # flag为0，表示添加到session中的商品之前并没有添加
            if not flag:
                session_goods.append(goods_list)
            # 修改成功session中商品的信息
            request.session['goods'] = session_goods
            cart_count = len(session_goods)
        else:
            # 说明购物车中还没有存储商品信息
            data = []
            data.append(goods_list)
            request.session['goods'] = data
            cart_count = 1

        return JsonResponse({'code': 200, 'cart_count': cart_count})


def cart(request):
    if request.method == 'GET':
        # 需要判断用户是否登录， session['user_id']
        # 1. 如果登录，则购物车中展示当前登录用户的购物车表中的数据
        # 2. 如果没有登录，则购物车页面中展示session中的数据
        user_id = request.session.get('user_id')
        if user_id:
            # 登录系统用户, 获取购物车中的商品信息
            shop_cart = ShoppingCart.objects.filter(user_id=user_id)
            goods_all = [(cart.goods, cart.is_select, cart.nums) for cart in shop_cart]

            return render(request, 'cart.html', {'goods_all': goods_all})
        else:
            # 没有登录
            session_goods = request.session.get('goods')
            # 拿到session中所有的商品id值
            if session_goods:
                # [[goods objects, 是否选择 , 商品数量], [goods objects, 是否选择 , 商品数量]]
                goods_all = [(Goods.objects.get(pk=good[0]), good[2], good[1])
                             for good in session_goods]
            else:
                goods_all = ''
            return render(request, 'cart.html', {'goods_all': goods_all})


def f_price(request):
    """
    返回购物车或session中商品的价格，和总价
    {key:[[id1, price1],[id2, price2]], key2: total_price}
    """
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        if user_id:
            # 获取当前登录系统的用户的购物车中的数据
            carts = ShoppingCart.objects.filter(user_id=user_id)
            cart_data = {}
            cart_data['goods_price'] = [(cart.goods_id,
                                         cart.nums * cart.goods.shop_price)
                                        for cart in carts]
            all_price = 0
            # 总的价格
            for cart in carts:
                if cart.is_select:
                    all_price += cart.nums * cart.goods.shop_price
            cart_data['all_price'] = all_price
        else:
            # 拿到session中所有的商品信息,[id, num, is_select]
            session_goods = request.session.get('goods')
            # 返回数据结构，{’goods_price'：[[id1, price1],[id2, price2]...]}
            cart_data = {}
            data_all = []
            # 计算总价
            all_price = 0
            for goods in session_goods:
                data = []
                data.append(goods[0])
                g = Goods.objects.get(pk=goods[0])
                data.append(int(goods[1]) * g.shop_price)
                # 生成的data为: [id1, price1]
                data_all.append(data)
                # 判断如果商品勾选了，才计算总价格
                if goods[2]:
                    all_price += int(goods[1]) * g.shop_price
            cart_data['goods_price'] = data_all
            cart_data['all_price'] = all_price
        return JsonResponse({'code': 200, 'cart_data': cart_data})


def cart_count(request):
    if request.method == 'GET':
        # 判断购物车中商品的个数
        user_id = request.session.get('user_id')
        # 当前购物车中的商品数量
        if user_id:
            # 如果用户登录。则回去购物车表中的商品个数
            count = ShoppingCart.objects.filter(user_id=user_id).count()
        else:
            # 如果用户没有登录，则回去session中的商品个数
            session_goods = request.session.get('goods')
            count = len(session_goods)
        return JsonResponse({'code': 200, 'msg': '请求成功', 'count': count})


def change_goods_num(request):
    if request.method == 'POST':
        # 修改购物车中商品的个数
        # 1. 先判断用户登录与否，如果用户没有登录，则修改session中商品的个数
        # 2. 如果用户登录，需要判断当前修改的商品是否存在于session中，如果存在，则修改session。如果不存在则修改购物车的表
        # 获取修改的商品id，商品个数，商品选择状态
        goods_id = request.POST.get('goods_id')
        goods_num = int(request.POST.get('goods_num'))
        is_select = int(request.POST.get('is_select'))

        user_id = request.session.get('user_id')

        # 先判断要修改的商品是否存在于session中，如果存在则修改session中的商品个数和选择状态
        session_goods = request.session.get('goods')
        # goods的结构为: [id1, num, is_select]
        if session_goods:
            for goods in session_goods:
                if goods_id == goods[0]:
                    # 修改session中商品的个数和选择状态
                    goods[1] = goods_num
                    goods[2] = is_select
            request.session['goods'] = session_goods

        # 如果用户登录了，则需要在修改购物车中数据，因为session中的商品有可能并不在购物车表中
        if user_id:
            # 修改购物车中商品个数
            ShoppingCart.objects.filter(user_id=user_id, goods_id=goods_id).update(nums=goods_num,
                                                                                   is_select=is_select)
        return JsonResponse({'code': 200, 'msg': '请求成功'})
