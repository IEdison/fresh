from django.contrib.auth.decorators import login_required
from django.conf.urls import url


from orders import views

urlpatterns = [
    # 订单列表页面
    url('order_list/', login_required(views.order_list), name='order_list'),
]
