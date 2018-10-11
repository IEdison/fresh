from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from fresh_shop_back.settings import PAGE_NUMBER
from orders.models import OrderInfo


def order_list(request):

    if request.method == 'GET':
        try:
            page = request.GET.get('page', 1)
        except:
            page = 1
        order_infos = OrderInfo.objects.all()
        # 分页
        paginator = Paginator(order_infos, PAGE_NUMBER)
        page = paginator.page(page)
        return render(request, 'order_list.html', {'page': page})
