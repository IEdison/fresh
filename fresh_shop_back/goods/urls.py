
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from goods import views

urlpatterns = [
    # 商品分类列表
    url(r'^goods_category_list/', login_required(views.goods_category_list), name='goods_category_list'),
    # 商品分类编辑页面
    url(r'^goods_category_edit/(\d+)/', login_required(views.goods_category_edit), name='goods_category_edit'),
    # 商品列表
    url(r'^goods_list/', login_required(views.goods_list), name='goods_list'),
    # 添加商品
    url(r'^goods_add/', login_required(views.goods_add), name='goods_add'),
    # 删除商品
    url(r'^goods_delete/(\d+)/', login_required(views.goods_delete), name='goods_delete'),
    # 商品编辑
    url(r'^goods_edit/(\d+)/', login_required(views.goods_edit), name='goods_edit'),
    # 商品编辑
    url(r'^goods_desc/(\d+)/', login_required(views.goods_desc), name='goods_desc'),
]