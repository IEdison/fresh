"""fresh_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import static

from fresh_shop import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 首页模块
    url(r'^home/', include('home.urls', namespace='home')),
    # 商品模块
    url(r'^goods/', include('goods.urls', namespace='goods')),
    # 购物车模块
    url(r'^cart/', include('cart.urls', namespace='cart')),
    # 用户模块
    url(r'^users/', include('users.urls', namespace='users')),
    # 订单模块
    url(r'^orders/', include('orders.urls', namespace='orders')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

