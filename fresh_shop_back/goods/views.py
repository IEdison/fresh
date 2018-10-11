from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from fresh_shop_back.settings import PAGE_NUMBER
from goods.models import GoodsCategory, Goods
from goods.forms import GoodsForm


def goods_category_list(request):
    if request.method == 'GET':
        # 获取分类信息
        categorys = GoodsCategory.objects.all()
        # 返回类型
        category_types = GoodsCategory.CATEGORY_TYPE
        return render(request, 'goods_category_list.html',
                      {'categorys': categorys,
                       'category_types': category_types})


def goods_category_edit(request, id):
    if request.method == 'GET':
        # 获取当前选择的商品分类
        category = GoodsCategory.objects.get(pk=id)
        # 返回商品类型
        categorys_types = GoodsCategory.CATEGORY_TYPE
        return render(request, 'goods_category_detail.html',
                      {'category': category, 'categorys_types': categorys_types})

    if request.method == 'POST':
        # 获取图片
        category_front_image = request.FILES.get('category_front_image')
        if category_front_image:
            category = GoodsCategory.objects.get(pk=id)
            category.category_front_image = category_front_image
            category.save()
        return HttpResponseRedirect(reverse('goods:goods_category_list'))


def goods_list(request):
    if request.method == 'GET':
        try:
            page_number = int(request.GET.get('page', 1))
        except:
            page_number = 1
        # 获取所有商品信息
        goods = Goods.objects.all()
        # 返回商品类型
        category_types = GoodsCategory.CATEGORY_TYPE
        # 分页
        paginator = Paginator(goods, PAGE_NUMBER)
        page = paginator.page(page_number)
        return render(request, 'goods_list.html', {'page': page, 'category_types': category_types})


def goods_add(request):
    if request.method == 'GET':
        category_types = GoodsCategory.CATEGORY_TYPE
        return render(request, 'goods_detail.html', {'category_types': category_types})

    if request.method == 'POST':
        # 保存商品数据，并跳转到商品列表页面
        # 1. 获取页面中传递的参数，并校验是否填写完整
        # 2. 保存
        # 3. 跳转到列表页面
        form = GoodsForm(request.POST, request.FILES)
        if form.is_valid():
            # 保存, def xxx(*args, **kwargs)
            data = form.cleaned_data
            # 保存
            Goods.objects.create(**data)
            # 跳转到列表页面
            return HttpResponseRedirect(reverse('goods:goods_list'))
        else:
            # 字段验证不通过，返回页面，并在页面中使用form.errors拿到错误信息
            return render(request, 'goods_detail.html', {'form': form})


def goods_delete(request, id):
    if request.method == 'POST':
        # 删除商品
        Goods.objects.filter(pk=id).delete()
        return JsonResponse({'code': 200, 'msg': '请求成功'})


def goods_edit(request, id):
    if request.method == 'GET':
        # 获取需要编辑的商品对象
        goods = Goods.objects.get(pk=id)
        category_types = GoodsCategory.CATEGORY_TYPE
        return render(request, 'goods_detail.html', {'goods': goods, 'category_types': category_types})
    if request.method == 'POST':
        form = GoodsForm(request.POST, request.FILES)
        if form.is_valid():
            # 获取表单验证中的参数，其中包含了封面图的键值对
            data = form.cleaned_data
            # 从字典中剔出封面图
            goods_front_image = data.pop('goods_front_image')
            # 判断，如果修改了封面图，则进行单独的修改
            if goods_front_image:
                goods = Goods.objects.filter(pk=id).first()
                goods.goods_front_image = goods_front_image
                goods.save()
            # 更新操作
            Goods.objects.filter(pk=id).update(**data)
            return HttpResponseRedirect(reverse('goods:goods_list'))
        else:
            # 验证表单失败
            goods = Goods.objects.get(pk=id)
            category_types = GoodsCategory.CATEGORY_TYPE
            return render(request, 'goods_detail.html',
                          {'goods': goods, 'category_types': category_types,
                           'form': form})


def goods_desc(request, id):
    if request.method == 'GET':
        goods = Goods.objects.get(pk=id)
        return render(request, 'goods_desc.html', {'goods': goods})

    if request.method == 'POST':
        # 保存商品的描述信息
        content = request.POST.get('content')
        Goods.objects.filter(pk=id).update(goods_desc=content)
        return HttpResponseRedirect(reverse('goods:goods_list'))
